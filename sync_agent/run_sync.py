import json
import os
import sys
from state_manager import StateManager
from logic_core import LogicCore

# Configuration
SP_PLUGIN_DIR = os.path.expanduser("~/.config/superProductivity/plugin_commands")
TEMP_GCAL_FILE = "sync_agent/temp_gcal.json"
TEMP_SP_FILE = "sync_agent/temp_sp_tasks.json"

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return json.load(f)

def write_sp_command(action, payload):
    if not os.path.exists(SP_PLUGIN_DIR):
        print(f"Error: SP Plugin directory not found: {SP_PLUGIN_DIR}")
        return

    command = {
        "action": action,
        "payload": payload,
        "id": f"sync_{action}_{os.urandom(4).hex()}",
        "timestamp": 123456789 # Placeholder, plugin might overwrite
    }
    
    # Write to a unique file
    fname = os.path.join(SP_PLUGIN_DIR, f"{command['id']}.json")
    with open(fname, 'w') as f:
        json.dump(command, f, indent=2)
    print(f"-> Queued SP Command: {action} ({fname})")

def main():
    print("--- Starting Agentic Sync ---")
    
    # 1. Load State
    state_mgr = StateManager("sync_agent")
    
    # 2. Load Data (Provided by the Agent)
    gcal_events = load_json(TEMP_GCAL_FILE)
    sp_tasks = load_json(TEMP_SP_FILE)
    
    if not gcal_events:
        print("No GCal events found in temp file. Aborting.")
        return

    # 3. Check Hash (Optimization)
    # We strip the events down to ID+Update for the hash check
    simple_events = [{"id": e.get("id"), "updated": e.get("updated")} for e in gcal_events]
    has_changed, new_hash = state_mgr.check_hash_diff(simple_events, mode="daily")
    
    if not has_changed:
        print("Hash match. No changes in Calendar since last run. Done.")
        # return # Uncomment to enable optimization

    # 4. Run Logic Diff
    logic = LogicCore()
    plan = logic.diff_events(gcal_events, sp_tasks)
    
    print(f"Plan: Create {len(plan['create'])}, Update {len(plan['update'])}")

    # 5. Execute (The Actor)
    # Circuit Breaker (bumped for initial sync)
    if len(plan['create']) > 50:
        print(f"SAFETY STOP: >50 items to create ({len(plan['create'])}). Manual approval required.")
        return

    for event in plan['create']:
        # Format: [CAL] HH:MM Title
        start_time = event.get('start', {}).get('dateTime', '')
        time_str = ""
        if start_time:
            # Parse ISO string to get HH:MM
            # simple slice assuming ISO format YYYY-MM-DDTHH:MM:SS...
            try:
                dt = start_time.split('T')[1][:5]
                time_str = f"{dt} "
            except:
                pass

        new_task = {
            "title": f"[CAL] {time_str}{event.get('summary', 'Untitled')}",
            "originalId": event.get("id"), 
            "notes": f"Event: {event.get('summary')}\nTime: {start_time}\n{event.get('description', '')}",
        }
        write_sp_command("addTask", new_task)
        
    for update in plan['update']:
        write_sp_command("updateTask", update)

    # 6. Update State
    state_mgr.update_daily_run(new_hash)
    print("--- Sync Complete ---")

if __name__ == "__main__":
    main()
