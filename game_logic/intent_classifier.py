from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
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

Player input: {player_input}

{format_instructions}
""",
    input_variables=["player_input"],
    partial_variables={"format_instructions": intent_parser.get_format_instructions()}
)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

def infer_intent(player_input):
    response = intent_chain.run(player_input=player_input)
    parsed = intent_parser.parse(response)
    return parsed["intent"]

# --- Goal Progress Helper ---
def infer_goal_action(player_input, current_goal):
    response = llm.invoke([
        {
            "role": "system",
            "content": (
                "You are a game logic engine for a text-based RPG.\n"
                "Given a player input and the current goal, your job is to decide whether this input helps progress that goal.\n"
                "Respond only with 'yes' or 'no'."
            ),
        },
        {
            "role": "user",
            "content": f"Current goal: {current_goal}\nPlayer input: {player_input}\nDoes this progress the goal?"
        },
    ])
    return response.content.strip().lower() == "yes"
