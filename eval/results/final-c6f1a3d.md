# Scoreboard: final-c6f1a3d

Corpus sha256 `7dee141652f3bf94d41865f9037760e3e7a31e69183b22e96713b77989af028a`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: all

## Mode: pixels (OK)

Command: `pixel-perfect diff {design} {shot}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 177 | 0 | 3 | 9.734 | 0.167 | 0.225 | 0.1558 | 0 | 2 | 0 | 9.124 |
| train | 114 | 0 | 2.5 | 10.167 | 0.179 | 0.244 | 0.1403 | 0 | 0 | 0 | 6.098 |
| heldout | 63 | 0 | 3 | 8.952 | 0.143 | 0.19 | 0.1912 | 0 | 2 | 0 | 11.196 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 14 | 0 | 12.0 | 30.857 | 0.1 | 0.1 | 0.631 | 0 | 0 | 0 | 11.512 |
| heldout/dark | 14 | 0 | 1.5 | 2.143 | 0.0 | 0.0 | 0.105 | 0 | 0 | 0 | 3.431 |
| heldout/dynamic | 11 | 0 | 3 | 3.455 | 0.333 | 0.333 | 0.1316 | 0 | 2 | 0 | 2.553 |
| heldout/pricing | 14 | 0 | 2.0 | 2.071 | 0.1 | 0.2 | 0.127 | 0 | 0 | 0 | 4.242 |
| heldout/pricing-mobile | 10 | 0 | 3.0 | 3.5 | 0.333 | 0.5 | 0.056 | 0 | 0 | 0 | 3.585 |
| train/borderless | 14 | 0 | 11.0 | 12.071 | 0.1 | 0.1 | 0.1875 | 0 | 0 | 0 | 3.841 |
| train/form | 14 | 0 | 2.5 | 3.429 | 0.3 | 0.4 | 0.3643 | 0 | 0 | 0 | 2.602 |
| train/form-mobile | 10 | 0 | 4.5 | 3.9 | 0.333 | 0.5 | 0.3833 | 0 | 0 | 0 | 1.611 |
| train/grid | 14 | 0 | 0.0 | 0.143 | 0.2 | 0.2 | 0.0417 | 0 | 0 | 0 | 1.965 |
| train/grid-mobile | 10 | 0 | 0.0 | 3.2 | 0.167 | 0.167 | 0.0685 | 0 | 0 | 0 | 2.237 |
| train/landing | 14 | 0 | 3.0 | 2.643 | 0.2 | 0.2 | 0.1047 | 0 | 0 | 0 | 2.264 |
| train/landing-mobile | 10 | 0 | 5.5 | 3.7 | 0.0 | 0.167 | 0.0855 | 0 | 0 | 0 | 2.392 |
| train/settings | 14 | 0 | 0.0 | 0.143 | 0.0 | 0.2 | 0.0444 | 0 | 0 | 0 | 4.505 |
| train/table | 14 | 0 | 37.5 | 56.643 | 0.3 | 0.3 | 0.1621 | 0 | 0 | 0 | 7.537 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 3 | 3 | - | - | - | 0 | 2 | 0 | 2.868 |
| heldout/mutation | 42 | 0 | 3.0 | 9.5 | 0.143 | 0.19 | - | 0 | 0 | 0 | 11.206 |
| heldout/rasterizer | 15 | 0 | 4 | 10.8 | - | - | 0.255 | 0 | 0 | 0 | 11.196 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 6.984 |
| train/mutation | 78 | 0 | 4.0 | 11.705 | 0.179 | 0.244 | - | 0 | 0 | 0 | 6.245 |
| train/rasterizer | 27 | 0 | 4 | 9.111 | - | - | 0.1871 | 0 | 0 | 0 | 7.255 |
| train/rerender | 9 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 4.384 |

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | FAIL |
| recall_heldout>0_and>=baseline | PASS |
| review_rate_noise<10% | FAIL |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | UNKNOWN |
| no_errors_or_fatal | PASS |

Recall baseline (heldout): 0.143. Long-page (>= 4000 px) max runtime (min of 2 runs): 10.58 s. Load average before/after: [76.2, 58.9]

## Mode: maps (OK)

Command: `pixel-perfect diff {design} {shot} --design-map {design_map} --shot-map {shot_map}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 177 | 0 | 0 | 0.288 | 1.0 | 1.0 | 0.048 | 0 | 5 | 0 | 10.437 |
| train | 114 | 0 | 0.0 | 0.114 | 1.0 | 1.0 | 0.0219 | 0 | 0 | 0 | 5.296 |
| heldout | 63 | 0 | 0 | 0.603 | 1.0 | 1.0 | 0.1076 | 0 | 5 | 0 | 11.71 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 14 | 0 | 0.0 | 0.571 | 1.0 | 1.0 | 0.0238 | 0 | 0 | 0 | 15.163 |
| heldout/dark | 14 | 0 | 0.0 | 0.214 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 3.782 |
| heldout/dynamic | 11 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 5 | 0 | 7.065 |
| heldout/pricing | 14 | 0 | 0.0 | 0.786 | 1.0 | 1.0 | 0.2024 | 0 | 0 | 0 | 2.302 |
| heldout/pricing-mobile | 10 | 0 | 2.0 | 1.6 | 1.0 | 1.0 | 0.2284 | 0 | 0 | 0 | 1.554 |
| train/borderless | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 6.738 |
| train/form | 14 | 0 | 0.0 | 0.214 | 1.0 | 1.0 | 0.0286 | 0 | 0 | 0 | 5.379 |
| train/form-mobile | 10 | 0 | 0.0 | 0.2 | 1.0 | 1.0 | 0.0417 | 0 | 0 | 0 | 2.893 |
| train/grid | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 5.545 |
| train/grid-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 4.881 |
| train/landing | 14 | 0 | 1.0 | 0.571 | 1.0 | 1.0 | 0.0756 | 0 | 0 | 0 | 3.361 |
| train/landing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0658 | 0 | 0 | 0 | 2.189 |
| train/settings | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0778 | 0 | 0 | 0 | 1.801 |
| train/table | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.005 | 0 | 0 | 0 | 2.415 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 0 | 0 | - | - | - | 0 | 4 | 0 | 6.975 |
| heldout/mutation | 42 | 0 | 0.0 | 0.571 | 1.0 | 1.0 | - | 0 | 1 | 0 | 11.71 |
| heldout/rasterizer | 15 | 0 | 0 | 0.933 | - | - | 0.1434 | 0 | 0 | 0 | 11.608 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 14.242 |
| train/mutation | 78 | 0 | 0.0 | 0.115 | 1.0 | 1.0 | - | 0 | 0 | 0 | 5.308 |
| train/rasterizer | 27 | 0 | 0 | 0.148 | - | - | 0.0291 | 0 | 0 | 0 | 5.267 |
| train/rerender | 9 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 5.545 |

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | PASS |
| recall_heldout>0_and>=baseline | PASS |
| review_rate_noise<10% | PASS |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | UNKNOWN |
| no_errors_or_fatal | PASS |

Recall baseline (heldout): 0.929. Long-page (>= 4000 px) max runtime (min of 2 runs): 4.235 s. Load average before/after: [54.3, 29.0]
