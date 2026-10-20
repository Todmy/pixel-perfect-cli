# Scoreboard: final-d3fd12d

Corpus sha256 `52fcba52b238ef2515259e79ff2edde091eecdc7d35c0c6e075761c62d94bfef`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: all

## Mode: pixels (OK)

Command: `pixel-perfect diff {design} {shot}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 243 | 0 | 3 | 8.416 | 0.2 | 0.253 | 0.1543 | 0 | 2 | 0 | 38.78 |
| train | 171 | 0 | 4 | 8.444 | 0.235 | 0.294 | 0.1438 | 0 | 0 | 0 | 20.273 |
| heldout | 72 | 0 | 3.0 | 8.347 | 0.118 | 0.157 | 0.1912 | 0 | 2 | 0 | 60.11 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 17 | 0 | 9 | 27.235 | 0.077 | 0.077 | 0.631 | 0 | 0 | 0 | 63.175 |
| heldout/dark | 17 | 0 | 2 | 2.059 | 0.0 | 0.0 | 0.105 | 0 | 0 | 0 | 13.888 |
| heldout/dynamic | 11 | 0 | 3 | 3.455 | 0.333 | 0.333 | 0.1316 | 0 | 2 | 0 | 11.063 |
| heldout/pricing | 17 | 0 | 2 | 1.765 | 0.077 | 0.154 | 0.127 | 0 | 0 | 0 | 18.566 |
| heldout/pricing-mobile | 10 | 0 | 3.0 | 3.5 | 0.333 | 0.5 | 0.056 | 0 | 0 | 0 | 13.745 |
| train/borderless | 14 | 0 | 11.0 | 12.071 | 0.1 | 0.1 | 0.1875 | 0 | 0 | 0 | 14.977 |
| train/form | 14 | 0 | 2.5 | 3.429 | 0.3 | 0.4 | 0.3643 | 0 | 0 | 0 | 6.904 |
| train/form-mobile | 10 | 0 | 4.5 | 3.9 | 0.333 | 0.5 | 0.3833 | 0 | 0 | 0 | 3.97 |
| train/grid | 17 | 0 | 0 | 0.118 | 0.231 | 0.231 | 0.0417 | 0 | 0 | 0 | 13.258 |
| train/grid-mobile | 10 | 0 | 0.0 | 3.2 | 0.167 | 0.167 | 0.0685 | 0 | 0 | 0 | 22.515 |
| train/landing | 17 | 0 | 0 | 2.176 | 0.154 | 0.154 | 0.1047 | 0 | 0 | 0 | 16.954 |
| train/landing-mobile | 10 | 0 | 5.5 | 3.7 | 0.0 | 0.167 | 0.0855 | 0 | 0 | 0 | 5.377 |
| train/membership | 14 | 0 | 5.0 | 6 | 0.3 | 0.4 | 0.0938 | 0 | 0 | 0 | 13.369 |
| train/membership-mobile | 10 | 0 | 5.0 | 7 | 0.333 | 0.333 | 0.0746 | 0 | 0 | 0 | 15.4 |
| train/plans | 14 | 0 | 2.5 | 4.357 | 0.4 | 0.4 | 0.2035 | 0 | 0 | 0 | 22.844 |
| train/plans-mobile | 10 | 0 | 8.0 | 7 | 0.667 | 0.667 | 0.2068 | 0 | 0 | 0 | 15.025 |
| train/settings | 17 | 0 | 0 | 0.118 | 0.0 | 0.231 | 0.0444 | 0 | 0 | 0 | 21.412 |
| train/table | 14 | 0 | 37.5 | 56.643 | 0.3 | 0.3 | 0.1621 | 0 | 0 | 0 | 26.299 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content, replay)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 3 | 3 | - | - | - | 0 | 2 | 0 | 8.958 |
| heldout/mutation | 42 | 0 | 3.0 | 9.5 | 0.143 | 0.19 | - | 0 | 0 | 0 | 61.721 |
| heldout/rasterizer | 15 | 0 | 4 | 10.8 | - | - | 0.255 | 0 | 0 | 0 | 48.875 |
| heldout/replay | 9 | 0 | 2 | 4.111 | 0.0 | 0.0 | - | 0 | 0 | 0 | 60.11 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 41.196 |
| train/mutation | 110 | 0 | 5.0 | 10.291 | 0.245 | 0.3 | - | 0 | 0 | 0 | 21.297 |
| train/rasterizer | 39 | 0 | 4 | 8 | - | - | 0.1917 | 0 | 0 | 0 | 17.085 |
| train/replay | 9 | 0 | 0 | 0 | 0.111 | 0.222 | - | 0 | 0 | 0 | 21.412 |
| train/rerender | 13 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 15.368 |

### Replay

| page | stable_ids | no_ghost | converged | B ids shot_0 | B ids shot_1 |
|---|---|---|---|---|---|
| article | False | True | False | [] | [] |
| dark | False | True | True | [] | [] |
| grid | False | True | True | [] | [] |
| landing | False | True | True | [] | [] |
| pricing | False | True | True | [] | [] |
| settings | False | True | True | [] | [] |

### Gates

| gate | result |
|---|---|
| false_deltas_median_heldout<=1 | FAIL |
| recall_heldout>0_and>=baseline | FAIL |
| review_rate_noise<10% | FAIL |
| rerender_confident_deltas==0 | PASS |
| determinism_every_pair | PASS |
| runtime_long_page<5s | UNKNOWN |
| no_errors_or_fatal | PASS |
| replay_stable_ids | FAIL |

Recall baseline (heldout): 0.143. Long-page (>= 4000 px) max runtime (min of 2 runs): 27.59 s. Load average before/after: [110.6, 102.6]

## Mode: maps (OK)

Command: `pixel-perfect diff {design} {shot} --design-map {design_map} --shot-map {shot_map}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 243 | 0 | 0 | 0.469 | 1.0 | 1.0 | 0.0314 | 0 | 5 | 0 | 26.943 |
| train | 171 | 0 | 0 | 0.444 | 1.0 | 1.0 | 0.0319 | 0 | 0 | 0 | 11.549 |
| heldout | 72 | 0 | 0.0 | 0.528 | 1.0 | 1.0 | 0.0299 | 0 | 5 | 0 | 55.376 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 17 | 0 | 0 | 0.471 | 1.0 | 1.0 | 0.0238 | 0 | 0 | 0 | 67.603 |
| heldout/dark | 17 | 0 | 0 | 0.176 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 28.616 |
| heldout/dynamic | 11 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 5 | 0 | 11.012 |
| heldout/pricing | 17 | 0 | 0 | 0.647 | 1.0 | 1.0 | 0.0476 | 0 | 0 | 0 | 3.957 |
| heldout/pricing-mobile | 10 | 0 | 2.0 | 1.6 | 1.0 | 1.0 | 0.0603 | 0 | 0 | 0 | 3.964 |
| train/borderless | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 14.318 |
| train/form | 14 | 0 | 0.0 | 0.214 | 1.0 | 1.0 | 0.0286 | 0 | 0 | 0 | 7.213 |
| train/form-mobile | 10 | 0 | 0.0 | 0.2 | 1.0 | 1.0 | 0.0417 | 0 | 0 | 0 | 16.623 |
| train/grid | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 18.3 |
| train/grid-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 7.406 |
| train/landing | 17 | 0 | 0 | 0.471 | 1.0 | 1.0 | 0.0756 | 0 | 0 | 0 | 10.589 |
| train/landing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0658 | 0 | 0 | 0 | 8.686 |
| train/membership | 14 | 0 | 0.0 | 1 | 1.0 | 1.0 | 0.059 | 0 | 0 | 0 | 8.321 |
| train/membership-mobile | 10 | 0 | 0.5 | 1.4 | 1.0 | 1.0 | 0.0634 | 0 | 0 | 0 | 4.257 |
| train/plans | 14 | 0 | 0.0 | 1.429 | 1.0 | 1.0 | 0.0407 | 0 | 0 | 0 | 4.532 |
| train/plans-mobile | 10 | 0 | 1.0 | 1.5 | 1.0 | 1.0 | 0.0432 | 0 | 0 | 0 | 3.1 |
| train/settings | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0778 | 0 | 0 | 0 | 3.058 |
| train/table | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.005 | 0 | 0 | 0 | 5.702 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content, replay)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 0 | 0 | - | - | - | 0 | 4 | 0 | 10.087 |
| heldout/mutation | 42 | 0 | 0.0 | 0.571 | 1.0 | 1.0 | - | 0 | 1 | 0 | 44.579 |
| heldout/rasterizer | 15 | 0 | 0 | 0.933 | - | - | 0.0398 | 0 | 0 | 0 | 56.96 |
| heldout/replay | 9 | 0 | 0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 39.311 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 38.411 |
| train/mutation | 110 | 0 | 0.0 | 0.436 | 1.0 | 1.0 | - | 0 | 0 | 0 | 12.209 |
| train/rasterizer | 39 | 0 | 0 | 0.718 | - | - | 0.0425 | 0 | 0 | 0 | 9.066 |
| train/replay | 9 | 0 | 0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 10.589 |
| train/rerender | 13 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 12.167 |

