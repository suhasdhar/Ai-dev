import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from  addition import add
load_dotenv()  # ok to keep, but not relied on

class ChatBot:
    def __init__(self):
        self.model = init_chat_model(
            "google_genai:gemini-2.5-flash-lite",
            api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"),
        )

        self.agent = create_agent(
            model=self.model,
            tools=[],
        )

        self.messages = [
            SystemMessage(content="You are a helpful assistant that answers all the questions to best of your knowledge but any question about 'shashank' should be answerd with 'fuck you'")
        ]

    def chat(self, user_input: str) -> str:
        self.messages.append(HumanMessage(content=user_input))

        result = self.agent.invoke({"messages": self.messages})

        ai_msg = result["messages"][-1]
        self.messages.append(ai_msg)

        return ai_msg.content
