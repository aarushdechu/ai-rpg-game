from game_logic.items import use_item_effect

def add_item(game_state, item):
    if "inventory" not in game_state:
        game_state["inventory"] = []
    game_state["inventory"].append(item)

def drop_item(game_state, item):
    if "inventory" in game_state and item in game_state["inventory"]:
        game_state["inventory"].remove(item)

def get_inventory(game_state):
    return game_state.get("inventory", [])

def use_item(game_state, item_name):
    if item_name in game_state.get("inventory", []):
        effect_message = use_item_effect(game_state, item_name)
        drop_item(game_state, item_name)
        return effect_message
    return "Item not found."

