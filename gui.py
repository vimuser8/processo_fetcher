import tkinter as tk
"""
Copyright 2026 CRC/AL
Autor: Demerson Oliveira
Criado em: Fevereiro, 2026
Modificado em: Fevereiro, 2026

GUI em fase de teste.
"""
root = tk.Tk()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - WINDOW_WIDTH/2)
center_y = int(screen_height/2 - WINDOW_HEIGHT/2)

root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}')
root.resizable(False, False)

root.title("CRC-AL Processos")
app_icon = tk.PhotoImage(file="png/crcal_logo.png")
root.iconphoto(True, app_icon)

root.mainloop()

