# Scoreboard: probe-legacy

Corpus sha256 `7dee141652f3bf94d41865f9037760e3e7a31e69183b22e96713b77989af028a`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: all

## Mode: pixels (UNSUPPORTED)

Command: `pixel-perfect {design} {shot}`

CLI rejected this mode:

```
usage: pixel-perfect [-h] {diff,capture} ...
pixel-perfect: error: argument cmd: invalid choice: 'eval/corpus/article/design.png' (choose from diff, capture)
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

Recall baseline (heldout): None. Long-page (>= 4000 px) max runtime (min of 2 runs): None s. Load average before/after: [12.5, 12.5]
