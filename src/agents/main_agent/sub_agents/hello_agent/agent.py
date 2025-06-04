from google.adk.agents import LlmAgent
from google.adk.agents import Agent

MODEL = "gemini-2.0-flash"

hello_agent = LlmAgent(
    name="hello_agent",
    model=MODEL,
    description=(
        "挨拶をしてくれるエージェントです。"
    ),
    instruction=(
        "友達のように挨拶します。"
        "挨拶以外はしません。"
    )
)
