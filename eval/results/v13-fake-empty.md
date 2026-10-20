# Scoreboard: v13-fake-empty

Corpus sha256 `52fcba52b238ef2515259e79ff2edde091eecdc7d35c0c6e075761c62d94bfef`. SYNTHETIC PROXY corpus (design = Chromium DPR2 downscaled; no real Figma pairs yet). Split: all

## Mode: maps (OK)

Command: `python eval/fakes/empty.py {design} {shot} --design-map {design_map} --shot-map {shot_map}`

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 243 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.05 |
| train | 171 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.039 |
| heldout | 72 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.058 |

### Per page kind

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/article | 17 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.064 |
| heldout/dark | 17 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.056 |
| heldout/dynamic | 11 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.059 |
| heldout/pricing | 17 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.05 |
| heldout/pricing-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.042 |
| train/borderless | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.041 |
| train/form | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.047 |
| train/form-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.037 |
| train/grid | 17 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.033 |
| train/grid-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.034 |
| train/landing | 17 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.033 |
| train/landing-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.034 |
| train/membership | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.034 |
| train/membership-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.033 |
| train/plans | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.034 |
| train/plans-mobile | 10 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.038 |
| train/settings | 17 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.036 |
| train/table | 14 | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 0.034 |

### Per pair kind (mutation, rasterizer noise, rerender, dynamic-content, replay)

| group | pairs | errors | median_false_deltas | mean_false_deltas | recall | recall_incl_review | review_rate_noise | rerender_confident_deltas | dynamic_deltas | determinism_failures | p95_runtime_s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| heldout/dynamic-content | 1 | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0.059 |
| heldout/mutation | 42 | 0 | 0.0 | 0 | 0.0 | 0.0 | - | 0 | 0 | 0 | 0.057 |
| heldout/rasterizer | 15 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.065 |
| heldout/replay | 9 | 0 | 0 | 0 | 0.0 | 0.0 | - | 0 | 0 | 0 | 0.048 |
| heldout/rerender | 5 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.062 |
| train/mutation | 110 | 0 | 0.0 | 0 | 0.0 | 0.0 | - | 0 | 0 | 0 | 0.039 |
| train/rasterizer | 39 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.039 |
| train/replay | 9 | 0 | 0 | 0 | 0.0 | 0.0 | - | 0 | 0 | 0 | 0.034 |
| train/rerender | 13 | 0 | 0 | 0 | - | - | 0.0 | 0 | 0 | 0 | 0.041 |

### Replay

| page | stable_ids | no_ghost | converged | B ids shot_0 | B ids shot_1 |
|---|---|---|---|---|---|
| article | False | True | True | [] | [] |
| dark | False | True | True | [] | [] |
| grid | False | True | True | [] | [] |
| landing | False | True | True | [] | [] |
| pricing | False | True | True | [] | [] |
| settings | False | True | True | [] | [] |

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
| replay_stable_ids | FAIL |

Recall baseline (heldout): 0.929. Long-page (>= 4000 px) max runtime (min of 2 runs): 0.025 s. Load average before/after: [13.0, 12.7]
