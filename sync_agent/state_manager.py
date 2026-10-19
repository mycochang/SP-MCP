import json
import os
import hashlib
from datetime import datetime, date

STATE_FILE = "sync_state.json"

class StateManager:
    def __init__(self, state_dir):
        self.state_path = os.path.join(state_dir, STATE_FILE)
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_path):
            with open(self.state_path, 'r') as f:
                return json.load(f)
        return {
            "last_daily_sync": None,
            "last_weekly_sync": None,
            "gcal_hash_daily": "",
            "gcal_hash_weekly": ""
        }

    def _save_state(self):
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=2)

    def should_run_daily(self):
        # Logic: Run if not run today
        if not self.state["last_daily_sync"]:
            return True
        last_run_date = self.state["last_daily_sync"].split("T")[0]
        today_date = date.today().isoformat()
        return last_run_date != today_date

    def update_daily_run(self, new_hash):
        self.state["last_daily_sync"] = datetime.now().isoformat()
        self.state["gcal_hash_daily"] = new_hash
        self._save_state()

    def check_hash_diff(self, new_data, mode="daily"):
        # Create a stable hash of the event IDs and update times
        stable_string = "".join(sorted([f"{e['id']}:{e.get('updated','')}" for e in new_data]))
        new_hash = hashlib.md5(stable_string.encode()).hexdigest()
        
        old_hash = self.state.get(f"gcal_hash_{mode}", "")
        return new_hash != old_hash, new_hash
