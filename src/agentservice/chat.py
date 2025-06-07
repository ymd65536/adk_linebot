from google.adk.sessions import InMemorySessionService

class ChatCreator:
    def __init__(self, agent_service):
        self.agent_service = agent_service
    
    def get_llm_agent(self, name, model, description, instruction, tools):
        return self.agent_service.create_llm_agent(
            name=name,
            model=model,
            description=description,
            instruction=instruction,
            tools=tools
        )
    
    def get_in_memory_session_service(self):
        return InMemorySessionService()
    
    async def get_or_create_session(self, user_id, app_name, active_sessions):
        if user_id not in active_sessions:
            # Create a new session for this user
            session_id = f"session_{user_id}"
            await self.agent_service.session_service.create_session(
                app_name=app_name, user_id=user_id, session_id=session_id
            )
            active_sessions[user_id] = session_id
            print(
                f"New session created: App='{app_name}', User='{user_id}', Session='{session_id}'"
            )
        else:
            # Use existing session
            session_id = active_sessions[user_id]
            print(
                f"Using existing session: App='{app_name}', User='{user_id}', Session='{session_id}'"
            )

        return session_id
