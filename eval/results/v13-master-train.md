# Scoreboard: v13-master-train

Corpus sha256 `52fcba52b238ef2515259e79ff2edde091eecdc7d35c0c6e075761c62d94bfef`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: train

## Mode: pixels (OK)

Command: `pixel-perfect diff {design} {shot}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 171 | 0 | 4 | 8.444 | 0.235 | 0.294 | 0.1438 | 0 | 0 | 0 | 4.625 |
| train | 171 | 0 | 4 | 8.444 | 0.235 | 0.294 | 0.1438 | 0 | 0 | 0 | 4.625 |
| heldout | 0 | 0 | - | - | - | - | - | 0 | 0 | 0 | - |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| train/borderless | 14 | 0 | 11.0 | 12.071 | 0.1 | 0.1 | 0.1875 | 0 | 0 | 0 | 6.952 |
| train/form | 14 | 0 | 2.5 | 3.429 | 0.3 | 0.4 | 0.3643 | 0 | 0 | 0 | 2.186 |
| train/form-mobile | 10 | 0 | 4.5 | 3.9 | 0.333 | 0.5 | 0.3833 | 0 | 0 | 0 | 1.728 |
| train/grid | 17 | 0 | 0 | 0.118 | 0.231 | 0.231 | 0.0417 | 0 | 0 | 0 | 2.101 |
| train/grid-mobile | 10 | 0 | 0.0 | 3.2 | 0.167 | 0.167 | 0.0685 | 0 | 0 | 0 | 1.86 |
| train/landing | 17 | 0 | 0 | 2.176 | 0.154 | 0.154 | 0.1047 | 0 | 0 | 0 | 2.269 |
| train/landing-mobile | 10 | 0 | 5.5 | 3.7 | 0.0 | 0.167 | 0.0855 | 0 | 0 | 0 | 1.416 |
| train/membership | 14 | 0 | 5.0 | 6 | 0.3 | 0.4 | 0.0938 | 0 | 0 | 0 | 3.349 |
| train/membership-mobile | 10 | 0 | 5.0 | 7 | 0.333 | 0.333 | 0.0746 | 0 | 0 | 0 | 3.009 |
| train/plans | 14 | 0 | 2.5 | 4.357 | 0.4 | 0.4 | 0.2035 | 0 | 0 | 0 | 5.601 |
| train/plans-mobile | 10 | 0 | 8.0 | 7 | 0.667 | 0.667 | 0.2068 | 0 | 0 | 0 | 3.595 |
| train/settings | 17 | 0 | 0 | 0.118 | 0.0 | 0.231 | 0.0444 | 0 | 0 | 0 | 2.078 |
| train/table | 14 | 0 | 37.5 | 56.643 | 0.3 | 0.3 | 0.1621 | 0 | 0 | 0 | 3.575 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content, replay)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| train/mutation | 110 | 0 | 5.0 | 10.291 | 0.245 | 0.3 | - | 0 | 0 | 0 | 5.152 |
| train/rasterizer | 39 | 0 | 4 | 8 | - | - | 0.1917 | 0 | 0 | 0 | 5.182 |
| train/replay | 9 | 0 | 0 | 0 | 0.111 | 0.222 | - | 0 | 0 | 0 | 2.313 |
| train/rerender | 13 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 2.927 |

### Replay

| page | stable_ids | no_ghost | converged | B ids shot_0 | B ids shot_1 |
|---|---|---|---|---|---|
| grid | False | True | True | [] | [] |
| landing | False | True | True | [] | [] |
| settings | False | True | True | [] | [] |

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
| replay_stable_ids | FAIL |

Recall baseline (heldout): 0.143. Long-page (>= 4000 px) max runtime (min of 2 runs): None s. Load average before/after: [24.0, 21.9]

## Mode: maps (OK)

Command: `pixel-perfect diff {design} {shot} --design-map {design_map} --shot-map {shot_map}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 171 | 0 | 0 | 0.444 | 1.0 | 1.0 | 0.053 | 0 | 0 | 0 | 1.759 |
| train | 171 | 0 | 0 | 0.444 | 1.0 | 1.0 | 0.053 | 0 | 0 | 0 | 1.759 |
| heldout | 0 | 0 | - | - | - | - | - | 0 | 0 | 0 | - |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| train/borderless | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 2.741 |
| train/form | 14 | 0 | 0.0 | 0.214 | 1.0 | 1.0 | 0.0286 | 0 | 0 | 0 | 1.566 |
| train/form-mobile | 10 | 0 | 0.0 | 0.2 | 1.0 | 1.0 | 0.0417 | 0 | 0 | 0 | 1.22 |
| train/grid | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 1.644 |
| train/grid-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 1.511 |
| train/landing | 17 | 0 | 0 | 0.471 | 1.0 | 1.0 | 0.0756 | 0 | 0 | 0 | 1.819 |
| train/landing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0658 | 0 | 0 | 0 | 1.168 |
| train/membership | 14 | 0 | 0.0 | 1 | 1.0 | 1.0 | 0.0694 | 0 | 0 | 0 | 1.708 |
| train/membership-mobile | 10 | 0 | 0.5 | 1.4 | 1.0 | 1.0 | 0.0746 | 0 | 0 | 0 | 1.38 |
| train/plans | 14 | 0 | 0.0 | 1.429 | 1.0 | 1.0 | 0.1395 | 0 | 0 | 0 | 1.551 |
| train/plans-mobile | 10 | 0 | 1.0 | 1.5 | 1.0 | 1.0 | 0.1481 | 0 | 0 | 0 | 1.318 |
| train/settings | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0778 | 0 | 0 | 0 | 1.468 |
| train/table | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.005 | 0 | 0 | 0 | 1.775 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content, replay)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| train/mutation | 110 | 0 | 0.0 | 0.436 | 1.0 | 1.0 | - | 0 | 0 | 0 | 1.767 |
| train/rasterizer | 39 | 0 | 0 | 0.718 | - | - | 0.0706 | 0 | 0 | 0 | 1.819 |
| train/replay | 9 | 0 | 0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 1.744 |
| train/rerender | 13 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 1.652 |

### Replay

| page | stable_ids | no_ghost | converged | B ids shot_0 | B ids shot_1 |
|---|---|---|---|---|---|
| grid | True | True | True | ['body>div.wrap>div.cards>div.card:nth-of-type(5)>div.body:nth-of-type(2)>h3', 'body>div.wrap>div.cards>div.card:nth-of-type(5)>div.body:nth-of-type(2)>h3'] | ['body>div.wrap>div.cards>div.card:nth-of-type(5)>div.body:nth-of-type(2)>h3', 'body>div.wrap>div.cards>div.card:nth-of-type(5)>div.body:nth-of-type(2)>h3'] |
| landing | True | True | True | ['body>section.hero:nth-of-type(1)>div.copy:nth-of-type(1)>div.actions>a.btn.primary.start:nth-of-type(1)'] | ['body>section.hero:nth-of-type(1)>div.copy:nth-of-type(1)>div.actions>a.btn.primary.start:nth-of-type(1)'] |
| settings | True | True | True | ['body>div.layout>main.main>div.opt:nth-of-type(2)>div:nth-of-type(1)>b'] | ['body>div.layout>main.main>div.opt:nth-of-type(2)>div:nth-of-type(1)>b'] |

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
| replay_stable_ids | PASS |

Recall baseline (heldout): 0.929. Long-page (>= 4000 px) max runtime (min of 2 runs): None s. Load average before/after: [17.9, 16.0]
