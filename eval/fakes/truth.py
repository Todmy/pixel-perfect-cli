"""Fake CLI (b): reads the pair's truth.json and emits exactly the planted mutations. Must pass delta/recall gates."""

import json
import sys
from pathlib import Path

DELTA_TYPE = {"margin": "gap", "font-size": "size", "radius": "appearance", "removed": "missing", "added": "extra"}

truth = json.loads((Path(sys.argv[2]).parent / "truth.json").read_text())
deltas = [{"type": DELTA_TYPE.get(m["type"], m["type"]), "id": m["selector"], "selector": m["selector"],
           "bbox": m["bbox"] or m["shot_bbox"], "expected": m["from"], "actual": m["to"],
           "confidence": "high", "source": "map"} for m in truth["mutations"]]
print(json.dumps({"status": "deltas" if deltas else "pass", "deltas": deltas, "review": []}, sort_keys=True))
sys.exit(1 if deltas else 0)
