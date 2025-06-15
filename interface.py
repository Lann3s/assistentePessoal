import tkinter as tk
import os
import sys
from calendar_utils import formatar_evento

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def criar_interface(eventos):
    janela = tk.Tk()
    janela.title("Assistente Diário")
    janela.geometry("450x600")
    janela.configure(bg="#f0f0f0")

    # Aplica o ícone na janela correta
    icon_path = resource_path("assets/icon.ico")
    janela.iconbitmap(icon_path)

    titulo = tk.Label(janela, text="Eventos de Hoje",
                      font=("Arial", 16, "bold"), bg="#f0f0f0")
    titulo.pack(pady=10)

    if not eventos:
        sem_eventos = tk.Label(
            janela, text="Nenhum evento encontrado.", font=("Arial", 12), bg="#f0f0f0")
        sem_eventos.pack(pady=20)
    else:
        for evento in eventos:
            texto = formatar_evento(evento)
            label = tk.Label(janela, text=texto, wraplength=400,
                     justify="left", bg="#f0f0f0", font=("Arial", 11))
            label.pack(anchor='w', padx=10, pady=4)

    janela.mainloop()
