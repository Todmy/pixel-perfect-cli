"""Score a diff CLI against the frozen eval corpus (Contract v1). The CLI runs only as a subprocess.

Run: uv run python -m eval.score --label NAME [--mode pixels|maps|both] [--split train|heldout|all] [--gate]
     [--cmd "pixel-perfect diff {design} {shot}"] [--legacy]

Matching (Contract v1): a delta that carries a selector must name the mutated element (or its parent for
gap/padding/margin); a delta without one matches by bbox IoU >= 0.3 with the element (or parent) in design or shot.
Deltas on dynamic-content elements are counted apart, not as false. Errors and fatals never count as passes.
"""

import argparse
import hashlib
import json
import os
import re
import shlex
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = Path(__file__).parent / "corpus"
RESULTS = Path(__file__).parent / "results"
DEFAULT_CMD = "pixel-perfect diff {design} {shot}"
LEGACY_CMD = "pixel-perfect {design} {shot}"
MAP_FLAGS = "--design-map {design_map} --shot-map {shot_map}"
IOU_MIN = 0.3
SPACING = {"gap", "padding", "margin"}
LONG_PAGE = 4000  # px: the runtime gate applies to pages at least this tall
ARGPARSE = re.compile(r"usage:|unrecognized arguments|invalid choice|the following arguments are required")


def iou(a, b) -> float:
    if not a or not b:
        return 0.0
    ix = max(0.0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = a[2] * a[3] + b[2] * b[3] - inter
    return inter / union if union > 0 else 0.0


def hits(delta: dict, ids: set, boxes: list) -> bool:
    if sel := delta.get("selector"):  # map-backed: identity is exact, overlap does not rescue a wrong element
        return sel in ids
    return any(iou(db, b) >= IOU_MIN for db in (delta.get("bbox"), delta.get("shot_bbox")) for b in boxes)


def targets(m: dict) -> tuple[set, list]:
    ids, boxes = {m["selector"]}, [m["bbox"], m["shot_bbox"]]
    if m["type"] in SPACING:
        ids.add(m["parent"])
        boxes.append(m["parent_bbox"])
    return ids, [b for b in boxes if b]


def judge(out: dict, truth: dict, dmap: dict) -> dict:
    muts = truth["mutations"]
    dyn_ids = set(truth["dynamic"])
    dyn_boxes = [n["bbox"] for n in dmap["nodes"] if n["id"] in dyn_ids]
    found, found_any = set(), set()
    false = dup = dyn = 0
    for bucket in ("deltas", "review"):
        for d in out.get(bucket) or []:
            idx = next((i for i, m in enumerate(muts) if hits(d, *targets(m))), None)
            if idx is not None:
                found_any.add(idx)
                if bucket == "deltas":
                    dup += idx in found
                    found.add(idx)
            elif bucket == "deltas":
                if hits(d, dyn_ids, dyn_boxes):
                    dyn += 1
                else:
                    false += 1
    return {"mutations": len(muts), "found": len(found), "found_any": len(found_any), "false_deltas": false,
            "dup_deltas": dup, "dynamic_deltas": dyn, "review_items": len(out.get("review") or [])}


def png_height(path: Path) -> int:
    with open(path, "rb") as f:
        return int.from_bytes(f.read(24)[20:24], "big")  # IHDR height


def run(cmd: list[str], timeout: float) -> dict:
    t = time.perf_counter()
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"exit": None, "stdout": b"", "stderr": "timeout", "wall_s": timeout}
    return {"exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr.decode(errors="replace")[-2000:],
            "wall_s": round(time.perf_counter() - t, 3)}


def pairs(split: str) -> list[Path]:
    out = sorted(p.parent for p in CORPUS.glob("*/*/truth.json"))
    return [p for p in out if split == "all" or json.loads((p / "truth.json").read_text())["split"] == split]


