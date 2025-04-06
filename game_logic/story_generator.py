import openai
import os
from langchain.prompts import PromptTemplate
from game_logic.memory import update_memory

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# Define Dungeon Master AI Prompt
dm_prompt = PromptTemplate(
    input_variables=["current_location", "inventory", "game_history", "player_input", "current_goal", "npc_status"],
    template="""
    You are a Dungeon Master for a text-based RPG game. 
    Your job is to narrate the adventure, describe surroundings, and react dynamically to the player's actions.

    The player is currently in:
    {current_location}

    The player’s current goal is:
    {current_goal}


    They have:
    {inventory}

    Previous events:
    {game_history}

    Player action: {player_input}

    NPCs are currently {npc_status}.


    What happens next? Respond with a vivid description, a possible challenge, or an unexpected twist.
    """
)

def generate_story(player_input, game_state):
    npc_status = {'unlocked' if game_state['npc_unlocked'] else 'locked'}
    formatted_prompt = dm_prompt.format(
        player_input=player_input,
        current_location=game_state["current_location"],
        inventory=game_state["inventory"],
        game_history=game_state["game_history"]
        npc_status=game_state["npc_unlocked"]
        current_goal=game_state["current_goal"]
    )

    # 🆕 NEW OpenAI SDK usage
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Dungeon Master for a text-based RPG game."},
            {"role": "user", "content": formatted_prompt}
        ],
        max_tokens=521
    )

    ai_response = response.choices[0].message.content
    update_memory(game_state, f"{player_input} → {ai_response}")
    return ai_response

