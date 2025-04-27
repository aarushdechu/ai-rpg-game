import os
from game_logic.memory import load_progress, save_progress, reset_memory
from game_logic.combat import handle_combat
from game_logic.explore import explore
from game_logic.shop import buy_item, sell_item
from game_logic.inventory import add_item, drop_item, use_item, get_inventory
from game_logic.items import calculate_stats_from_inventory
from game_logic.npc import interact_with_npc
from game_logic.story_generator import generate_story
from game_logic.intent_classifier import infer_intent, infer_goal_action

def load_or_start_game():
    save_path = "game_state.json"
    if os.path.exists(save_path):
        game_state = load_progress()
    else:
        game_state = start_new_game()
    return game_state

def start_new_game():
    game_state = {
        "player_name": "Adventurer",
        "current_location": "a dark cave with glowing runes",
        "inventory": ["Torch"],
        "gold": 20,
        "game_history": "You woke up in a mysterious cave.",
        "health": 100,
        "damage": 10,
        "defence": 10,
        "game_over": False,
        "completed_goals": [],
        "current_goal": "Find and activate all 3 glowing runes",
        "runes_activated": 0,
        "npc_unlocked": False
    }
    save_progress(game_state)
    return game_state

def game_loop(game_state, player_action=None, item_name=None):
    """
    player_action: string ("attack", "explore", "talk", etc.)
    item_name: string (only if using or picking up item)
    """
    output = {"story": "", "combat_result": None, "loot": None, "gold_found": None}

    calculate_stats_from_inventory(game_state)

    if game_state["game_over"]:
        output["story"] = "Game Over. You have perished."
        return game_state, output

    if player_action == "attack":
        combat_log = handle_combat(game_state)
        output["combat_result"] = combat_log

    elif player_action == "explore":
        gold = explore(game_state)
        output["gold_found"] = gold

    elif player_action == "talk":
        npc_result = interact_with_npc(game_state)
        output["story"] = npc_result

    elif player_action == "pickup":
        if item_name:
            add_item(game_state, item_name)

    elif player_action == "use":
        if item_name:
            use_item(game_state, item_name)

    elif player_action == "drop":
        if item_name:
            drop_item(game_state, item_name)

    elif player_action == "shop_buy":
        if item_name:
            success = buy_item(game_state, item_name)
            output["shop_action"] = "bought" if success else "failed"

    elif player_action == "shop_sell":
        if item_name:
            success = sell_item(game_state, item_name)
            output["shop_action"] = "sold" if success else "failed"

    elif player_action == "inventory":
        output["inventory"] = get_inventory(game_state)

    else:
        # Default fallback: generate AI story for general action
        ai_response = generate_story(player_action, game_state)
        output["story"] = ai_response

    save_progress(game_state)
    return game_state, output

def end_game(game_state):
    save_progress(game_state)

if __name__ == "__main__":
    game_state = load_or_start_game()
    # Only for command line (temporary)
    while not game_state["game_over"]:
        # Normally in UI this would be triggered by buttons
        player_input = input("What do you do? ").strip()
        intent = infer_intent(player_input)
        game_state, output = game_loop(game_state, player_action=intent)
