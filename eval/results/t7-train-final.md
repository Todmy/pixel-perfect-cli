# Scoreboard: t7-train-final

Corpus sha256 `7dee141652f3bf94d41865f9037760e3e7a31e69183b22e96713b77989af028a`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: train

## Mode: pixels (OK)

Command: `pixel-perfect diff {design} {shot}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 114 | 0 | 2.5 | 10.167 | 0.179 | 0.244 | 0.1403 | 0 | 0 | 0 | 3.059 |
| train | 114 | 0 | 2.5 | 10.167 | 0.179 | 0.244 | 0.1403 | 0 | 0 | 0 | 3.059 |
| heldout | 0 | 0 | - | - | - | - | - | 0 | 0 | 0 | - |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| train/borderless | 14 | 0 | 11.0 | 12.071 | 0.1 | 0.1 | 0.1875 | 0 | 0 | 0 | 3.002 |
| train/form | 14 | 0 | 2.5 | 3.429 | 0.3 | 0.4 | 0.3643 | 0 | 0 | 0 | 1.899 |
| train/form-mobile | 10 | 0 | 4.5 | 3.9 | 0.333 | 0.5 | 0.3833 | 0 | 0 | 0 | 1.459 |
| train/grid | 14 | 0 | 0.0 | 0.143 | 0.2 | 0.2 | 0.0417 | 0 | 0 | 0 | 2.28 |
| train/grid-mobile | 10 | 0 | 0.0 | 3.2 | 0.167 | 0.167 | 0.0685 | 0 | 0 | 0 | 2.043 |
| train/landing | 14 | 0 | 3.0 | 2.643 | 0.2 | 0.2 | 0.1047 | 0 | 0 | 0 | 2.389 |
| train/landing-mobile | 10 | 0 | 5.5 | 3.7 | 0.0 | 0.167 | 0.0855 | 0 | 0 | 0 | 1.622 |
| train/settings | 14 | 0 | 0.0 | 0.143 | 0.0 | 0.2 | 0.0444 | 0 | 0 | 0 | 2.167 |
| train/table | 14 | 0 | 37.5 | 56.643 | 0.3 | 0.3 | 0.1621 | 0 | 0 | 0 | 3.736 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| train/mutation | 78 | 0 | 4.0 | 11.705 | 0.179 | 0.244 | - | 0 | 0 | 0 | 3.048 |
| train/rasterizer | 27 | 0 | 4 | 9.111 | - | - | 0.1871 | 0 | 0 | 0 | 3.266 |
| train/rerender | 9 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 2.059 |

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | UNKNOWN |
| recall_heldout>0_and>=baseline | UNKNOWN |
| review_rate_noise<10% | FAIL |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | UNKNOWN |
| no_errors_or_fatal | PASS |

Recall baseline (heldout): 0.143. Long-page (>= 4000 px) max runtime (min of 2 runs): None s. Load average before/after: [31.0, 27.1]

## Mode: maps (OK)

Command: `pixel-perfect diff {design} {shot} --design-map {design_map} --shot-map {shot_map}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 114 | 0 | 0.0 | 0.114 | 1.0 | 1.0 | 0.0219 | 0 | 0 | 0 | 2.784 |
| train | 114 | 0 | 0.0 | 0.114 | 1.0 | 1.0 | 0.0219 | 0 | 0 | 0 | 2.784 |
| heldout | 0 | 0 | - | - | - | - | - | 0 | 0 | 0 | - |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| train/borderless | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 1.923 |
| train/form | 14 | 0 | 0.0 | 0.214 | 1.0 | 1.0 | 0.0286 | 0 | 0 | 0 | 1.839 |
| train/form-mobile | 10 | 0 | 0.0 | 0.2 | 1.0 | 1.0 | 0.0417 | 0 | 0 | 0 | 1.289 |
| train/grid | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 1.864 |
| train/grid-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 1.737 |
| train/landing | 14 | 0 | 1.0 | 0.571 | 1.0 | 1.0 | 0.0756 | 0 | 0 | 0 | 1.818 |
| train/landing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0658 | 0 | 0 | 0 | 1.327 |
| train/settings | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0778 | 0 | 0 | 0 | 1.792 |
| train/table | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.005 | 0 | 0 | 0 | 4.712 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| train/mutation | 78 | 0 | 0.0 | 0.115 | 1.0 | 1.0 | - | 0 | 0 | 0 | 2.663 |
| train/rasterizer | 27 | 0 | 0 | 0.148 | - | - | 0.0291 | 0 | 0 | 0 | 3.954 |
| train/rerender | 9 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 2.411 |

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | UNKNOWN |
| recall_heldout>0_and>=baseline | UNKNOWN |
| review_rate_noise<10% | PASS |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | UNKNOWN |
| no_errors_or_fatal | PASS |

Recall baseline (heldout): 0.929. Long-page (>= 4000 px) max runtime (min of 2 runs): None s. Load average before/after: [24.8, 22.0]
