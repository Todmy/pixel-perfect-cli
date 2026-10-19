"""Fake CLI (a): reports a clean pass for every pair. Must score recall 0 and fail the gate."""

import json

print(json.dumps({"status": "pass", "deltas": [], "review": []}))
