import os
from game_logic.memory import load_progress, save_progress, reset_memory
from game_logic.story_generator import generate_story

def start_new_game():
    game_state = {
        "player_name": input("Enter your name, adventurer: "),
        "current_location": "a dark cave with glowing runes",
        "inventory": ["torch"],
        "gold": 0,
        "game_history": "You woke up in a mysterious cave.",
        "health": 100,
        "game_over": False,
        "completed_goals": [],
        "current_goal": "Find and activate all 3 glowing runes",
        "runes_activated": 0,
        "npc_unlocked": False
        "damage": 2
        "defence": 10
    }

    save_progress(game_state)
    print("\n🔮 A new adventure begins!\n")

    # generate intro story using the full game_state
    intro_story = generate_story("start game", game_state)
    print("\n📖", intro_story)

    return game_state

def load_or_start_game():
    save_path = "game_state.json"

    if os.path.exists(save_path):
        choice = input("Would you like to continue your previous adventure? (yes/no): ").strip().lower()
        if choice == "yes":
            return load_progress()
        else:
            reset_memory()
            return start_new_game()
    else:
        return start_new_game()
