import os
from game_logic.memory import load_progress, reset_memory
from game_logic.story_generator import generate_story

def load_or_start_game(start_new_game):
    """Load game progress if available, otherwise start a new game."""
    save_path = "game_state.json"
    
    if os.path.exists(save_path):
        choice = input("Would you like to continue your previous adventure? (yes/no): ").strip().lower()
        if choice == "yes":
            game_state = load_progress()
        else:
            reset_memory()
            game_state = start_new_game()
    else:
        game_state = start_new_game()
    return game_state
