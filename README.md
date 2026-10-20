# pixel-perfect-cli

Deterministic visual diff of a design and a screenshot, for AI agents. Same input, same JSON. Full spec: [docs/contract.md](docs/contract.md).

## Install

```sh
uv tool install --from ~/github/pixel-perfect-cli pixel-perfect-cli
```

`diff` needs no browser. `capture` needs a Playwright browser; if it is missing, `capture` exits 12 and prints the exact install command (`<tool python> -m playwright install chromium`, ~30 s).

Check a fresh-user install without touching your HOME: `scripts/smoke_install.sh`.

## Commands

```sh
pixel-perfect capture page.html --out shot.png --map shot.json     # or a URL; --width/--height/--full-page/--dpr/--mask
pixel-perfect diff design.png shot.png --design-map design.json --shot-map shot.json
```

stdout is one JSON document: `status`, `deltas` (confident, fix them), `review` (low confidence: escalate the crops to a VLM).

Exit codes: `0` pass, `1` deltas, `2` review only, `12` fatal (bad input, missing browser; `{"status": "fatal", "error": ...}`).

## Agent loop

1. `capture` the built page with `--map`.
2. `diff` against the design and its map.
3. Apply each delta's `fix` (`{"selector", "property", "value"}`); when `fix` is null, use `selector`, `expected`, `actual`.
4. Repeat until exit 0. Delta `id`s are stable across iterations, so you can tell fixed from new.

## Maps

A structure map is the DOM node tree (CSS path id, bbox, computed styles) that `capture --map` writes. With maps on both sides, `diff` names the element, its selector and the one CSS property to change. Without maps it falls back to pixels: segment, pair, explain.

Use maps. On the held-out eval (63 pairs, `eval/results/final-c6f1a3d.md`): maps mode recall 1.0, median 0 false deltas per screen; pixels-only recall 0.14, median 3 false deltas.

## Limits

- No Figma adapter yet: the design side needs a rendered PNG plus a DOM map (render the design HTML with `capture`). Pixels-only works on any PNG but is weak.
- Text content changes land in `review` (no OCR).
- The 5 s runtime gate on a 1440x4000 page is unproven: measured 4.2 s (maps) and 10.6 s (pixels) on a loaded machine.
