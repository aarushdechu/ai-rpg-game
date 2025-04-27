import random
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from game_logic.inventory import add_item
from game_logic.memory import save_progress
from game_logic.items import calculate_stats_from_inventory

llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")

monster_prompt = PromptTemplate(
    input_variables=[],
    template="""
Generate a fantasy monster for a text-based RPG game.

Rules:
- HP between 10 and 30
- Defense between 8 and 18
- Damage inversely related to HP
- Loot: 1-2 items (gold, weapons, potions)
- Gold between 5 and 25

Respond ONLY with JSON like:
{{
  "name": "MonsterName",
  "hp": number,
  "defense": number,
  "damage": number,
  "loot": ["item1", "item2"],
  "gold": number
}}
"""
)

monster_chain = monster_prompt | llm

def generate_monster():
    response = monster_chain.invoke({})
    try:
        monster = eval(response.content)
        return monster
    except Exception:
        return {
            "name": "Fallback Goblin",
            "hp": 20,
            "defense": 10,
            "damage": 5,
            "loot": ["Rusty Sword"],
            "gold": 10
        }

def player_attack_monster(monster, game_state):
    dice_roll = random.randint(1, 20)
    return dice_roll >= monster["defense"]

def monster_attack_player(monster, game_state):
    dice_roll = random.randint(1, 20)
    return dice_roll >= game_state["defence"]

def distribute_loot(game_state, monster):
    for item in monster["loot"]:
        add_item(game_state, item)
    game_state["gold"] += monster.get("gold", 0)

def handle_combat(game_state):
    calculate_stats_from_inventory(game_state)
    monster = generate_monster()
    combat_log = {
        "monster": monster,
        "player_damage": [],
        "monster_damage": [],
        "result": None
    }

    while monster["hp"] > 0 and game_state["health"] > 0:
        if player_attack_monster(monster, game_state):
            monster["hp"] -= game_state["damage"]
            combat_log["player_damage"].append(game_state["damage"])

        if monster["hp"] > 0 and monster_attack_player(monster, game_state):
            game_state["health"] -= monster["damage"]
            combat_log["monster_damage"].append(monster["damage"])

    if game_state["health"] <= 0:
        game_state["game_over"] = True
        combat_log["result"] = "defeat"
    else:
        distribute_loot(game_state, monster)
        combat_log["result"] = "victory"

    save_progress(game_state)
    return combat_log
