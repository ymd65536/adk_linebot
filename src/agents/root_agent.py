from google.adk.agents import LlmAgent
from . import prompt

MODEL = "gemini-2.5-pro-preview-05-06"


root_agent = LlmAgent(
    name="root_agent",
    model=MODEL,
    description=(),
    instruction=prompt.ACADEMIC_COORDINATOR_PROMPT,
    output_key="seminal_paper",
    tools=[],
)
