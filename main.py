import os
import random
from game_logic.story_generator import generate_story
from game_logic.memory import save_progress, load_progress, update_memory, reset_memory
from game_logic.inventory import add_item, get_inventory, use_item, drop_item
from game_logic.combat import handle_combat
from game_logic.npc import interact_with_npc

# Shop Inventory (NPC Merchant's Stock)
SHOP_ITEMS = {
    "Health Potion": {"price": 10, "effect": "Restores 20 HP"},
    "Torch": {"price": 5, "effect": "Lights up dark places"},
    "Magic Sword": {"price": 50, "effect": "Stronger attacks"},
    "Shield": {"price": 30, "effect": "Reduces enemy damage"},
}

def load_or_start_game():
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

def start_new_game():
    """Initialize a new game with default settings."""
    game_state = {
        "player_name": input("Enter your name, adventurer: "),
        "current_location": "a dark cave with glowing runes",
        "inventory": ["torch"],
        "gold": 20,  # Starting gold
        "game_history": "You woke up in a mysterious cave.",
        "health": 100,
        "game_over": False
    }
    
    save_progress(game_state)
    print("\n🔮 A new adventure begins!\n")

    # 🎯 Generate AI story when game starts
    intro_story = generate_story(
        player_input="start game",
        game_state=game_state
    )

    return game_state



def display_intro():
    """Displays the game introduction."""
    print("\n🗺️ Welcome to AI Dungeon Master RPG!")
    print("Your choices shape the world around you. Be wise, be brave, and good luck!\n")

def visit_shop(game_state):
    """Allows the player to buy and sell items."""
    print("\n🛒 Welcome to the Merchant's Shop!\n")
    print(f"💰 You have {game_state['gold']} gold.")
    
    print("\nItems for sale:")
    for item, details in SHOP_ITEMS.items():
        print(f"- {item}: {details['price']} gold ({details['effect']})")

    action = input("\nDo you want to [buy] an item, [sell] an item, or [leave] the shop? ").strip().lower()

    if action == "buy":
        item_to_buy = input("Enter the name of the item you want to buy: ").strip()
        if item_to_buy in SHOP_ITEMS:
            price = SHOP_ITEMS[item_to_buy]["price"]
            if game_state["gold"] >= price:
                game_state["gold"] -= price
                add_item(game_state, item_to_buy)
                print(f"\n✅ You bought {item_to_buy} for {price} gold!")
            else:
                print("\n❌ You don't have enough gold.")
        else:
            print("\n❌ That item is not available in the shop.")

    elif action == "sell":
        get_inventory(game_state)
        item_to_sell = input("Enter the name of the item you want to sell: ").strip()
        if item_to_sell in game_state["inventory"]:
            sell_price = SHOP_ITEMS.get(item_to_sell, {"price": 5})["price"] // 2  # Half price for selling
            game_state["gold"] += sell_price
            drop_item(game_state, item_to_sell)
            print(f"\n✅ You sold {item_to_sell} for {sell_price} gold!")
        else:
            print("\n❌ You don't have that item to sell.")

    elif action == "leave":
        print("\n🚪 You leave the shop and continue your adventure.")
    
    save_progress(game_state)

def game_loop(game_state):
    """Runs the main game loop until the game ends."""
    while not game_state["game_over"]:
        print("\n📍 Location:", game_state["current_location"])
        print("🎒 Inventory:", ", ".join(game_state["inventory"]))
        print("❤️ Health:", game_state["health"])
        print("💰 Gold:", game_state["gold"])
        
        player_input = input("\nWhat do you do? ").strip().lower()

        # Allow quitting the game
        if player_input in ["quit", "exit"]:
            save_progress(game_state)
            break

        # Handle combat
        elif "attack" in player_input or "fight" in player_input:
            game_state = handle_combat(game_state)
            update_memory(game_state, f"Engaged in combat: {player_input}")

        # Handle NPC interactions
        elif "talk" in player_input or "meet" in player_input or "ask" in player_input:
            interact_with_npc(game_state)

        # Handle inventory actions
        elif "inventory" in player_input or "check items" in player_input:
            get_inventory(game_state)

        elif "take" in player_input or "pickup" in player_input:
            item = player_input.split(" ", 1)[-1]
            add_item(game_state, item)
            update_memory(game_state, f"Picked up {item}")

        elif "use" in player_input:
            item = player_input.split(" ", 1)[-1]
            use_item(game_state, item)
            update_memory(game_state, f"Used {item}")

        elif "drop" in player_input:
            item = player_input.split(" ", 1)[-1]
            drop_item(game_state, item)
            update_memory(game_state, f"Dropped {item}")

        # Handle visiting the shop
        elif "shop" in player_input or "buy" in player_input or "sell" in player_input:
            visit_shop(game_state)

        # Exploration gold bonus
        elif "explore" in player_input or "search" in player_input:
            if random.random() < 0.4:  # 40% chance to find gold
                gold_found = random.randint(3, 15)
                game_state["gold"] += gold_found
                print(f"\n💰 While searching, you found {gold_found} gold!")

        else:
            # Generate AI-driven story progression
            ai_response = generate_story(
                player_input, 
                game_state  # ✅ NEW ARGUMENT
                )

            print("\n📖", ai_response)

            # Update game history and memory
            update_memory(game_state, f"{player_input}: {ai_response}")

        # Check for game over conditions
        if game_state["health"] <= 0:
            print("\n💀 You have perished! Game Over.")
            game_state["game_over"] = True

        # Save progress after every action
        save_progress(game_state)

def end_game(game_state):
    """Handles the end of the game."""
    print("\n💾 Saving your adventure...")
    save_progress(game_state)
    print("\n🔚 Thanks for playing! See you next time, adventurer.")

if __name__ == "__main__":
    display_intro()
    game_state = load_or_start_game()
    game_loop(game_state)
    end_game(game_state)
