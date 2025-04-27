import json
import os

def save_progress(game_state):
    with open("game_state.json", "w") as f:
        json.dump(game_state, f)

def load_progress():
    if os.path.exists("game_state.json"):
        with open("game_state.json", "r") as f:
            return json.load(f)
    return None

def reset_memory():
    if os.path.exists("game_state.json"):
        os.remove("game_state.json")
