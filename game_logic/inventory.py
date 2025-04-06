import json
from game_logic.memory import save_progress

def add_item(game_state, item):
    """Adds an item to the player's inventory."""
    if "inventory" not in game_state:
        game_state["inventory"] = []  # Ensure inventory exists

    game_state["inventory"].append(item)
    save_progress(game_state)  # Save after adding item
    print(f"\n👜 You picked up {item}!")

def get_inventory(game_state):
    """Displays the player's inventory."""
    inventory = game_state.get("inventory", [])
    
    if inventory:
        print("\n🎒 Your Inventory:")
        for item in inventory:
            print(f"- {item}")
    else:
        print("\n😕 Your inventory is empty.")

def use_item(game_state, item):
    """Allows the player to use an item if available."""
    inventory = game_state.get("inventory", [])

    if item in inventory:
        if item == "Health Potion":
            game_state["health"] = min(game_state["health"] + 20, 100)  # Heal up to max 100 HP
            print("\n❤️ You drank a Health Potion! (+20 HP)")
        
        elif item == "Torch":
            print("\n🔥 The torch flickers, illuminating the dark surroundings.")
        
        else:
            print(f"\n🤔 You used {item}, but nothing happens.")

        inventory.remove(item)  # Remove used item
        save_progress(game_state)  # Save inventory changes

    else:
        print(f"\n⚠️ You don't have {item} in your inventory.")

def drop_item(game_state, item):
    """Removes an item from the player's inventory."""
    inventory = game_state.get("inventory", [])

    if item in inventory:
        inventory.remove(item)
        save_progress(game_state)  # Save inventory update
        print(f"\n🗑️ You dropped {item}.")
    else:
        print(f"\n⚠️ You don't have {item} to drop.")
