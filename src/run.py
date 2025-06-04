import asyncio
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner

from agents.main_agent import agent
from agents.main_agent.sub_agents.hello_agent.agent import hello_agent
from agents.main_agent.sub_agents.summarize_agent.agent import summarize_agent

msg = """
文章の要約
Googleの新しいAIモデル「Gemini 2.0 Flash」は、特にモバイルデバイス向けに設計されており、迅速な応答と高い効率性を提供します。
このモデルは、テキスト生成、要約、翻訳などのタスクにおいて優れたパフォーマンスを発揮します。
Gemini 2.0 Flashは、ユーザーが求める情報を迅速に提供し、モバイル体験を向上させることを目指しています。
"""

user_id = "user_12345"


MODEL = "gemini-2.0-flash"
session_service = InMemorySessionService()
APP_NAME = "linebot_agent"
active_sessions = {}

main_agent = LlmAgent(
    name="line_bot",
    model=MODEL,
    description=("挨拶と要約を行うエージェントです。"),
    instruction="あいさつをして、要約を行うエージェントです。",
    tools=[
        AgentTool(agent=hello_agent),
        AgentTool(agent=summarize_agent),
    ],
)

runner = Runner(
    agent=main_agent,  # The agent we want to run
    app_name=APP_NAME,  # Associates runs with our app
    session_service=session_service,  # Uses our session manager
)

async def get_or_create_session(user_id):  # Make function async
    if user_id not in active_sessions:
        # Create a new session for this user
        session_id = f"session_{user_id}"
        # Add await for the async session creation
        await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        active_sessions[user_id] = session_id
        print(
            f"New session created: App='{APP_NAME}', User='{user_id}', Session='{session_id}'"
        )
    else:
        # Use existing session
        session_id = active_sessions[user_id]
        print(
            f"Using existing session: App='{APP_NAME}', User='{user_id}', Session='{session_id}'"
        )

    return session_id


async def call_agent_async(query: str, user_id: str) -> str:
    """Sends a query to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    session_id = await get_or_create_session(user_id)  # Add await
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response."  # Default

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    # Assuming text response in the first part
                    final_response_text = event.content.parts[0].text
                elif (
                    event.actions and event.actions.escalate
                ):  # Handle potential errors/escalations
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                # Add more checks here if needed (e.g., specific error codes)
                break  # Stop processing events once the final response is found
    except ValueError as e:
        # Handle errors, especially session not found
        print(f"Error processing request: {str(e)}")
        # Recreate session if it was lost
        if "Session not found" in str(e):
            active_sessions.pop(user_id, None)  # Remove the invalid session
            session_id = await get_or_create_session(
                user_id
            )  # Create a new one # Add await
            # Try again with the new session
            try:
                async for event in runner.run_async(
                    user_id=user_id, session_id=session_id, new_message=content
                ):
                    # Same event handling code as above
                    if event.is_final_response():
                        if event.content and event.content.parts:
                            final_response_text = event.content.parts[0].text
                        elif event.actions and event.actions.escalate:
                            final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                        break
            except Exception as e2:
                final_response_text = f"Sorry, I encountered an error: {str(e2)}"
        else:
            final_response_text = f"Sorry, I encountered an error: {str(e)}"
    return final_response_text

async def run():
    async def get_or_create_session(user_id):  # Make function async
        if user_id not in active_sessions:
            # Create a new session for this user
            session_id = f"session_{user_id}"
            # Add await for the async session creation
            await session_service.create_session(
                app_name=APP_NAME, user_id=user_id, session_id=session_id
            )
            active_sessions[user_id] = session_id
            print(
                f"New session created: App='{APP_NAME}', User='{user_id}', Session='{session_id}'"
            )
        else:
            # Use existing session
            session_id = active_sessions[user_id]
            print(
                f"Using existing session: App='{APP_NAME}', User='{user_id}', Session='{session_id}'"
            )

        return session_id

    print(f"Runner created for agent '{runner.agent.name}'.")
    response = await call_agent_async(msg, user_id)

    print(f"Final response: {response}")

if __name__ == "__main__":
    # Run the main function in an asyncio event loop
    asyncio.run(run())
    print("Run completed.")
