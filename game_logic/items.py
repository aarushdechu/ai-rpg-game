def use_item_effect(game_state, item_name):
    """Apply the effect of using a specific item."""
    item_name = item_name.lower()

   def use_item_effect(game_state, item_name):
    if item_name.lower() == "health potion":
        game_state["health"] = min(100, game_state["health"] + 20)
        return "Health restored by 20."
    
    # Future: add more items here
    elif item_name.lower() == "magic elixir":
        game_state["damage"] += 5
        return "Damage increased by 5."
    
    return "Nothing happened."

    return game_state

def calculate_stats_from_inventory(game_state):
    # Start with default base stats
    base_damage = game_state["damage"]
    base_defence = game_state["defence"]

    # Check inventory and boost stats
    for item in game_state.get("inventory", []):
        item = item.lower()
        if "dagger" in item:
            base_damage += 3
        elif "sword" in item:
            base_damage += 5
        elif "axe" in item:
            base_damage += 6
        elif "shield" in item:
            base_defence += 2
        elif "armor" in item:
            base_defence += 3
