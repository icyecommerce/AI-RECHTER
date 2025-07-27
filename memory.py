import os
import json
from datetime import datetime
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
USE_SUPABASE = SUPABASE_URL and SUPABASE_KEY

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

def get_user_file(user_id):
    return os.path.join(DATA_FOLDER, f"{user_id}.json")

def save_message(user_id, role, content):
    if USE_SUPABASE:
        try:
            payload = {
                "user_id": user_id,
                "role": role,
                "message": content,
                "timestamp": datetime.now().isoformat()  # 🔧 FIXED: string ipv datetime
            }

            res = requests.post(
                f"{SUPABASE_URL}/rest/v1/memory",  # ✅ let op: kleine letters 'memory'
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal"
                },
                json=payload
            )

            if res.status_code >= 300:
                print("⚠️ Supabase fout:", res.json(), "— fallback naar JSON")
                save_message_local(user_id, role, content)
        except Exception as e:
            print("⚠️ Supabase exception:", str(e), "— fallback naar JSON")
            save_message_local(user_id, role, content)
    else:
        save_message_local(user_id, role, content)

def save_message_local(user_id, role, content):
    filepath = get_user_file(user_id)
    convo = load_conversation(user_id)
    convo.append({"role": role, "content": content})
    with open(filepath, "w") as f:
        json.dump(convo, f)

def load_conversation(user_id):
    filepath = get_user_file(user_id)
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)
