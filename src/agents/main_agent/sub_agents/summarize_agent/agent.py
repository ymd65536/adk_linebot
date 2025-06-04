from google.adk.agents import LlmAgent
from google.adk.agents import Agent

MODEL = "gemini-2.0-flash"

summarize_agent = LlmAgent(
    name="summarize",
    model=MODEL,
    description=(
        "要約を行うエージェントです。"
        "入力されたテキストを短く要約します。"
    ),
    instruction=(
        "与えられたテキストを短く要約してください。"
        "要約は簡潔で、重要な情報を含むようにしてください。"
        "出力は日本語で行ってください。"
        "要約以外のことはしないでください。"
    )
)
