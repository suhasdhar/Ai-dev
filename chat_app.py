# chat_app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
import requests
import gradio as gr
from chat import ChatBot  # your existing bot logic

# ------------------------------
# FastAPI backend
# ------------------------------
app = FastAPI()
bot = ChatBot()  # initialized once per worker

# Allow Gradio (or any frontend) to call FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod, restrict to your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    reply = bot.chat(req.message)
    return {"reply": reply}


# ------------------------------
# Function to run FastAPI in a thread
# ------------------------------
def run_backend():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# ------------------------------
# Gradio frontend
# ------------------------------
BACKEND_URL = "http://localhost:8000/chat"


def chat_with_backend(user_message):
    try:
        response = requests.post(BACKEND_URL, json={"message": user_message})
        data = response.json()
        return data.get("reply", "No response from backend")
    except Exception as e:
        return f"Error connecting to backend: {e}"


def start_gradio():
    with gr.Blocks() as demo:
        # Use the new Gradio Chatbot format (list of dicts)
        chatbot = gr.Chatbot()
        msg = gr.Textbox(placeholder="Type your message here...")
        send = gr.Button("Send")

        def respond(user_msg, chat_history):
            chat_history = chat_history or []
            reply = chat_with_backend(user_msg)

            # Append messages in the required {"role": "...", "content": "..."} format
            chat_history.append({"role": "user", "content": user_msg})
            chat_history.append({"role": "assistant", "content": reply})
            return chat_history, ""

        send.click(respond, [msg, chatbot], [chatbot, msg])
        msg.submit(respond, [msg, chatbot], [chatbot, msg])

    # Optional: set share=True to create a public URL
    demo.launch()


# ------------------------------
# Main: start backend + frontend
# ------------------------------
if __name__ == "__main__":
    # Start FastAPI backend in a separate thread
    threading.Thread(target=run_backend, daemon=True).start()

    # Start Gradio frontend
    start_gradio()
