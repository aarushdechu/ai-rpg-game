import random
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from game_logic.inventory import add_item
from game_logic.memory import save_progress

# Initialize LLM
llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")

monster_prompt = PromptTemplate(
    input_variables=[],
    template="""
Generate a fantasy monster for a text-based RPG game.

Rules:
- HP between 10 and 30
- Defense between 8 and 18 (higher defense = harder to hit)
- Damage inversely related to HP
- Loot: 1-2 items (gold, weapons, potions)
- Gold between 5 and 25

Respond ONLY with valid JSON:
{
  "name": "MonsterName",
  "hp": number,
  "defense": number,
  "damage": number,
  "loot": ["item1", "item2"],
  "gold": number
}
"""
)

# ✅ New Chain: prompt | llm
monster_chain = monster_prompt | llm

def generate_monster():
    response = monster_chain.invoke({})
    try:
        monster = eval(response.content)
        return monster
    except Exception as e:
        print("⚠️ Monster generation failed. Using fallback.")
        return {
            "name": "Fallback Goblin",
            "hp": 20,
            "defense": 10,
            "damage": 5,
            "loot": ["Rusty Sword"],
            "gold": 10
        }

def player_attack_monster(monster):
    dice_roll = random.randint(1, 20)
    print(f"🎲 You rolled {dice_roll} vs monster defense {monster['defense']}")
    return dice_roll >= monster["defense"]

def monster_attack_player(game_state, monster):
    dice_roll = random.randint(1, 20)
    print(f"🎲 {monster['name']} rolled {dice_roll} vs your defense {game_state.get('defense_bonus', 10)}")
    return dice_roll >= game_state.get("defense_bonus", 10)

def distribute_loot(game_state, monster):
    print("\n🎁 Loot Collected:")
    for item in monster["loot"]:
        if "gold" in item.lower():
            try:
                amount = int(item.split(" ")[0])
                game_state["gold"] += amount
                print(f"💰 Found {amount} gold!")
            except:
                print(f"⚠️ Could not process loot item: {item}")
        else:
            add_item(game_state, item)
            print(f"🛡️ Found {item}")

    game_state["gold"] += monster.get("gold", 0)
    print(f"🪙 Earned {monster.get('gold', 0)} extra gold!")

def handle_combat(game_state):
    monster = generate_monster()

    print(f"\n⚔️ A wild {monster['name']} appears!")
    print(f"🧟 Stats → HP: {monster['hp']} | Defense: {monster['defense']} | Damage: {monster['damage']}")

    while monster["hp"] > 0 and game_state["health"] > 0:
        action = input("\nDo you [attack], [run], or [use item]? ").strip().lower()

        if action == "attack":
            if player_attack_monster(monster):
                player_attack = 10 + game_state.get("attack_bonus", 0)
                monster["hp"] -= player_attack
                print(f"🗡️ You hit {monster['name']} for {player_attack} damage! (HP left: {max(monster['hp'], 0)})")
            else:
                print(f"🛡️ You missed!")

        elif action == "use item":
            print("🔮 Using items during battle coming soon!")

        elif action == "run":
            print("🏃 You escaped!")
            save_progress(game_state)
            return game_state

        else:
            print("❓ Invalid action. Try again.")
            continue

        # Monster attacks back
        if monster["hp"] > 0:
            if monster_attack_player(game_state, monster):
                damage_taken = monster["damage"]
                game_state["health"] -= damage_taken
                print(f"💥 {monster['name']} hits you for {damage_taken} damage! (Your HP: {max(game_state['health'], 0)})")
            else:
                print(f"🛡️ You dodged {monster['name']}'s attack!")

    # Battle end
    if game_state["health"] <= 0:
        print("\n💀 You have been defeated...")
        game_state["game_over"] = True
    else:
        print(f"\n🏆 You defeated {monster['name']}!")
        distribute_loot(game_state, monster)

    save_progress(game_state)
    return game_state
