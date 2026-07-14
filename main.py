from fastapi import FastAPI, HTTPException, Request
import os
import requests

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


@app.get("/")
def home():
    return {"status": "Elite One Server Online 🚀"}


@app.get("/teste")
def teste_telegram():
    if not BOT_TOKEN or not CHAT_ID:
        raise HTTPException(
            status_code=500,
            detail="BOT_TOKEN ou CHAT_ID não configurado",
        )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    resposta = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": "🤖 ELITE ONE\n\n✅ Servidor conectado ao Telegram com sucesso!",
        },
        timeout=15,
    )

    if not resposta.ok:
        raise HTTPException(
            status_code=500,
            detail=resposta.json(),
        )

    return {"ok": True, "mensagem": "Mensagem enviada ao Telegram"}


@app.post("/webhook")
async def webhook(request: Request):
    if not BOT_TOKEN or not CHAT_ID:
        raise HTTPException(
            status_code=500,
            detail="BOT_TOKEN ou CHAT_ID não configurado",
        )

    try:
        dados = await request.json()
        mensagem = dados.get("mensagem", "Alerta recebido do TradingView")
    except Exception:
        corpo = await request.body()
        mensagem = corpo.decode("utf-8") or "Alerta recebido do TradingView"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    resposta = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": mensagem,
        },
        timeout=15,
    )

    if not resposta.ok:
        raise HTTPException(
            status_code=500,
            detail=resposta.json(),
        )

    return {"ok": True}
