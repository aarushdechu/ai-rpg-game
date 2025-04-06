import random
from game_logic.story_generator import generate_story
from game_logic.memory import save_progress, update_memory
from game_logic.inventory import add_item, get_inventory, use_item, drop_item
from game_logic.combat import handle_combat
from game_logic.npc import interact_with_npc
from game_logic.shop import visit_shop
from game_logic.explore import explore
from game_logic.game_loader import load_or_start_game

def display_intro():
    print("\n🗺️ Welcome to AI Dungeon Master RPG!")
    print("Your choices shape the world around you. Be wise, be brave, and good luck!\n")

def game_loop(game_state):
    while not game_state["game_over"]:
        print("\n📍 Location:", game_state["current_location"])
        print("🎒 Inventory:", ", ".join(game_state["inventory"]))
        print("❤️ Health:", game_state["health"])
        print("💰 Gold:", game_state["gold"])
        print("🎯 Goal:", game_state.get("current_goal", "None"))

        player_input = input("\nWhat do you do? ").strip().lower()

        if player_input in ["quit", "exit"]:
            save_progress(game_state)
            break

        elif "attack" in player_input or "fight" in player_input:
            game_state = handle_combat(game_state)
            update_memory(game_state, f"Engaged in combat: {player_input}")

        elif "talk" in player_input or "meet" in player_input or "ask" in player_input:
            interact_with_npc(game_state)

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

        # ✅ This now uses the external shop function!
        elif "shop" in player_input or "buy" in player_input or "sell" in player_input:
            visit_shop(game_state)

        # ✅ This now uses the external explore function!
        elif "explore" in player_input or "search" in player_input:
            explore(game_state)

        # ✅ Touch rune logic remains in main.py for goal control
        elif "touch rune" in player_input or "activate rune" in player_input:
            game_state["runes_activated"] += 1
            print(f"✨ You have activated {game_state['runes_activated']} of 3 runes!")

            if game_state["runes_activated"] == 3 and "rune_quest" not in game_state["completed_goals"]:
                game_state["completed_goals"].append("rune_quest")
                game_state["current_goal"] = "Recover the Crystal Sword from the Goblin King"
                print("\n🎉 You have completed your goal! The chamber rumbles and a hidden door opens...")

        elif len(game_state["completed_goals"]) >= 2 and not game_state["npc_unlocked"]:
            game_state["npc_unlocked"] = True
            print("\n🧙 NPCs are now available! Seek out the villagers, sages, and merchants for help.")

        else:
            ai_response = generate_story(
                player_input=player_input,
                game_state=game_state
            )
            print("\n📖", ai_response)
            update_memory(game_state, f"{player_input}: {ai_response}")

        if game_state["health"] <= 0:
            print("\n💀 You have perished! Game Over.")
            game_state["game_over"] = True

        save_progress(game_state)

def end_game(game_state):
    print("\n💾 Saving your adventure...")
    save_progress(game_state)
    print("\n🔚 Thanks for playing! See you next time, adventurer.")

if __name__ == "__main__":
    display_intro()
    game_state = load_or_start_game()
    game_loop(game_state)
    end_game(game_state)
