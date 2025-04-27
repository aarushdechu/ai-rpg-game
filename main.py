import random
from game_logic.story_generator import generate_story
from game_logic.memory import save_progress, update_memory
from game_logic.inventory import add_item, get_inventory, use_item, drop_item
from game_logic.combat import handle_combat
from game_logic.npc import interact_with_npc
from game_logic.shop import visit_shop
from game_logic.explore import explore
from game_logic.game_loader import load_or_start_game
from game_logic.intent_classifier import infer_intent, infer_goal_action
from game_logic.items import use_item_effect

def pickup_item(game_state, raw_input):
    item = raw_input.split(" ", 1)[-1].strip().title()
    add_item(game_state, item)
    print(f"🎒 Picked up {item}")
    update_memory(game_state, f"Picked up {item}")

def use_inventory_item(game_state, raw_input):
    item = raw_input.split(" ", 1)[-1].strip().title()
    if item in game_state["inventory"]:
        use_item_effect(game_state, item)
        update_memory(game_state, f"Used {item}")
    else:
        print("❌ You don't have that item.")

def drop_inventory_item(game_state, raw_input):
    item = raw_input.split(" ", 1)[-1].strip().title()
    drop_item(game_state, item)
    print(f"🗑️ Dropped {item}")
    update_memory(game_state, f"Dropped {item}")

def display_player_info(game_state):
    print("\n📍 Location:", game_state.get("current_location", "Unknown"))
    print("🎒 Inventory:", ", ".join(game_state.get("inventory", [])))
    print("❤️ Health:", game_state.get("health", 0))
    print("💰 Gold:", game_state.get("gold", 0))
    print("🎯 Goal:", game_state.get("current_goal", "None"))

# --- Action Map ---

ACTION_MAP = {
    "attack": lambda game_state, raw_input: handle_combat(game_state),
    "talk": lambda game_state, raw_input: interact_with_npc(game_state),
    "inventory": lambda game_state, raw_input: get_inventory(game_state),
    "explore": lambda game_state, raw_input: explore(game_state),
    "search": lambda game_state, raw_input: explore(game_state),
    "shop": lambda game_state, raw_input: visit_shop(game_state),
    "buy": lambda game_state, raw_input: visit_shop(game_state),
    "sell": lambda game_state, raw_input: visit_shop(game_state),
    "pickup": lambda game_state, raw_input: pickup_item(game_state, raw_input),
    "take": lambda game_state, raw_input: pickup_item(game_state, raw_input),
    "use": lambda game_state, raw_input: use_inventory_item(game_state, raw_input),
    "drop": lambda game_state, raw_input: drop_inventory_item(game_state, raw_input), 
    "info": lambda game_state, raw_input: display_player_info(game_state)

}

def display_intro():
    print("\n🗺️ Welcome to AI Dungeon Master RPG!")
    print("Your choices shape the world around you. Be wise, be brave, and good luck!\n")

def game_loop(game_state):
    while not game_state["game_over"]:
        calculate_stats_from_inventory(game_state)
        
        raw_input = input("\nWhat do you do? ").strip()
        intent = infer_intent(raw_input)

        if intent in ["quit", "exit"]:
            save_progress(game_state)
            break

        elif intent == "attack":
            game_state = handle_combat(game_state)
            update_memory(game_state, f"Engaged in combat: {raw_input}")

        elif intent == "talk":
            interact_with_npc(game_state)

        elif intent == "inventory":
            get_inventory(game_state)

        elif intent in ["pickup", "take"]:
            item = raw_input.split(" ", 1)[-1]
            add_item(game_state, item)
            update_memory(game_state, f"Picked up {item}")

        elif intent == "use":
            item = raw_input.split(" ", 1)[-1].strip().title()
            if item in game_state["inventory"]:
                use_item_effect(game_state, item)
                update_memory(game_state, f"Used {item}")
            else:
                print("❌ You don't have that item.")
        elif intent == "drop":
            item = raw_input.split(" ", 1)[-1]
            drop_item(game_state, item)
            update_memory(game_state, f"Dropped {item}")

        elif intent in ["shop", "buy", "sell"]:
            visit_shop(game_state)

        elif intent in ["explore", "search"]:
            explore(game_state)

        elif intent == "goal_action":
            if infer_goal_action(raw_input, game_state["current_goal"]):
                game_state["runes_activated"] += 1
                print(f"✨ You have activated {game_state['runes_activated']} of 3 runes!")

                if game_state["runes_activated"] == 3 and "rune_quest" not in game_state["completed_goals"]:
                    game_state["completed_goals"].append("rune_quest")
                    game_state["current_goal"] = "Recover the Crystal Sword from the Goblin King"
                    print("\n🎉 You have completed your goal! The chamber rumbles and a hidden door opens...")
            else:
                print("🤔 That didn't seem to help with your current goal.")

        if game_state["runes_activated"] == 3 and "rune_quest" not in game_state["completed_goals"]:
            game_state["completed_goals"].append("rune_quest")
            game_state["current_goal"] = "Recover the Crystal Sword from the Goblin King"
            print("\n🎉 You have completed your goal! The chamber rumbles and a hidden door opens...")
            if game_state["runes_activated"] == 3 and "rune_quest" not in game_state["completed_goals"]:
                game_state["completed_goals"].append("rune_quest")
                game_state["current_goal"] = "Recover the Crystal Sword from the Goblin King"
                print("\n🎉 You have completed your goal! The chamber rumbles and a hidden door opens...")

        elif len(game_state["completed_goals"]) >= 2 and not game_state["npc_unlocked"]:
            game_state["npc_unlocked"] = True
            print("\n🧙 NPCs are now available! Seek out the villagers, sages, and merchants for help.")

        else:
            ai_response = generate_story(
                player_input=raw_input,
                game_state=game_state
            )
            print("\n📖", ai_response)
            update_memory(game_state, f"{raw_input}: {ai_response}")

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
