import random
from game_logic.memory import save_progress

def explore(game_state):
    if random.random() < 0.4:
        gold_found = random.randint(3, 15)
        game_state["gold"] += gold_found
        print(f"\n💰 While searching, you found {gold_found} gold!")
        save_progress(game_state)
    else:
        print("\n🔍 You search the area, but find nothing of value.")
