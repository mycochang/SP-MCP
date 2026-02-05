import os
import json
import asyncio
from datetime import datetime, timedelta

# Placeholder for the actual Agent/LLM client if needed
# from gemini_client import GeminiClient 

class LogicCore:
    def __init__(self):
        pass

    def _is_noise(self, event):
        """
        Determines if an event is 'noise' (Lunch, Catch-up, Free time)
        """
        title = event.get('summary', '')
        
        # 1. Emoji Filters (often used for routine/optional blocks)
        noise_emojis = ["🆓", "🍱", "📧", "🥪", "☕"]
        if any(emoji in title for emoji in noise_emojis):
            return True
            
        # 2. Keyword Filters
        noise_keywords = ["Lunch", "Catch Up", "Focus Time", "OOO", "Out of Office"]
        if any(kw.lower() in title.lower() for kw in noise_keywords):
            return True
            
        # 3. Availability Check (transparency = 'transparent' means 'Free')
        if event.get('transparency') == 'transparent':
            return True
            
        return False

    def diff_events(self, gcal_events, sp_tasks):
        """
        Strict logic diff with Noise Filtering.
        Returns: { "create": [], "update": [], "ambiguous": [] }
        """
        plan = {
            "create": [],
            "update": [],
            "ambiguous": [] 
        }

        # Index SP tasks by 'gcal_id' (if it exists in meta)
        sp_map = {t.get('originalId'): t for t in sp_tasks if t.get('originalId')}
        sp_title_map = {t['title'].lower(): t for t in sp_tasks}

        for event in gcal_events:
            # --- FILTERING LOGIC ---
            if self._is_noise(event):
                continue
            # -----------------------

            event_id = event['id']
            event_title = event.get('summary', '(No Title)')
            
            # 1. ID MATCH (The Gold Standard)
            if event_id in sp_map:
                continue 

            # 2. EXACT TITLE MATCH (The Silver Standard)
            if event_title.lower() in sp_title_map:
                plan['update'].append({
                    "taskId": sp_title_map[event_title.lower()]['id'],
                    "changes": {"originalId": event_id} 
                })
                continue

            # 3. NO MATCH -> CREATE
            plan['create'].append(event)

        return plan
