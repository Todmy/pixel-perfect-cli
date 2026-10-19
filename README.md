# pixel-perfect-cli

Deterministic visual diff of two UI images (design vs screenshot) for AI agents. Same input, same JSON.

```sh
uv tool install --from . pixel-perfect-cli
pixel-perfect design.png shot.png        # JSON on stdout
```

Exit codes: `0` pass, `1` deltas (fix them), `2` review only (low-confidence appearance: escalate crops to a VLM), `12` fatal.

Noise floor is calibrated on the same page rendered by Chromium, WebKit, Firefox and Chromium@2x (`tests/fixtures/web/noise_*`). Retina: zero false deltas. Other engines: 1-2 residual (glyph descender height, synthetic bold). Text content changes land in `review` until OCR lands.

Pipeline (stages 1-5 done, OCR pending):
1. Normalize: ICC to sRGB, alpha onto white, DPR resize, global shift via phase correlation.
2. Pixel gate: Lab ΔE mask, connected-component regions, NVIDIA FLIP severity.
3. Segment: recursive XY-cut into an element tree; containers = uniform-border boxes.
4. Pair elements: Hungarian on content similarity, size, position.
5. Explain: gap / padding / align / size / color / appearance / missing / extra. Moves are decomposed into parent gaps, so cascades collapse to one cause.