### Replay

| page | stable_ids | no_ghost | converged | B ids shot_0 | B ids shot_1 |
|---|---|---|---|---|---|
| article | True | True | True | ['body>article.art>section.s4:nth-of-type(4)>blockquote'] | ['body>article.art>section.s4:nth-of-type(4)>blockquote'] |
| dark | True | True | True | ['body>div.wrap>div.kpis:nth-of-type(1)>div.kpi:nth-of-type(4)>div.v:nth-of-type(2)'] | ['body>div.wrap>div.kpis:nth-of-type(1)>div.kpi:nth-of-type(4)>div.v:nth-of-type(2)'] |
| grid | True | True | True | ['body>div.wrap>div.cards>div.card:nth-of-type(5)>div.body:nth-of-type(2)>h3', 'body>div.wrap>div.cards>div.card:nth-of-type(5)>div.body:nth-of-type(2)>h3'] | ['body>div.wrap>div.cards>div.card:nth-of-type(5)>div.body:nth-of-type(2)>h3', 'body>div.wrap>div.cards>div.card:nth-of-type(5)>div.body:nth-of-type(2)>h3'] |
| landing | True | True | True | ['body>section.hero:nth-of-type(1)>div.copy:nth-of-type(1)>div.actions>a.btn.primary.start:nth-of-type(1)'] | ['body>section.hero:nth-of-type(1)>div.copy:nth-of-type(1)>div.actions>a.btn.primary.start:nth-of-type(1)'] |
| pricing | True | True | True | ['body>section.plans:nth-of-type(2)>div.plan.pro:nth-of-type(2)>a.btn.primary'] | ['body>section.plans:nth-of-type(2)>div.plan.pro:nth-of-type(2)>a.btn.primary'] |
| settings | True | True | True | ['body>div.layout>main.main>div.opt:nth-of-type(2)>div:nth-of-type(1)>b'] | ['body>div.layout>main.main>div.opt:nth-of-type(2)>div:nth-of-type(1)>b'] |

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
| replay_stable_ids | PASS |

Recall baseline (heldout): 0.929. Long-page (>= 4000 px) max runtime (min of 2 runs): 6.779 s. Load average before/after: [604.8, 182.5]
