# pixel-perfect-cli

Deterministic visual diff of two UI images (design vs screenshot) for AI agents. Same input, same JSON.

```sh
uv tool install --from . pixel-perfect-cli
pixel-perfect design.png shot.png        # JSON on stdout
```

Exit codes: `0` pass, `1` deltas, `12` fatal (missing file, aspect mismatch).

Pipeline (stages 1-2 of 5 done):
1. Normalize: ICC to sRGB, alpha onto white, DPR resize, global shift via phase correlation.
2. Pixel gate: Lab ΔE mask, connected-component regions, NVIDIA FLIP severity.
3. Segment (XY-cut + connected components). TODO
4. Pair elements (Hungarian). TODO
5. Measure: shift, gap, color ΔE, text. TODO
