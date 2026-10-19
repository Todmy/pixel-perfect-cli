# Scoreboard: fake-truth

Corpus sha256 `7dee141652f3bf94d41865f9037760e3e7a31e69183b22e96713b77989af028a`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: all

## Mode: pixels (OK)

Command: `python eval/fakes/truth.py {design} {shot}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 177 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.059 |
| train | 114 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.059 |
| heldout | 63 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.051 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.036 |
| heldout/dark | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.043 |
| heldout/dynamic | 11 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.088 |
| heldout/pricing | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.039 |
| heldout/pricing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.047 |
| train/borderless | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.046 |
| train/form | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.079 |
| train/form-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.073 |
| train/grid | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.056 |
| train/grid-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.062 |
| train/landing | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.041 |
| train/landing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.057 |
| train/settings | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.049 |
| train/table | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.053 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0.041 |
| heldout/mutation | 42 | 0 | 0.0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.05 |
| heldout/rasterizer | 15 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.088 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.048 |
| train/mutation | 78 | 0 | 0.0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.055 |
| train/rasterizer | 27 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.064 |
| train/rerender | 9 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.063 |

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | PASS |
| recall_heldout>0_and>=baseline | PASS |
| review_rate_noise<10% | PASS |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | PASS |
| no_errors_or_fatal | PASS |

Recall baseline (heldout): 0.143. Long-page (>= 4000 px) max runtime (min of 2 runs): 0.036 s. Load average before/after: [10.3, 10.7]

## Mode: maps (OK)

Command: `python eval/fakes/truth.py {design} {shot} --design-map {design_map} --shot-map {shot_map}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 177 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.048 |
| train | 114 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.049 |
| heldout | 63 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.044 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.044 |
| heldout/dark | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.04 |
| heldout/dynamic | 11 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.034 |
| heldout/pricing | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.051 |
| heldout/pricing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.044 |
| train/borderless | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.042 |
| train/form | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.047 |
| train/form-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.054 |
| train/grid | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.058 |
| train/grid-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.059 |
| train/landing | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.052 |
| train/landing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.037 |
| train/settings | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.034 |
| train/table | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.037 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0.027 |
| heldout/mutation | 42 | 0 | 0.0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.044 |
| heldout/rasterizer | 15 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.045 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.051 |
| train/mutation | 78 | 0 | 0.0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.05 |
| train/rasterizer | 27 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.044 |
| train/rerender | 9 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.058 |

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | PASS |
| recall_heldout>0_and>=baseline | PASS |
| review_rate_noise<10% | PASS |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | PASS |
| no_errors_or_fatal | PASS |

Recall baseline (heldout): 0.929. Long-page (>= 4000 px) max runtime (min of 2 runs): 0.038 s. Load average before/after: [10.7, 11.8]
