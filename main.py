from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model


load_dotenv()

key = os.getenv("GEMINI_API_KEY");
os.environ["GOOGLE_API_KEY"] = key

model = init_chat_model("google_genai:gemini-2.5-flash-lite")

response = model.invoke("Why do parrots talk?")
print(response)