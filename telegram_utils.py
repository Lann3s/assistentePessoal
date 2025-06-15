import requests
from config import TELEGRAM_TOKEN, CHAT_ID
from calendar_utils import formatar_evento

def send_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)

    if not response.ok:
        print("Erro ao enviar mensagem:", response.text)

def enviar_eventos_telegram(eventos):
    if not eventos:
        send_message("Salve! Você não tem eventos marcados para hoje. 😎")
    else:
        mensagem = "📅 *Eventos de hoje:*\n\n"
        for evento in eventos:
            mensagem += f"• {formatar_evento(evento)}\n"
        send_message(mensagem)