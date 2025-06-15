from calendar_utils import get_calendar_service, get_today_events
from telegram_utils import send_message
from interface import criar_interface
from scheduler import iniciar_agendamentos
from telegram_utils import enviar_eventos_telegram


def main():
    service = get_calendar_service()
    eventos = get_today_events(service)

    # Envia os eventos por Telegram
    enviar_eventos_telegram(eventos)

    # Começa o timer para enviar os lembretes
    iniciar_agendamentos(eventos)

    # Abre a janela
    criar_interface(eventos)


if __name__ == "__main__":
    main()
