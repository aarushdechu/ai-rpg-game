import json
import os

SAVE_FILE = "game_state.json"  # File where progress is saved

def save_progress(game_state):
    """Saves the current game state to a JSON file."""
    with open(SAVE_FILE, "w") as file:
        json.dump(game_state, file, indent=4)

def load_progress():
    """Loads the saved game state from a JSON file."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            game_state = json.load(file)
        print("\n🔄 Game progress loaded!\n")
        return game_state
    else:
        print("\n⚠️ No saved game found. Starting a new game...\n")
        return None  # If no save file, return None

def update_memory(game_state, event):
    """Adds an event to the game history for AI memory."""
    game_state["game_history"] += f"\n{event}"
    save_progress(game_state)

def reset_memory():
    """Deletes the saved game progress to start a new game."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("\n🗑️ Previous game progress deleted. Starting a new adventure!\n")
