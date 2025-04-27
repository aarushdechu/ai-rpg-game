from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")

story_prompt = PromptTemplate(
    input_variables=["player_input", "current_location", "inventory", "game_history", "npc_status"],
    template="""
You are the narrator of a fantasy RPG. Given the player's input, describe what happens next.

Player Input: {player_input}
Current Location: {current_location}
Inventory: {inventory}
Game History: {game_history}
NPCs Unlocked: {npc_status}

Describe next event vividly but short (max 5 lines).
"""
)

story_chain = story_prompt | llm

def generate_story(player_input, game_state):
    npc_status = game_state["npc_unlocked"]
    response = story_chain.invoke({
        "player_input": player_input,
        "current_location": game_state["current_location"],
        "inventory": ", ".join(game_state["inventory"]),
        "game_history": game_state["game_history"],
        "npc_status": npc_status
    })
    return response.content
