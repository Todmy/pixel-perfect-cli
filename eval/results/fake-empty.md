# Scoreboard: fake-empty

Corpus sha256 `7d286320f428ff072441200a85c21d7ad05d4f0f21f0095c02aaf16f82e65c74`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: all

## Mode: pixels (OK)

Command: `python eval/fakes/empty.py {design} {shot}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 177 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.029 |
| train | 114 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.03 |
| heldout | 63 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.026 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.025 |
| heldout/dark | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.025 |
| heldout/dynamic | 11 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.027 |
| heldout/pricing | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.026 |
| heldout/pricing-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.025 |
| train/borderless | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.028 |
| train/form | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.026 |
| train/form-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.032 |
| train/grid | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.029 |
| train/grid-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.033 |
| train/landing | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.03 |
| train/landing-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.027 |
| train/settings | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.024 |
| train/table | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.023 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0.023 |
| heldout/mutation | 42 | 0 | 0.0 | 0 | 0.0 | 0.0 | - | 0 | 0 | 0 | 0.026 |
| heldout/rasterizer | 15 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.025 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.026 |
| train/mutation | 78 | 0 | 0.0 | 0 | 0.0 | 0.0 | - | 0 | 0 | 0 | 0.029 |
| train/rasterizer | 27 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.03 |
| train/rerender | 9 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.03 |

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | PASS |
| recall_heldout>0_and>=baseline | FAIL |
| review_rate_noise<10% | PASS |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | PASS |
| no_errors_or_fatal | PASS |

Recall baseline (heldout): 0.071. Long-page (>= 4000 px) max runtime (min of 2 runs): 0.025 s. Load average before/after: [10.1, 9.4]

## Mode: maps (OK)

Command: `python eval/fakes/empty.py {design} {shot} --design-map {design_map} --shot-map {shot_map}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 177 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.036 |
| train | 114 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.038 |
| heldout | 63 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.031 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.022 |
| heldout/dark | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.023 |
| heldout/dynamic | 11 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.023 |
| heldout/pricing | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.028 |
| heldout/pricing-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.035 |
| train/borderless | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.022 |
| train/form | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.022 |
| train/form-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.023 |
| train/grid | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.022 |
| train/grid-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.022 |
| train/landing | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.024 |
| train/landing-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.024 |
| train/settings | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.041 |
| train/table | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.035 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0.023 |
| heldout/mutation | 42 | 0 | 0.0 | 0 | 0.0 | 0.0 | - | 0 | 0 | 0 | 0.031 |
| heldout/rasterizer | 15 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.031 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.031 |
| train/mutation | 78 | 0 | 0.0 | 0 | 0.0 | 0.0 | - | 0 | 0 | 0 | 0.037 |
| train/rasterizer | 27 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.038 |
| train/rerender | 9 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.047 |

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | PASS |
| recall_heldout>0_and>=baseline | FAIL |
| review_rate_noise<10% | PASS |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | PASS |
| no_errors_or_fatal | PASS |

Recall baseline (heldout): 0.071. Long-page (>= 4000 px) max runtime (min of 2 runs): 0.021 s. Load average before/after: [9.4, 9.0]
