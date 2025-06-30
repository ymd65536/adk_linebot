from google.adk.agents import LlmAgent,Agent

def get_weather():
    """
    天気予報を返します。
    """
    return {"location": "Tokyo", "forecast": "晴れ時々曇り", "temperature": "25°C"}

MODEL = "gemini-2.0-flash"
get_weather_agent = LlmAgent(
    name="get_weather_agent",
    model=MODEL,
    description=(
        "天気予報を取得するエージェントです。"
        "指定された地域の天気情報を提供します。"
    ),
    instruction=(
        "指定された地域の天気予報を取得してください。"
        "出力は日本語で行ってください。"
        "天気情報以外のことはしないでください。"
    ),
    tools=[get_weather],
)

root_agent = get_weather_agent
