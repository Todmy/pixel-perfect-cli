# Scoreboard: t7-heldout

Corpus sha256 `7dee141652f3bf94d41865f9037760e3e7a31e69183b22e96713b77989af028a`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: heldout

## Mode: pixels (OK)

Command: `pixel-perfect diff {design} {shot}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 63 | 0 | 3 | 8.952 | 0.143 | 0.19 | 0.1912 | 0 | 2 | 0 | 11.847 |
| train | 0 | 0 | - | - | - | - | - | 0 | 0 | 0 | - |
| heldout | 63 | 0 | 3 | 8.952 | 0.143 | 0.19 | 0.1912 | 0 | 2 | 0 | 11.847 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 14 | 0 | 12.0 | 30.857 | 0.1 | 0.1 | 0.631 | 0 | 0 | 0 | 12.519 |
| heldout/dark | 14 | 0 | 1.5 | 2.143 | 0.0 | 0.0 | 0.105 | 0 | 0 | 0 | 3.138 |
| heldout/dynamic | 11 | 0 | 3 | 3.455 | 0.333 | 0.333 | 0.1316 | 0 | 2 | 0 | 2.151 |
| heldout/pricing | 14 | 0 | 2.0 | 2.071 | 0.1 | 0.2 | 0.127 | 0 | 0 | 0 | 2.291 |
| heldout/pricing-mobile | 10 | 0 | 3.0 | 3.5 | 0.333 | 0.5 | 0.056 | 0 | 0 | 0 | 1.453 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 3 | 3 | - | - | - | 0 | 2 | 0 | 1.822 |
| heldout/mutation | 42 | 0 | 3.0 | 9.5 | 0.143 | 0.19 | - | 0 | 0 | 0 | 11.847 |
| heldout/rasterizer | 15 | 0 | 4 | 10.8 | - | - | 0.255 | 0 | 0 | 0 | 11.87 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 5.8 |

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

Recall baseline (heldout): 0.143. Long-page (>= 4000 px) max runtime (min of 2 runs): 5.067 s. Load average before/after: [22.0, 15.9]

## Mode: maps (OK)

Command: `pixel-perfect diff {design} {shot} --design-map {design_map} --shot-map {shot_map}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 63 | 0 | 0 | 0.603 | 1.0 | 1.0 | 0.1076 | 0 | 5 | 0 | 8.724 |
| train | 0 | 0 | - | - | - | - | - | 0 | 0 | 0 | - |
| heldout | 63 | 0 | 0 | 0.603 | 1.0 | 1.0 | 0.1076 | 0 | 5 | 0 | 8.724 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 14 | 0 | 0.0 | 0.571 | 1.0 | 1.0 | 0.0238 | 0 | 0 | 0 | 9.289 |
| heldout/dark | 14 | 0 | 0.0 | 0.214 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 3.035 |
| heldout/dynamic | 11 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 5 | 0 | 1.793 |
| heldout/pricing | 14 | 0 | 0.0 | 0.786 | 1.0 | 1.0 | 0.2024 | 0 | 0 | 0 | 1.885 |
| heldout/pricing-mobile | 10 | 0 | 2.0 | 1.6 | 1.0 | 1.0 | 0.2284 | 0 | 0 | 0 | 1.632 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 0 | 0 | - | - | - | 0 | 4 | 0 | 1.57 |
| heldout/mutation | 42 | 0 | 0.0 | 0.571 | 1.0 | 1.0 | - | 0 | 1 | 0 | 8.724 |
| heldout/rasterizer | 15 | 0 | 0 | 0.933 | - | - | 0.1434 | 0 | 0 | 0 | 9.078 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 5.763 |

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | PASS |
| recall_heldout>0_and>=baseline | PASS |
| review_rate_noise<10% | FAIL |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | UNKNOWN |
| no_errors_or_fatal | PASS |

Recall baseline (heldout): 0.929. Long-page (>= 4000 px) max runtime (min of 2 runs): 2.833 s. Load average before/after: [20.7, 11.6]
