import tkinter as tk
import random
import time

colors = {
    1: "green",
    2: "red",
    3: "blue",
    4: "yellow",
    5: "purple",
    6: "orange",
    7: "pink",
    8: "brown",
    9: "gray"
}

board = []  # Lista para almacenar la secuencia del juego
player_input = []  # Lista para almacenar la entrada del jugador
score = 0  # Contador de puntaje

# Configuración de la ventana principal
window = tk.Tk()
window.title("Simon 3x3")
window.geometry("400x400")

def generate_sequence():
    global board
    board = random.sample(list(colors.keys()), 9)  # Generar una secuencia aleatoria de 9 elementos

def show_sequence():
    for i, color_idx in enumerate(board):
        button = buttons[i]
        button.config(bg=colors[color_idx])  # Iluminar el botón con el color correspondiente
        window.update()  # Actualizar la ventana para mostrar el cambio
        time.sleep(1)  # Esperar 1 segundo antes de apagar el color
        button.config(bg="lightgray")  # Apagar el botón

def check_player_input():
    global score, player_input, board
    if player_input == board[:len(player_input)]:
        score += 1
        print(f"¡Correcto! Puntaje: {score}")
        player_input.clear()  # Limpiar la entrada del jugador
        window.after(1000, show_sequence)  # Mostrar la secuencia nuevamente después de 1 segundo
    else:
        print(f"¡Incorrecto! Game Over. Puntaje final: {score}")
        window.destroy()  # Cerrar la ventana al finalizar el juego

def handle_button_click(color):
    player_input.append(color)
    print(f"Entrada del jugador: {player_input}")
    if len(player_input) == len(board):
        check_player_input()  # Verificar la entrada del jugador después de que complete la secuencia

def create_button(color, row, col):
    button = tk.Button(window, bg="lightgray", width=8, height=4, command=lambda c=color: handle_button_click(c))
    button.grid(row=row, column=col, padx=5, pady=5)
    return button

# Crear botones del tablero
buttons = []
for idx, color_idx in enumerate(random.sample(list(colors.keys()), 9)):
    row, col = divmod(idx, 3)
    button = create_button(color_idx, row, col)
    buttons.append(button)

# Botón para iniciar el juego
start_button = tk.Button(window, text="Iniciar", command=lambda: [generate_sequence(), show_sequence()])
start_button.grid(row=3, columnspan=3, pady=10)

# Mostrar la ventana principal
window.mainloop()