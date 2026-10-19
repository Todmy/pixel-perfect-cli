# Scoreboard: baseline

Corpus sha256 `7dee141652f3bf94d41865f9037760e3e7a31e69183b22e96713b77989af028a`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: all

## Mode: pixels (OK)

Command: `pixel-perfect diff {design} {shot}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 177 | 6 | 4 | 13.064 | 0.167 | 0.242 | 0.3405 | 0 | 2 | 0 | 7.92 |
| train | 114 | 6 | 2.0 | 13.648 | 0.179 | 0.269 | 0.28 | 0 | 0 | 0 | 4.903 |
| heldout | 63 | 0 | 6 | 12.063 | 0.143 | 0.19 | 0.4661 | 0 | 2 | 0 | 11.358 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 14 | 0 | 14.0 | 35 | 0.1 | 0.1 | 1.4821 | 0 | 0 | 0 | 12.469 |
| heldout/dark | 14 | 0 | 6.5 | 7.286 | 0.0 | 0.0 | 0.25 | 0 | 0 | 0 | 1.914 |
| heldout/dynamic | 11 | 0 | 5 | 6.364 | 0.333 | 0.333 | 0.3882 | 0 | 2 | 0 | 1.562 |
| heldout/pricing | 14 | 0 | 2.0 | 3.071 | 0.1 | 0.2 | 0.2937 | 0 | 0 | 0 | 4.407 |
| heldout/pricing-mobile | 10 | 0 | 5.5 | 5.5 | 0.333 | 0.5 | 0.1552 | 0 | 0 | 0 | 3.274 |
| train/borderless | 14 | 3 | 12 | 12.455 | 0.0 | 0.0 | 0.5625 | 0 | 0 | 0 | 3.69 |
| train/form | 14 | 0 | 2.5 | 4.857 | 0.3 | 0.5 | 0.6357 | 0 | 0 | 0 | 3.568 |
| train/form-mobile | 10 | 0 | 5.5 | 5.5 | 0.333 | 0.5 | 0.6417 | 0 | 0 | 0 | 2.688 |
| train/grid | 14 | 0 | 0.0 | 0.857 | 0.2 | 0.2 | 0.0801 | 0 | 0 | 0 | 3.915 |
| train/grid-mobile | 10 | 0 | 1.0 | 3.9 | 0.167 | 0.167 | 0.0856 | 0 | 0 | 0 | 4.795 |
| train/landing | 14 | 0 | 4.5 | 4.214 | 0.2 | 0.2 | 0.3256 | 0 | 0 | 0 | 3.825 |
| train/landing-mobile | 10 | 1 | 8 | 4.667 | 0.0 | 0.333 | 0.2829 | 0 | 0 | 0 | 2.792 |
| train/settings | 14 | 0 | 0.0 | 1.071 | 0.0 | 0.2 | 0.1 | 0 | 0 | 0 | 9.315 |
| train/table | 14 | 2 | 37.0 | 87.25 | 0.4 | 0.4 | 0.3102 | 0 | 0 | 0 | 4.903 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 3 | 3 | - | - | - | 0 | 2 | 0 | 1.777 |
| heldout/mutation | 42 | 0 | 6.0 | 12.524 | 0.143 | 0.19 | - | 0 | 0 | 0 | 11.23 |
| heldout/rasterizer | 15 | 0 | 8 | 15.4 | - | - | 0.6215 | 0 | 0 | 0 | 11.555 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 3.462 |
| train/mutation | 78 | 5 | 4 | 15.753 | 0.179 | 0.269 | - | 0 | 0 | 0 | 5.375 |
| train/rasterizer | 27 | 1 | 4.0 | 12.462 | - | - | 0.3857 | 0 | 0 | 0 | 4.201 |
| train/rerender | 9 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 8.344 |

### First errors

- `borderless/added`: 'aspect mismatch: design 1440x900, shot 1440x942'
- `borderless/margin`: 'aspect mismatch: design 1440x900, shot 1440x916'
- `borderless/padding`: 'aspect mismatch: design 1440x900, shot 1440x948'
- `landing-m/font-size`: 'aspect mismatch: design 390x1186, shot 390x1272'
- `table/margin`: 'aspect mismatch: design 1440x1201, shot 1440x1217'
- `table/noise-firefox`: 'aspect mismatch: design 1440x1201, shot 1440x1212'

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | FAIL |
| recall_heldout>0_and>=baseline | PASS |
| review_rate_noise<10% | FAIL |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | FAIL |
| no_errors_or_fatal | FAIL |

Recall baseline (heldout): None. Long-page (>= 4000 px) max runtime (min of 2 runs): 12.283 s. Load average before/after: [22.3, 63.1]

## Mode: maps (OK)

Command: `pixel-perfect diff {design} {shot} --design-map {design_map} --shot-map {shot_map}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 177 | 6 | 0 | 12.655 | 0.883 | 0.908 | 0.1955 | 0 | 16 | 0 | 3.775 |
| train | 114 | 6 | 0.0 | 13.824 | 0.859 | 0.885 | 0.1539 | 0 | 0 | 0 | 1.743 |
| heldout | 63 | 0 | 0 | 10.651 | 0.929 | 0.952 | 0.2819 | 0 | 16 | 0 | 4.809 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 14 | 0 | 2.0 | 9.571 | 1.0 | 1.0 | 0.2738 | 0 | 0 | 0 | 6.257 |
| heldout/dark | 14 | 0 | 0.0 | 3.571 | 0.9 | 1.0 | 0.135 | 0 | 0 | 0 | 2.392 |
| heldout/dynamic | 11 | 0 | 0 | 12.818 | 0.833 | 0.833 | 0.2434 | 0 | 16 | 0 | 1.603 |
| heldout/pricing | 14 | 0 | 0.0 | 9.857 | 0.9 | 0.9 | 0.3571 | 0 | 0 | 0 | 1.057 |
| heldout/pricing-mobile | 10 | 0 | 7.5 | 20.8 | 1.0 | 1.0 | 0.3578 | 0 | 0 | 0 | 0.728 |
| train/borderless | 14 | 3 | 0 | 3.091 | 0.6 | 0.6 | 0.1964 | 0 | 0 | 0 | 3.83 |
| train/form | 14 | 0 | 0.0 | 7.143 | 0.9 | 1.0 | 0.1857 | 0 | 0 | 0 | 1.566 |
| train/form-mobile | 10 | 0 | 0.0 | 5.7 | 1.0 | 1.0 | 0.175 | 0 | 0 | 0 | 0.998 |
| train/grid | 14 | 0 | 0.0 | 15.786 | 0.9 | 0.9 | 0.1987 | 0 | 0 | 0 | 1.414 |
| train/grid-mobile | 10 | 0 | 0.5 | 12.3 | 1.0 | 1.0 | 0.1849 | 0 | 0 | 0 | 1.095 |
| train/landing | 14 | 0 | 4.0 | 11.571 | 0.9 | 0.9 | 0.2267 | 0 | 0 | 0 | 1.892 |
| train/landing-mobile | 10 | 1 | 6 | 11.111 | 0.833 | 0.833 | 0.2039 | 0 | 0 | 0 | 1.079 |
| train/settings | 14 | 0 | 0.0 | 3.143 | 0.9 | 0.9 | 0.2167 | 0 | 0 | 0 | 1.616 |
| train/table | 14 | 2 | 2.5 | 54.333 | 0.8 | 0.9 | 0.0446 | 0 | 0 | 0 | 1.677 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 0 | 0 | - | - | - | 0 | 4 | 0 | 1.049 |
| heldout/mutation | 42 | 0 | 0.0 | 9.69 | 0.929 | 0.952 | - | 0 | 9 | 0 | 4.867 |
| heldout/rasterizer | 15 | 0 | 3 | 17.6 | - | - | 0.3758 | 0 | 3 | 0 | 4.539 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 4.543 |
| train/mutation | 78 | 5 | 0 | 11.89 | 0.859 | 0.885 | - | 0 | 0 | 0 | 1.677 |
| train/rasterizer | 27 | 1 | 3.0 | 24.038 | - | - | 0.212 | 0 | 0 | 0 | 2.534 |
| train/rerender | 9 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 1.755 |

### First errors

- `borderless/added`: 'aspect mismatch: design 1440x900, shot 1440x942'
- `borderless/margin`: 'aspect mismatch: design 1440x900, shot 1440x916'
- `borderless/padding`: 'aspect mismatch: design 1440x900, shot 1440x948'
- `landing-m/font-size`: 'aspect mismatch: design 390x1186, shot 390x1272'
- `table/margin`: 'aspect mismatch: design 1440x1201, shot 1440x1217'
- `table/noise-firefox`: 'aspect mismatch: design 1440x1201, shot 1440x1212'

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | PASS |
| recall_heldout>0_and>=baseline | PASS |
| review_rate_noise<10% | FAIL |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | FAIL |
| no_errors_or_fatal | FAIL |

Recall baseline (heldout): None. Long-page (>= 4000 px) max runtime (min of 2 runs): 6.257 s. Load average before/after: [63.1, 11.6]
