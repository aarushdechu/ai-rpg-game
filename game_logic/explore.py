import random

def explore(game_state):
    gold_found = random.randint(3, 15)
    game_state["gold"] += gold_found
    return gold_found
