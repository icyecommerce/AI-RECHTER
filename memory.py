import os
import json
from datetime import datetime
from supabase import create_client

# 🔐 Supabase config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🗂️ JSON fallback folder
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

def get_user_file(user_id):
    return os.path.join(DATA_FOLDER, f"{user_id}.json")

def save_message(user_id, role, content):
    # 1. 🔁 Probeer Supabase
    if supabase:
        try:
            supabase.table("memory").insert({
                "user_id": user_id,
                "role": role,
                "message": content,
                "timestamp": datetime.utcnow()
            }).execute()
        except Exception as e:
            print(f"⚠️ Supabase fout: {e} — fallback naar JSON")

    # 2. 💾 Ook lokaal opslaan (fallback)
    filepath = get_user_file(user_id)
    convo = load_conversation(user_id)
    convo.append({"role": role, "content": content})
    with open(filepath, "w") as f:
        json.dump(convo, f)

def load_conversation(user_id):
    # 1. 📡 Probeer uit Supabase
    if supabase:
        try:
            response = supabase.table("memory") \
                .select("*") \
                .eq("user_id", user_id) \
                .order("timestamp", desc=False) \
                .execute()
            if response.data:
                return [{"role": r["role"], "content": r["message"]} for r in response.data]
        except Exception as e:
            print(f"⚠️ Supabase fout: {e} — fallback naar JSON")

    # 2. 📁 Laad lokaal bestand
    filepath = get_user_file(user_id)
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)
