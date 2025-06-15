import schedule
import time
from telegram_utils import send_message

def lembrete_agua():
    send_message("🚰 Hora de tomar uma água!")

def lembrete_postura():
    send_message("🧍 Dá uma alongada aí! Mantenha a postura.")

def iniciar_agendamentos(eventos):
    schedule.every(1).hours.do(lembrete_agua)
    schedule.every(90).minutes.do(lembrete_postura)

    # Roda o agendador em paralelo (só se quiser rodar junto da interface)
    import threading
    def rodar_agendador():
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    thread = threading.Thread(target=rodar_agendador, daemon=True)
    thread.start()
