import openai
import os
from langchain.prompts import PromptTemplate
from game_logic.memory import update_memory

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# Define Dungeon Master AI Prompt
dm_prompt = PromptTemplate(
    input_variables=["current_location", "inventory", "game_history", "player_input"],
    template="""
    You are a Dungeon Master for a text-based RPG game. 
    Your job is to narrate the adventure, describe surroundings, and react dynamically to the player's actions.

    The player is currently in:
    {current_location}

    They have:
    {inventory}

    Previous events:
    {game_history}

    Player action: {player_input}

    What happens next? Respond with a vivid description, a possible challenge, or an unexpected twist.
    """
)

def generate_story(player_input, game_state):

    formatted_prompt = dm_prompt.format(
        player_input=player_input,
        current_location=game_state["current_location"],
        inventory=game_state["inventory"],
        game_history=game_state["game_history"]
    )

    # 🆕 NEW OpenAI SDK usage
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a Dungeon Master for a text-based RPG game."},
            {"role": "user", "content": formatted_prompt}
        ],
        max_tokens=250
    )

    ai_response = response.choices[0].message.content
    update_memory(game_state, f"{player_input} → {ai_response}")
    return ai_response

