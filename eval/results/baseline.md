# Scoreboard: baseline

Corpus sha256 `7d286320f428ff072441200a85c21d7ad05d4f0f21f0095c02aaf16f82e65c74`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: all

## Mode: pixels (OK)

Command: `pixel-perfect {design} {shot}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 177 | 6 | 4 | 13.152 | 0.1 | 0.2 | 0.3168 | 0 | 2 | 0 | 5.29 |
| train | 114 | 6 | 2.5 | 13.694 | 0.115 | 0.218 | 0.2459 | 0 | 0 | 0 | 2.691 |
| heldout | 63 | 0 | 6 | 12.222 | 0.071 | 0.167 | 0.4641 | 0 | 2 | 0 | 7.146 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 14 | 0 | 17.0 | 35.571 | 0.0 | 0.0 | 1.4821 | 0 | 0 | 0 | 8.911 |
| heldout/dark | 14 | 0 | 6.5 | 7.286 | 0.0 | 0.0 | 0.25 | 0 | 0 | 0 | 1.74 |
| heldout/dynamic | 11 | 0 | 5 | 6.364 | 0.333 | 0.333 | 0.3882 | 0 | 2 | 0 | 1.489 |
| heldout/pricing | 14 | 0 | 2.0 | 3.071 | 0.1 | 0.2 | 0.2857 | 0 | 0 | 0 | 2.632 |
| heldout/pricing-mobile | 10 | 0 | 5.5 | 5.7 | 0.0 | 0.5 | 0.1552 | 0 | 0 | 0 | 1.427 |
| train/borderless | 14 | 3 | 12 | 12.455 | 0.0 | 0.0 | 0.5625 | 0 | 0 | 0 | 1.519 |
| train/form | 14 | 0 | 2.5 | 4.929 | 0.2 | 0.4 | 0.4143 | 0 | 0 | 0 | 2.272 |
| train/form-mobile | 10 | 0 | 5.5 | 5.6 | 0.167 | 0.333 | 0.3833 | 0 | 0 | 0 | 1.325 |
| train/grid | 14 | 0 | 0.5 | 1 | 0.0 | 0.1 | 0.0801 | 0 | 0 | 0 | 2.021 |
| train/grid-mobile | 10 | 0 | 1.0 | 3.9 | 0.167 | 0.167 | 0.0856 | 0 | 0 | 0 | 3.153 |
| train/landing | 14 | 0 | 4.5 | 4.214 | 0.2 | 0.2 | 0.3256 | 0 | 0 | 0 | 3.154 |
| train/landing-mobile | 10 | 1 | 8 | 4.667 | 0.0 | 0.333 | 0.2829 | 0 | 0 | 0 | 1.689 |
| train/settings | 14 | 0 | 0.0 | 1.071 | 0.0 | 0.2 | 0.1 | 0 | 0 | 0 | 2.691 |
| train/table | 14 | 2 | 37.0 | 87.333 | 0.3 | 0.3 | 0.2954 | 0 | 0 | 0 | 3.099 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 3 | 3 | - | - | - | 0 | 2 | 0 | 1.489 |
| heldout/mutation | 42 | 0 | 6.0 | 12.762 | 0.071 | 0.167 | - | 0 | 0 | 0 | 7.232 |
| heldout/rasterizer | 15 | 0 | 8 | 15.4 | - | - | 0.6189 | 0 | 0 | 0 | 7.146 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 6.845 |
| train/mutation | 78 | 5 | 4 | 15.822 | 0.115 | 0.218 | - | 0 | 0 | 0 | 2.684 |
| train/rasterizer | 27 | 1 | 4.0 | 12.462 | - | - | 0.3388 | 0 | 0 | 0 | 3.043 |
| train/rerender | 9 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 1.911 |

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

Recall baseline (heldout): None. Long-page (>= 4000 px) max runtime (min of 2 runs): 7.529 s. Load average before/after: [16.7, 10.1]
