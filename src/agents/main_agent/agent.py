from .sub_agents.hello_agent.agent import hello_agent
from .sub_agents.summarize_agent.agent import summarize_agent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

MODEL = "gemini-2.0-flash"


main_agent = LlmAgent(
    name="root_agent",
    model=MODEL,
    description=("挨拶と要約を行うエージェントです。"),
    instruction="あいさつをして、要約を行うエージェントです。",
    tools=[
        AgentTool(agent=hello_agent),
        AgentTool(agent=summarize_agent),
    ],
)

root_agent = main_agent
