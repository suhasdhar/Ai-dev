from fastapi import FastAPI
from pydantic import BaseModel
from chat import ChatBot

app = FastAPI()
bot = ChatBot()  # initialized once per worker

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    reply = bot.chat(req.message)
    return {"reply": reply}
