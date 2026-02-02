#!/usr/bin/env python3
import os
import json
import time
import sys
from pathlib import Path


def get_base_dir():
    if os.name == "nt":  # Windows
        data_dir = os.environ.get("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
    else:  # Linux/Mac
        data_dir = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))

    return Path(data_dir) / "super-productivity-mcp"


def run_diagnostic():
    base_dir = get_base_dir()
    command_dir = base_dir / "plugin_commands"
    response_dir = base_dir / "plugin_responses"

    print(f"🕵️  Diagnostic Stake: Bridge Check")
    print(f"📂 Base Dir: {base_dir}")

    if not command_dir.exists():
        print(f"❌ Command directory missing: {command_dir}")
        print("   -> Plugin likely never ran or failed initialization.")
        return

    print("✅ Directories exist.")

    # 1. Send Ping
    cmd_id = f"debug_{int(time.time())}"
    cmd_file = command_dir / f"{cmd_id}.json"

    payload = {"action": "probeAPI", "id": cmd_id, "timestamp": int(time.time() * 1000)}

    print(f"📤 Sending Probe... ({cmd_id})")
    try:
        with open(cmd_file, "w") as f:
            json.dump(payload, f)
    except Exception as e:
        print(f"❌ Failed to write command: {e}")
        return

    # 2. Wait for Response
    print("⏳ Waiting for Plugin (5s timeout)...")
    response_file = response_dir / f"{cmd_id}_response.json"

    start_time = time.time()
    while time.time() - start_time < 5:
        if response_file.exists():
            print("✅ Response Received!")
            try:
                with open(response_file, "r") as f:
                    data = json.load(f)
                print(f"📊 Plugin Status: Active")
                print(f"   Version: {data.get('result', {}).get('version', 'Unknown')}")
                print(f"   API Type: {data.get('result', {}).get('type')}")
                print(f"   Success: {data.get('success')}")

                # Cleanup
                response_file.unlink()
                return
            except Exception as e:
                print(f"⚠️  Response corrupted: {e}")
                return
        time.sleep(0.5)

    print("❌ Timeout: Plugin did not respond.")
    print("   -> Possible Causes:")
    print("      1. Super Productivity is not running.")
    print("      2. Plugin is not installed/active.")
    print("      3. Plugin crashed (check Console in App).")

    # Cleanup command if still there (Plugin didn't eat it)
    if cmd_file.exists():
        print("   -> Command file was NOT consumed.")
        cmd_file.unlink()
    else:
        print("   -> Command file WAS consumed, but no response wrote back.")


if __name__ == "__main__":
    run_diagnostic()
