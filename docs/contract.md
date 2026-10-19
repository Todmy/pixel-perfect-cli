# Contract v1 (2026-10-19)

Semantic contract the CLI, the capture step and the eval harness share. Changes to it are a new version, recorded in the m2 ledger.

## CLI

```
pixel-perfect diff DESIGN.png SHOT.png [--design-map D.json] [--shot-map S.json] [--crop-to-design] [--tol F] [--min-area N]
pixel-perfect capture URL_OR_HTML_FILE --out SHOT.png [--map S.json] [--width W] [--height H | --full-page] [--dpr N] [--mask SELECTOR]... [--browser chromium|webkit|firefox]
```

Exit codes: `0` pass, `1` deltas, `2` review only, `12` fatal. stdout is one JSON document.

## Structure map (`--design-map`, `--shot-map`, written by `capture --map`)

```json
{"version": 1, "source": "dom", "viewport": {"width": 1440, "height": 900}, "dpr": 1,
 "nodes": [{"id": "body>main>section.pricing>div.card:nth-of-type(2)",
            "selector": "same as id", "tag": "div", "parent": "<parent id or null>",
            "bbox": [x, y, w, h], "text": "own trimmed text or null",
            "style": {"color": "#101828", "background-color": "#F2F4F7", "font-size": "15px",
                      "font-weight": "600", "border-radius": "8px", "padding": "24px", "margin": "0px", "gap": "12px"}}]}
```

- `bbox` is in CSS pixels of the page, top-left of the captured image is (0, 0). `diff` scales by `dpr` itself.
- Only rendered, visible nodes with non-zero size. `id` is a deterministic CSS path; it must be identical for the same DOM across runs.
- `source` is `dom` today; a Figma node tree adapter will write `figma` with Figma node names as `id`.

## Deltas (`diff` output)

```json
{"status": "pass|deltas|review|fatal", "global": {...}, "deltas": [Delta], "review": [Delta], "regions": [...], "timing_ms": {...}}
```

Delta: `{"type", "id", "selector", "text", "bbox", "shot_bbox", "expected", "actual", "axis", "after", "confidence", "source"}`

- `type` in `gap | padding | align | size | color | text | appearance | missing | extra`.
- `id`: stable across iterations for the same element. From a map: the map `id`. Pixels only: content-derived, not a tree position.
- `selector` / `text`: present whenever a map covers the element, so an agent can find the code.
- `source`: `map` or `pixels`. `confidence`: `high` goes to `deltas`, `low` goes to `review`.
- Same inputs give byte-identical stdout, except the `timing_ms` object (wall-clock); scorers strip `timing_ms` before hashing. (v1.1)

## Eval ground truth (`eval/`)

Each pair has `truth.json`: `{"page", "split": "train|heldout", "kind": "mutation|noise|dynamic", "mutations": [{"type", "selector", "property", "from", "to"}]}`. A noise pair has `mutations: []`. The scorer matches reported deltas to mutations by selector, or by bbox overlap with the mutated element (or its parent for gap/padding) when the run had no map.

## Gates (premortem checklist)

| Metric | Gate |
|---|---|
| false deltas per screen, median, held-out | <= 1 |
| recall of mutations, held-out | reported, no gate until baseline exists |
| review rate on noise pairs | < 10% of elements, 0 confident deltas on same-engine re-render |
| determinism | identical stdout hash on 2 runs, every pair |
| runtime, 1440x4000 page | < 5 s |
