# Calibration log (T7, 2026-10-19)

Corpus: SYNTHETIC PROXY (oracle v1.1/v1.2). Iterated on `--split train` only; held-out scored once at the end (`eval/results/t7-heldout.md`).
Columns: median / mean false deltas per pair, recall (confident deltas), review rate on noise pairs (review items / elements), errors.

## Numeric constants

No existing constant changed value. Two were added:

| constant | value | why |
|---|---|---|
| `DPRS` (`__init__.py`) | 1, 1.5, 2, 3, 4 and their inverses | without maps, a design/shot width ratio is accepted as DPR only if it is one of these; with maps the ratio comes from `dpr` |
| `NUM` (`structure.py`) | floats in style values rounded to 2 decimals | `33.599998px` (float32 in WebKit) vs `33.6px` |

`APPEARANCE_SURE` (0.05) no longer applies in maps mode (pixel-only evidence there is always review); pixels mode still uses it.

## Iterations (train split)

| iter | change | maps median / mean / recall / review_noise / errors | pixels median / mean / recall / review_noise / errors |
|---|---|---|---|
| 0 | baseline (fd5506e = cf5d83d src) | 0.0 / 13.824 / 0.859 / 0.1539 / 6 | 2.0 / 13.648 / 0.179 / 0.28 / 6 |
| 1 | F6 height; style value normalization; glyph-advance width; end-anchored gap; ink-shift align; margin and sibling-align attribution | 0.0 / 0.746 / 0.987 / 0.0184 / 0 | 2.5 / 13.386 / 0.179 / 0.2898 / 0 |
| 2 | maps pixel-only appearance -> review; row end/center anchors; size consequences (layout parent, stretched row sibling, added/removed child) | 0.0 / 0.167 / 0.987 / 0.0219 / 0 | - |
| 3 | row cross-axis align reported on the parent; moves after an added/removed sibling dropped; page size delta uses PX_TOL + SIZE_REL_TOL | 0.0 / 0.114 / 1.0 / 0.0219 / 0 | - |
| px1 | pixels: same-height width change of an ink leaf is not a resize | - | 2.5 / 10.158 / 0.179 / 0.3392 / 0 |
| px2 | pixels: and not a review item either | 0.0 / 0.114 / 1.0 / 0.0219 / 0 | 2.5 / 10.167 / 0.179 / 0.1403 / 0 |

Pixels median rises 2.0 -> 2.5 only because the 6 former error pairs are now scored. px2 costs recall_incl_review 0.269 -> 0.244 (two mutations that were found only in review).

## What the noise was (maps mode, train rasterizer pairs, iteration 0)

Found by tallying delta types per pair (not guessed):

- 545 of 625 confident false deltas: `appearance` with `font-family` only, WebKit serializes `-apple-system, Helvetica Neue` without quotes. Plus `line-height` `33.599998px` vs `33.6px`. Fix: normalize values when a map is read.
- Firefox: inline text boxes 3-5 px wider (glyph advances) -> `size`, and the right-aligned sibling after it -> `gap`. Fix: a text leaf with the same text and style that only changed width is not resized; a gap is anchored if the child keeps its distance to the row's right edge.
- 312 review items: `appearance` on text leaves with the same text and style (glyph rasterization). Fix: for those leaves compare where the ink lines sit in the box (left, center, right edge per line). A move of all three is an `align` delta (text-align, which the map does not carry). Anything else is dropped. This also found the text-align mutations that were missed before.

## Known ceilings

- Text styles the map does not carry (font-style, text-decoration, text-transform) on an unchanged text leaf are no longer flagged in maps mode. Capturing `text-align`, `font-style` and `text-decoration-line` in `capture.STYLES` would close this (outside T7 scope: changes capture output).
- Remaining train false deltas: WebKit `<select>` UA style (border-radius 8 -> 5px, padding dropped) and one hero `h1` that wraps to one line in WebKit/Firefox. Both are real rendering differences from the design engine.
- Ancestry for consequence rules is read from the id prefix (DOM CSS paths). A Figma-node adapter needs the tree instead.

## Held-out (single run, `t7-heldout`)

| mode | median false | mean false | recall | review_rate_noise | errors |
|---|---|---|---|---|---|
| maps (baseline) | 0 | 10.651 | 0.929 | 0.2819 | 0 |
| maps (T7) | 0 | 0.603 | 1.0 | 0.1076 | 0 |
| pixels (baseline) | 6 | 12.063 | 0.143 | 0.4661 | 0 |
| pixels (T7) | 3 | 8.952 | 0.143 | 0.1912 | 0 |

Maps review rate on held-out noise is 10.8% (train 2.2%): 86 of the 108 items come from two pairs, `pricing/noise-chromium` and `pricing-m/noise-chromium` (43 each). Not inspected, so held-out stays unseen. It needs a new train-side case of that shape before anyone fixes it.

# T20: maps review noise on pricing-shaped pages (2026-10-20, train only)

Corpus: oracle v1.3. Command: `uv run python -m eval.score --mode maps --split train --jobs 8 --label t20-*`. Per-page column is maps review_rate_noise (review items / elements over the page's 3 rasterizer noise pairs).

## What the noise was

Tallied review items per element on the noise pairs (not guessed): plans/noise-chromium had 36 review items, 32 of them `unexplained` pixel regions on the three `div.cost` boxes (`€0`, `€12`, `€39`), one per glyph fragment. `div.cost` holds its own text and an `<em>` child (`€12<em> / user / mo</em>`). `causes()` covered only leaves and moved boxes, so the glyph pixels of a box with its own text and a child were never judged and fell through to `unexplained`, although `look()` had already compared that text and style.

Fix: a matched box with its own text is covered like a leaf. A changed text or style still reports through `look()`.

| iter | change | plans | plans-m | membership | membership-m | landing | settings | overall | median / mean false | recall | replay_stable_ids / determinism / errors |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | baseline (de3068c) | 0.1395 | 0.1481 | 0.0694 | 0.0746 | 0.0756 | 0.0778 | 0.053 | 0 / 0.444 | 1.0 | PASS / PASS / 0 |
| 1 | cover boxes with their own text | 0.0407 | 0.0432 | 0.0590 | 0.0634 | 0.0756 | 0.0778 | 0.0319 | 0 / 0.444 | 1.0 | PASS / PASS / 0 |

Remaining items on plans and membership: antialiased rounded corners of tinted or dark cards (`div.tier.hot`, `div.card.dark`), 2-6 per pair. Not changed: every page is under 0.08 and a corner rule would need its own train evidence.
