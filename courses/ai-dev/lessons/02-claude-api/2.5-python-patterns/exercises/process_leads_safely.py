# process_leads_safely.py
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_FILE = os.path.join(SCRIPT_DIR, 'leads.json')

# ...



def process_leads(filename):
    """Reads leads from a JSON file and processes them safely."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            leads = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    print("מתחיל עיבוד לידים...")
    for lead in leads:
        try:
            name = lead["name"]
            company = lead["company"]
            print(f"מעבד את {name} מ-{company}")
        except KeyError:
            print(f"שגיאה בעיבוד ליד: {lead.get('name', 'לא ידוע')}. שדה חסר.")

        # -----------------

    print("עיבוד לידים הושלם.")

# --- Main execution ---
process_leads(LEADS_FILE)