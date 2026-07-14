from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


@app.get("/")
def home():
    return {"status": "Elite One Server Online 🚀"}


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    mensagem = data.get("mensagem", "Alerta recebido!")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": mensagem
        }
    )

    return {"ok": True}
