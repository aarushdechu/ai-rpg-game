from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

# --- Intent Classifier Setup ---
intent_schema = ResponseSchema(
    name="intent",
    description="The player's intended action. Must be one of: attack, explore, talk, use, drop, pickup, shop, inventory, quit, goal_action"
)
intent_parser = StructuredOutputParser.from_response_schemas([intent_schema])

intent_prompt = PromptTemplate(
    template="""
You are an intent detection AI for a text-based RPG game.

Your job is to understand what the player is trying to do and map it to one of the known commands.

Valid commands are:
- attack
- explore
- talk
- use
- drop
- pickup
- shop
- inventory
- quit
- goal_action

Use 'goal_action' if the action is not a generic command, but clearly helps the player progress toward their current goal (e.g., touching a rune when the goal is to activate runes).

{format_instructions}

Player input: {player_input}
""",
    input_variables=["player_input"],
    partial_variables={"format_instructions": intent_parser.get_format_instructions()}
)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# --- NEW Chain (prompt | llm) ---
intent_chain = intent_prompt | llm

def infer_intent(player_input):
    response = intent_chain.invoke({"player_input": player_input})
    parsed = intent_parser.parse(response.content)  # .content instead of ["text"]
    return parsed["intent"]

# --- Goal Progress Helper (NEW, correct style) ---
goal_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a game logic engine for a text-based RPG.\n"
        "Given a player input and the current goal, your job is to decide whether this input helps progress that goal.\n"
        "Respond only with 'yes' or 'no'. Be generous — if the player is attempting or clearly describing a step related to the goal, say 'yes'."
    ),
    HumanMessagePromptTemplate.from_template(
        "Current goal: {current_goal}\nPlayer input: {player_input}\nDoes this progress the goal?"
    )
])

goal_chain = goal_prompt | llm

def infer_goal_action(player_input, current_goal):
    response = goal_chain.invoke({"player_input": player_input, "current_goal": current_goal})
    return response.content.strip().lower() == "yes"
