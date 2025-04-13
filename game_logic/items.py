def use_item_effect(game_state, item_name):
    """Apply the effect of using a specific item."""
    item_name = item_name.lower()

    if item_name == "health potion":
        restored = 20
        game_state["health"] = min(game_state["health"] + restored, 100)
        print(f"🧪 You drank a Health Potion and restored {restored} HP! Your health is now {game_state['health']}.")
        game_state["inventory"].remove("Health Potion")

    elif item_name == "torch":
        print("🔥 You hold up your Torch. The area around you is now well lit.")
        # Optional: set a flag like game_state["light_on"] = True

    elif item_name == "magic sword":
        print("🗡️ You grip the Magic Sword. Power surges through you!")
        game_state["damage"] += 5

    elif item_name == "shield":
        print("🛡️ You raise your Shield. Incoming attacks will be reduced.")
        game_state["defence"] = 3

    elif item_name == "goblin dagger":
        print("🗡️ You equip the Goblin Dagger. It's light but deadly.")
        game_state["damage"] = 2

    else:
        print("🤷 Nothing happens... maybe it's just decorative.")

    return game_state
