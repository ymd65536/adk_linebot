from .hello_agent import hello_agent
from .summarize_agent import summarize_agent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

MODEL = "gemini-2.0-flash"


root_agent = LlmAgent(
    name="root_agent",
    model=MODEL,
    description=("挨拶と要約を行うエージェントです。"),
    instruction="あいさつをして、要約を行うエージェントです。",
    output_key="seminal_paper",
    tools=[
        AgentTool(greeting_man),
        AgentTool(summarize_agent)
    ],
)
