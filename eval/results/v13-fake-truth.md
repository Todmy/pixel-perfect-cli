# Scoreboard: v13-fake-truth

Corpus sha256 `52fcba52b238ef2515259e79ff2edde091eecdc7d35c0c6e075761c62d94bfef`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: all

## Mode: maps (OK)

Command: `python eval/fakes/truth.py {design} {shot} --design-map {design_map} --shot-map {shot_map}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 243 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.105 |
| train | 171 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.114 |
| heldout | 72 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.089 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.092 |
| heldout/dark | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.091 |
| heldout/dynamic | 11 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.071 |
| heldout/pricing | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.097 |
| heldout/pricing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.085 |
| train/borderless | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.088 |
| train/form | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.113 |
| train/form-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.119 |
| train/grid | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.158 |
| train/grid-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.125 |
| train/landing | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.143 |
| train/landing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.116 |
| train/membership | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.081 |
| train/membership-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.116 |
| train/plans | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.072 |
| train/plans-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.093 |
| train/settings | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.102 |
| train/table | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.083 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content, replay)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0.067 |
| heldout/mutation | 42 | 0 | 0.0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.084 |
| heldout/rasterizer | 15 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.092 |
| heldout/replay | 9 | 0 | 0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.094 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.08 |
| train/mutation | 110 | 0 | 0.0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.116 |
| train/rasterizer | 39 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.102 |
| train/replay | 9 | 0 | 0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.156 |
| train/rerender | 13 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.113 |

### Replay

| page | stable_ids | no_ghost | converged | B ids shot_0 | B ids shot_1 |
|---|---|---|---|---|---|
| article | True | True | True | ['body>article.art>section.s4:nth-of-type(4)>blockquote'] | ['body>article.art>section.s4:nth-of-type(4)>blockquote'] |
| dark | True | True | True | ['body>div.wrap>div.kpis:nth-of-type(1)>div.kpi:nth-of-type(4)>div.v:nth-of-type(2)'] | ['body>div.wrap>div.kpis:nth-of-type(1)>div.kpi:nth-of-type(4)>div.v:nth-of-type(2)'] |
| grid | True | True | True | ['body>div.wrap>div.cards>div.card:nth-of-type(5)>div.body:nth-of-type(2)>h3'] | ['body>div.wrap>div.cards>div.card:nth-of-type(5)>div.body:nth-of-type(2)>h3'] |
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
| runtime_long_page<5s | PASS |
| no_errors_or_fatal | PASS |
| replay_stable_ids | PASS |

Recall baseline (heldout): 0.929. Long-page (>= 4000 px) max runtime (min of 2 runs): 0.054 s. Load average before/after: [11.2, 13.2]
