from google.adk import Agent
from google.adk.tools import google_search

agent = Agent(
    name="researcher",
    model="gemini-flash-latest",
    instruction="You help the user plan their workout for the day based on their current" \
    "workout program and how the user is feeling that day. You use local tools to make changes" \
    "to their workout plan for the day based on feedback from the user." \
    "You should always ask the user how they are feeling on a scale of 1-10, get the current"
    "days workout with the mcp tool 'get_workout' and then use the user's response of how they are feeling" \
    "to calculate changes to their workout program using your local tool: 'calibrate_workout'. ",
    tools=[google_search],
)