def score_mode(template: str, mode: str, split: str, timeout: float) -> dict:
    if mode == "maps":
        template += " " + MAP_FLAGS
    recs = []
    for d in pairs(split):
        truth = json.loads((d / "truth.json").read_text())
        rel = lambda p: str((d / p).resolve().relative_to(ROOT))  # noqa: E731
        paths = {"design": rel(truth["design"]), "shot": rel("shot.png"),
                 "design_map": rel(truth["design_map"]), "shot_map": rel("shot-map.json")}
        cmd = [tok.format(**paths) for tok in shlex.split(template)]
        a, b = run(cmd, timeout), run(cmd, timeout)
        try:
            out = json.loads(a["stdout"])
        except ValueError:
            out = None
        if out is None and ARGPARSE.search(a["stderr"]):
            return {"status": "UNSUPPORTED", "command": template, "reason": a["stderr"].strip()[-500:], "pairs": []}
        dmap = json.loads((d / truth["design_map"]).read_text())
        rec = {"pair": truth["pair"], "page": truth["page"], "page_kind": truth["page_kind"], "split": truth["split"],
               "kind": truth["kind"], "noise": truth["noise"], "shot_engine": truth["shot_engine"],
               "elements": len(dmap["nodes"]), "page_height": png_height(d / truth["design"]),
               "exit": a["exit"], "status": (out or {}).get("status"),
               "error": None if out and out.get("status") != "fatal" else (out or {}).get("error") or a["stderr"][-300:] or "no JSON on stdout",
               "deterministic": a["exit"] is not None and a["stdout"] == b["stdout"],
               "stdout_sha256": hashlib.sha256(a["stdout"]).hexdigest(), "wall_s": [a["wall_s"], b["wall_s"]]}
        rec.update(judge(out or {}, truth, dmap))
        recs.append(rec)
    return {"status": "OK", "command": template, "pairs": recs}


def pct(xs: list[float], q: float) -> float | None:
    if not xs:
        return None
    xs = sorted(xs)
    return xs[min(len(xs) - 1, max(0, round(q * len(xs) + 0.5) - 1))]  # nearest-rank


def agg(recs: list[dict]) -> dict:
    ok = [r for r in recs if not r["error"]]
    muts = sum(r["mutations"] for r in recs)
    noise = [r for r in ok if r["kind"] == "noise"]
    elems = sum(r["elements"] for r in noise)
    return {"pairs": len(recs), "errors": len(recs) - len(ok),
            "median_false_deltas": statistics.median([r["false_deltas"] for r in ok]) if ok else None,
            "mean_false_deltas": round(statistics.mean([r["false_deltas"] for r in ok]), 3) if ok else None,
            "mutations": muts, "recall": round(sum(r["found"] for r in recs) / muts, 3) if muts else None,
            "recall_incl_review": round(sum(r["found_any"] for r in recs) / muts, 3) if muts else None,
            "review_rate_noise": round(sum(r["review_items"] for r in noise) / elems, 4) if elems else None,
            "rerender_confident_deltas": sum(r["false_deltas"] + r["dynamic_deltas"] for r in ok if r["noise"] == "rerender"),
            "dynamic_deltas": sum(r["dynamic_deltas"] for r in recs),
            "determinism_failures": sum(not r["deterministic"] for r in recs),
            "p95_runtime_s": pct([w for r in recs for w in r["wall_s"]], 0.95)}


def gates(recs: list[dict], baseline_recall: float | None, is_baseline: bool) -> dict:
    held = agg([r for r in recs if r["split"] == "heldout"])
    alls = agg(recs)
    long = [min(r["wall_s"]) for r in recs if r["page_height"] >= LONG_PAGE]  # min of 2 runs: damps machine load
    rerender = [r for r in recs if r["noise"] == "rerender"]

    def g(cond, unknown=False):
        return "UNKNOWN" if unknown else "PASS" if cond else "FAIL"
    rec = held["recall"]
    if rec is None:
        recall_gate = "UNKNOWN"
    elif rec == 0:
        recall_gate = "FAIL"
    elif is_baseline:
        recall_gate = "PASS"
    else:
        recall_gate = g(baseline_recall is not None and rec >= baseline_recall, baseline_recall is None)
    return {
        "false_deltas_median_heldout<=1": g((held["median_false_deltas"] or 0) <= 1, held["median_false_deltas"] is None),
        "recall_heldout>0_and>=baseline": recall_gate,
        "review_rate_noise<10%": g((alls["review_rate_noise"] or 0) < 0.10, alls["review_rate_noise"] is None),
        "rerender_confident_deltas==0": g(alls["rerender_confident_deltas"] == 0 and not any(r["error"] for r in rerender), not rerender),
        "determinism_every_pair": g(alls["determinism_failures"] == 0, not recs),
        "runtime_long_page<5s": g(long and max(long) < 5.0, not long),
        "no_errors_or_fatal": g(alls["errors"] == 0, not recs),
    }


def table(rows: list[tuple[str, dict]]) -> str:
    cols = ["pairs", "errors", "median_false_deltas", "mean_false_deltas", "recall", "recall_incl_review",
            "review_rate_noise", "rerender_confident_deltas", "dynamic_deltas", "determinism_failures", "p95_runtime_s"]
    lines = ["| group | " + " | ".join(cols) + " |", "|---" * (len(cols) + 1) + "|"]
    lines += [f"| {name} | " + " | ".join("-" if a[c] is None else str(a[c]) for c in cols) + " |" for name, a in rows]
    return "\n".join(lines)


