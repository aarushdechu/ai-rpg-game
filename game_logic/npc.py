import random
from game_logic.memory import update_memory
from game_logic.inventory import add_item
from game_logic.story_generator import generate_story

def generate_npc():
    """Creates a random NPC with a personality."""
    npc_list = [
        {"name": "Old Wizard", "type": "wise", "greeting": "Ah, traveler... I have seen the future."},
        {"name": "Mysterious Merchant", "type": "trader", "greeting": "You seek power? Perhaps I have something for you."},
        {"name": "Suspicious Stranger", "type": "shady", "greeting": "Heh, not many survive these lands..."},
        {"name": "Friendly Villager", "type": "friendly", "greeting": "Oh! You must be the hero we've been waiting for!"},
    ]
    return random.choice(npc_list)

def interact_with_npc(game_state):
    """Handles interactions between the player and an NPC."""
    
    npc = generate_npc()
    print(f"\n🗣️ You meet {npc['name']}: \"{npc['greeting']}\"\n")

    player_choice = input("Do you want to [talk], [ask for help], or [leave]? ").strip().lower()

    if player_choice == "talk":
        dialogue = generate_story(
            player_input=f"Player is talking to {npc['name']} ({npc['type']} personality).",
            current_location=game_state["current_location"],
            inventory=game_state["inventory"],
            game_history=game_state["game_history"]
        )

        print(f"\n{npc['name']} says: \"{dialogue}\"")
        update_memory(game_state, f"Spoke with {npc['name']}: {dialogue}")

    elif player_choice == "ask for help":
        if npc["type"] == "wise":
            print("\n📜 The wizard whispers an ancient secret to you...")
            update_memory(game_state, "Received a prophecy from the Old Wizard.")

        elif npc["type"] == "trader":
            item = random.choice(["Health Potion", "Magic Ring", "Silver Key"])
            print(f"\n🛒 The merchant gives you a {item}.")
            add_item(game_state, item)
            update_memory(game_state, f"Received {item} from {npc['name']}.")

        elif npc["type"] == "shady":
            print("\n🤨 The stranger leans in and warns: \"Watch your back in these lands...\"")
            update_memory(game_state, f"Received a warning from {npc['name']}.")

        elif npc["type"] == "friendly":
            gold_reward = random.randint(10, 30)
            game_state["gold"] += gold_reward
            print(f"\n😊 The villager rewards you with {gold_reward} gold for your kindness!")
    elif player_choice == "leave":
        print(f"\n👋 You leave {npc['name']} behind.")
        update_memory(game_state, f"Left {npc['name']} without talking.")

    else:
        print("\n🤔 The NPC stares at you, confused by your response.")

    update_memory(game_state, f"Interacted with {npc['name']}.")
