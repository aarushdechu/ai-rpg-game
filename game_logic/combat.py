import random
import time
from game_logic.memory import save_progress

def handle_combat(game_state):
    """Handles a combat encounter between the player and an enemy."""
    
    print("\n⚔️ A battle begins! ⚔️\n")
    
    # 🎲 Generate a random enemy
    enemy = generate_enemy()
    enemy_hp = enemy["hp"]
    
    print(f"🧌 {enemy['name']} appears! ({enemy_hp} HP)\n")
    
    while enemy_hp > 0 and game_state["health"] > 0:
        # 🎯 Player's Turn
        print("\n💥 Your Turn!")
        action = input("Do you want to [attack] or [run]? ").strip().lower()

        if action == "run":
            print("\n🏃 You flee from the battle!")
            return game_state  # Escape battle without damage
        
        elif action == "attack":
            player_attack = roll_dice(20) + 2  # Simulating an attack roll
            print(f"\n🎲 You roll a {player_attack} to attack!")

            if player_attack >= enemy["defense"]:
                damage = 2  # default damage unless you get different weapons (add later)
                enemy_hp -= damage
                print(f"⚔️ You strike {enemy['name']} for {damage} damage!")
            else:
                print(f"❌ You miss! {enemy['name']} dodges your attack.")

        # 🎯 Enemy's Turn
        if enemy_hp > 0:
            print(f"\n🧌 {enemy['name']}'s turn!")
            enemy_attack = roll_dice(20)
            
            if enemy_attack >= 12:  # Example: Player has defense 12
                damage = enemy["damage"]
                game_state["health"] -= damage
                print(f"🔥 {enemy['name']} attacks you for {damage} damage!")
            else:
                print(f"💨 {enemy['name']} swings wildly but misses!")

        # 🎯 Check for Victory or Defeat
        if enemy_hp <= 0:
            gold_earned = enemy["gold"]
            game_state["gold"] += gold_earned
            print(f"\n🎉 You have defeated {enemy['name']} and earned {gold_earned} gold! 🎉")

            loot = enemy.get("loot")
            if loot:
                print(f"🎁 You found {loot}!")
                game_state["inventory"].append(loot)  # Add loot to inventory

        elif game_state["health"] <= 0:
            print("\n💀 You have been defeated... Game Over.")
            game_state["game_over"] = True
            return game_state
        
        # Save game state after every round
        save_progress(game_state)

    return game_state  # Return updated game state

def generate_enemy():
    """Generates a random enemy with stats."""
    enemies = [
        {"name": "Goblin", "hp": 10, "defense": 10, "loot": "Goblin Dagger", "damage": 7, "gold": 15},
        {"name": "Orc", "hp": 15, "defense": 12, "loot": "Orc War Axe", "damage": 3, "gold": 15},
        {"name": "Dark Wizard", "hp": 12, "defense": 14, "loot": "Magic Scroll", "damage": 5, "gold": 15},
        {"name": "Skeleton Warrior", "hp": 8, "defense": 11, "loot": "Rusty Sword", "damage": 10, "gold": 15},
    ]
    return random.choice(enemies)

def roll_dice(sides):
    """Rolls a dice with the given number of sides."""
    return random.randint(1, sides)
