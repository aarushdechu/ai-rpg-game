import random

NPC_LIST = [
    {"name": "Old Wizard", "type": "wise"},
    {"name": "Friendly Villager", "type": "friendly"},
    {"name": "Mysterious Stranger", "type": "mysterious"}
]

def interact_with_npc(game_state):
    npc = random.choice(NPC_LIST)
    return f"You meet {npc['name']}: \"Hello, traveler!\""
