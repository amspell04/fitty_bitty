from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    model=LiteLlm(model="ollama_chat/gemma3:latest"),
    name="researcher",
    instruction="You help the user plan their workout for the day based on their current" \
    "workout program and how the user is feeling that day. You use local tools to make changes" \
    "to their workout plan for the day based on feedback from the user." \
    "You should always ask the user how they are feeling on a scale of 1-10, get the current"
    "days workout with the mcp tool 'get_workout' and then use the user's response of how they are feeling" \
    "to calculate changes to their workout program using your local tool: 'calibrate_workout'. ",
    # tools=[],
)