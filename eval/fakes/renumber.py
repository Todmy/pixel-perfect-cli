"""Fake CLI (c): like truth.py, but ids are list positions, so they renumber when a fix shifts the list. Must fail replay_stable_ids."""

import json
import sys
from pathlib import Path

truth = json.loads((Path(sys.argv[2]).parent / "truth.json").read_text())
deltas = [{"type": m["type"], "id": f"delta-{i}", "selector": m["selector"], "bbox": m["bbox"] or m["shot_bbox"],
           "confidence": "high", "source": "map"} for i, m in enumerate(truth["mutations"])]
print(json.dumps({"status": "deltas" if deltas else "pass", "deltas": deltas, "review": []}, sort_keys=True))
sys.exit(1 if deltas else 0)
