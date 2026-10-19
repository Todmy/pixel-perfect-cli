# Premortem: pixel-perfect-cli

> Horizon: 6 months (April 2027) · Generated: 2026-10-19 · Workflow: RunPremortem, 9 independent agents

## Context
- **What:** local deterministic CLI (`pixel-perfect design.png shot.png` → cause-level JSON deltas) for an AI agent fix loop; Level 0 for pixel-mcp.
- **Stakeholders:** solo founder-dev; Claude Code agents in the loop; later other devs.
- **Success:** agent converges a real page to its Figma frame with ≤1 false delta per screen; used on real projects.

## Frame
It is April 2027. pixel-perfect-cli failed. Below is why.

## Failures (agent-rated; all agents rated high/high, re-ranked below by shared root cause)

| ID | Failure | Root cause cluster |
|---|---|---|
| F1 | Figma-vs-browser noise floor far above cross-engine calibration → phantom deltas | never ran a real pair |
| F2 | XY-cut collapses on gradients, shadows, photos, overlap | never ran a real pair / image-only |
| F3 | `e0.2 gap 14→20` can't be mapped to code → agent edits wrong element | image-only |
| F4 | ~12 constants overfit to one 440x480 page; tests written from tuned outputs (Goodhart) | never ran a real pair |
| F5 | positional ids renumber, threshold-edge flips → oscillation, STUCK/REGRESSION misfire | image-only |
| F6 | inputs don't line up: frame height vs scroll height, 2x export, dynamic data, fonts not loaded → exit 12 or content deltas | no capture contract |
| F7 | two repos with overlapping Level 0, no project pulling → quiet stall | no user pull |
| F8 | O(N×M) pairing with per-cell resize → minutes per call on 1440x4000 | never ran a real pair |
| F9 | `review` becomes the default bucket → expensive non-deterministic VLM loop | no OCR / never ran a real pair |

Per-failure detail (story, warning signs, mitigation): see agent outputs summarized in Synthesis.

## Synthesis
- **Most likely:** the first real Figma pair produces 15-40 false deltas (F1+F2+F6), the agent chases them, trust dies in a day.
- **Most dangerous:** F3+F5: deltas are *correct but unactionable and unstable*, so the agent edits the wrong CSS, ids shift, and the loop leaves the page worse than it started while STUCK never fires. Damage lands in the user's codebase, silently.
- **Biggest hidden assumption:** that structure must be recovered from pixels. In Figma mode both sides already have a tree: the Figma node tree and the DOM (`getBoundingClientRect` + selector). XY-cut re-derives, badly, what is available for free. It is only needed for screenshot-vs-screenshot (mobile, image-only mode).

## Revised plan (owner: founder-dev)
1. **Real eval corpus before any feature (1 day).** 5 real Figma frames + live pages, hand-labelled true deltas, held-out split. Go/no-go metric: false deltas per screen ≤1. Synthetic exact-output asserts become invariants only (identical → 0, shift → 1 gap).
2. **Structure from sources, pixels as fallback (2 days).** Optional `--dom-map` (bbox, selector, source file) and Figma node tree; pair by node, ids = selector / node name. XY-cut stays for image-only mode.
3. **Capture contract (0.5 day).** Helper: viewport = frame width, DPR, `document.fonts.ready`, clip to frame height, mask selectors for dynamic content; `--crop-to-design` instead of hard exit 12.
4. **Perf budget (0.5 day).** ΔE mask once and slice; pairing candidates top-k by IoU; hard budget 5 s on 1440x4000, fallback to region-level output.
5. **Integration deadline.** pixel-mcp calls the CLI as its image-mode Level 0 within 14 days of first commit (by 2026-11-02), or the repo is archived.

## Pre-launch checklist
- [ ] 5 real pairs: median false deltas per screen ≤1, review rate <10%
- [ ] No-change rerun (same page, re-render): 0 deltas, identical JSON hash
- [ ] Replay test: one CSS change → delta set differs only in that element, ids stable
- [ ] 1440x4000 real page: full pipeline <5 s
- [ ] pixel-mcp invokes the CLI end to end on one real screen
