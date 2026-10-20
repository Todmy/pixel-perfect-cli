# Scoreboard: v13-fake-renumber

Corpus sha256 `52fcba52b238ef2515259e79ff2edde091eecdc7d35c0c6e075761c62d94bfef`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: all

## Mode: maps (OK)

Command: `python eval/fakes/renumber.py {design} {shot} --design-map {design_map} --shot-map {shot_map}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 243 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.096 |
| train | 171 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.091 |
| heldout | 72 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.102 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.081 |
| heldout/dark | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.111 |
| heldout/dynamic | 11 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.109 |
| heldout/pricing | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.086 |
| heldout/pricing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.103 |
| train/borderless | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.128 |
| train/form | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.085 |
| train/form-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.073 |
| train/grid | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.083 |
| train/grid-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.084 |
| train/landing | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.098 |
| train/landing-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.112 |
| train/membership | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.074 |
| train/membership-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.059 |
| train/plans | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.055 |
| train/plans-mobile | 10 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.08 |
| train/settings | 17 | 0 | 0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.096 |
| train/table | 14 | 0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | 0 | 0 | 0 | 0.085 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content, replay)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0.086 |
| heldout/mutation | 42 | 0 | 0.0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.103 |
| heldout/rasterizer | 15 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.098 |
| heldout/replay | 9 | 0 | 0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.111 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.081 |
| train/mutation | 110 | 0 | 0.0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.096 |
| train/rasterizer | 39 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.086 |
| train/replay | 9 | 0 | 0 | 0 | 1.0 | 1.0 | - | 0 | 0 | 0 | 0.096 |
| train/rerender | 13 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.087 |

### Replay

| page | stable_ids | no_ghost | converged | B ids shot_0 | B ids shot_1 |
|---|---|---|---|---|---|
| article | False | True | True | ['delta-1'] | ['delta-0'] |
| dark | False | True | True | ['delta-1'] | ['delta-0'] |
| grid | False | True | True | ['delta-1'] | ['delta-0'] |
| landing | False | True | True | ['delta-1'] | ['delta-0'] |
| pricing | False | True | True | ['delta-1'] | ['delta-0'] |
| settings | False | True | True | ['delta-1'] | ['delta-0'] |

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
| replay_stable_ids | FAIL |

Recall baseline (heldout): 0.929. Long-page (>= 4000 px) max runtime (min of 2 runs): 0.045 s. Load average before/after: [13.2, 13.0]
