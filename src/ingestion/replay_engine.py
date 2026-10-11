import json
import os
from typing import List, Dict, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CRISIS_FILE = os.path.join(BASE_DIR, "data", "crisis_events.json")

def load_replay_scenarios() -> List[Dict]:
    if not os.path.exists(CRISIS_FILE):
        return []
    with open(CRISIS_FILE, "r") as f:
        return json.load(f)

def get_scenario_by_id(event_id: str) -> Optional[Dict]:
    scenarios = load_replay_scenarios()
    for s in scenarios:
        if s.get("event_id") == event_id:
            return s
    return None
