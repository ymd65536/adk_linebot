from get_weather_agent.agent import root_agent
from vertexai.preview import reasoning_engines


app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=False,
)

session = app.create_session(
    user_id="user_12345",
)

for event in app.stream_query(
    user_id="user_12345",
    session_id=session.id,
    message="今日の天気を教えてください。",
):
    print(event)
