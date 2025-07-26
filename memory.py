import os
import json

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

def get_user_file(user_id):
    return os.path.join(DATA_FOLDER, f"{user_id}.json")

def save_message(user_id, role, content):
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
