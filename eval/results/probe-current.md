# Scoreboard: probe-current

Corpus sha256 `7d286320f428ff072441200a85c21d7ad05d4f0f21f0095c02aaf16f82e65c74`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: all

## Mode: pixels (UNSUPPORTED)

Command: `pixel-perfect diff {design} {shot}`

CLI rejected this mode:

```
usage: pixel-perfect [-h] [--tol TOL] [--min-area MIN_AREA] design shot
pixel-perfect: error: unrecognized arguments: eval/corpus/article/added/shot.png
```

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | UNKNOWN |
| recall_heldout>0_and>=baseline | UNKNOWN |
| review_rate_noise<10% | UNKNOWN |
| rerender_confident_deltas==0 | UNKNOWN |
| determinism_every_pair | UNKNOWN |
| runtime_long_page<5s | UNKNOWN |
| no_errors_or_fatal | UNKNOWN |

Recall baseline (heldout): None. Long-page (>= 4000 px) max runtime (min of 2 runs): None s. Load average before/after: [7.9, 7.9]

## Mode: maps (UNSUPPORTED)

Command: `pixel-perfect diff {design} {shot} --design-map {design_map} --shot-map {shot_map}`

CLI rejected this mode:

```
usage: pixel-perfect [-h] [--tol TOL] [--min-area MIN_AREA] design shot
pixel-perfect: error: unrecognized arguments: eval/corpus/article/added/shot.png --design-map eval/corpus/article/design-map.json --shot-map eval/corpus/article/added/shot-map.json
```

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | UNKNOWN |
| recall_heldout>0_and>=baseline | UNKNOWN |
| review_rate_noise<10% | UNKNOWN |
| rerender_confident_deltas==0 | UNKNOWN |
| determinism_every_pair | UNKNOWN |
| runtime_long_page<5s | UNKNOWN |
| no_errors_or_fatal | UNKNOWN |

Recall baseline (heldout): None. Long-page (>= 4000 px) max runtime (min of 2 runs): None s. Load average before/after: [7.9, 7.9]