def corpus_sha() -> str:
    h = hashlib.sha256()
    for f in sorted(CORPUS.rglob("*")):
        if f.is_file():
            h.update(str(f.relative_to(CORPUS)).encode())
            h.update(f.read_bytes())
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(prog="eval.score", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", required=True)
    ap.add_argument("--mode", choices=["pixels", "maps", "both"], default="both")
    ap.add_argument("--split", choices=["train", "heldout", "all"], default="all")
    ap.add_argument("--gate", action="store_true", help="exit 1 if any gate is FAIL or UNKNOWN")
    ap.add_argument("--cmd", help=f"command template, default '{DEFAULT_CMD}'")
    ap.add_argument("--legacy", action="store_true", help=f"use the pre-contract form '{LEGACY_CMD}'")
    ap.add_argument("--timeout", type=float, default=120.0, help="seconds per CLI call (default 120)")
    a = ap.parse_args()
    template = a.cmd or (LEGACY_CMD if a.legacy else DEFAULT_CMD)
    base_file = RESULTS / "baseline.json"
    base = json.loads(base_file.read_text()) if base_file.exists() and a.label != "baseline" else None

    result = {"label": a.label, "split": a.split, "corpus_sha256": corpus_sha(), "synthetic_proxy": True, "modes": {}}
    md = [f"# Scoreboard: {a.label}", "", f"Corpus sha256 `{result['corpus_sha256']}`. SYNTHETIC PROXY corpus "
          "(design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: " + a.split, ""]
    failed = False
    for mode in (["pixels", "maps"] if a.mode == "both" else [a.mode]):
        load = os.getloadavg()[0]
        r = score_mode(template, mode, a.split, a.timeout)
        r["loadavg"] = [round(load, 1), round(os.getloadavg()[0], 1)]  # runtime gate is only as good as an idle machine
        md += [f"## Mode: {mode} ({r['status']})", "", f"Command: `{r['command']}`", ""]
        if r["status"] == "UNSUPPORTED":
            r["gates"] = {k: "UNKNOWN" for k in gates([], None, False)}
            md += ["CLI rejected this mode:", "", "```", r["reason"], "```", ""]
        else:
            recs = r["pairs"]
            bm = (base or {}).get("modes", {})
            bmode = bm.get(mode) if bm.get(mode, {}).get("status") == "OK" else bm.get("pixels")
            brecall = bmode["groups"]["heldout"]["recall"] if bmode and bmode.get("status") == "OK" else None
            r["baseline_recall_heldout"] = brecall
            r["groups"] = {s: agg([x for x in recs if s == "all" or x["split"] == s]) for s in ("all", "train", "heldout")}
            r["by_page_kind"] = {f"{s}/{k}": agg([x for x in recs if x["split"] == s and x["page_kind"] == k])
                                 for s, k in sorted({(x["split"], x["page_kind"]) for x in recs})}
            r["by_pair_kind"] = {f"{s}/{k}": agg([x for x in recs if x["split"] == s and (x["noise"] or x["kind"]) == k])
                                 for s, k in sorted({(x["split"], x["noise"] or x["kind"]) for x in recs})}
            r["gates"] = gates(recs, brecall, a.label == "baseline")
            r["long_page_max_runtime_s"] = max((min(x["wall_s"]) for x in recs if x["page_height"] >= LONG_PAGE), default=None)
            md += [table(list(r["groups"].items())), "", "### Per page kind", "", table(list(r["by_page_kind"].items())), "",
                   "### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)", "",
                   table(list(r["by_pair_kind"].items())), ""]
            errs = [x for x in recs if x["error"]][:10]
            if errs:
                md += ["### First errors", ""] + [f"- `{x['pair']}`: {str(x['error'])[:200]!r}" for x in errs] + [""]
        md += ["### Gates", "", "| gate | result |", "|---|---|"] + [f"| {k} | {v} |" for k, v in r["gates"].items()]
        md += ["", f"Recall baseline (heldout): {r.get('baseline_recall_heldout')}. "
               f"Long-page (>= {LONG_PAGE} px) max runtime (min of 2 runs): "
               f"{r.get('long_page_max_runtime_s')} s. Load average before/after: {r['loadavg']}", ""]
        failed |= any(v != "PASS" for v in r["gates"].values())
        result["modes"][mode] = r
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"{a.label}.json").write_text(json.dumps(result, indent=1))
    (RESULTS / f"{a.label}.md").write_text("\n".join(md))
    print("\n".join(md))
    sys.exit(1 if a.gate and failed else 0)


if __name__ == "__main__":
    main()
