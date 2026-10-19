# pixel-perfect-cli

Deterministic visual diff of two UI images (design vs screenshot) for AI agents. Same input, same JSON.

```sh
uv tool install --from . pixel-perfect-cli
pixel-perfect design.png shot.png        # JSON on stdout
```

Exit codes: `0` pass, `1` deltas, `12` fatal (missing file, aspect mismatch).

Pipeline (stages 1-5 done, OCR pending):
1. Normalize: ICC to sRGB, alpha onto white, DPR resize, global shift via phase correlation.
2. Pixel gate: Lab ΔE mask, connected-component regions, NVIDIA FLIP severity.
3. Segment: recursive XY-cut into an element tree; containers = uniform-border boxes.
4. Pair elements: Hungarian on content similarity, size, position.
5. Explain: gap / padding / align / size / color / appearance / missing / extra. Moves are decomposed into parent gaps, so cascades collapse to one cause.
