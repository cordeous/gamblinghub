import tkinter as tk
from tkinter import messagebox, ttk
from horse_racing import HorseRacing
from roulette import Roulette
from slot_machine import SlotMachine
from snake_game import SnakeGame
from blackjack import Blackjack  # Add this import

COLORS = {
    'background': '#F0F4F8',
    'primary': '#3498DB',
    'secondary': '#2ECC71',
    'accent': '#E74C3C',
    'text': '#2C3E50',
    'button_text': '#FFFFFF'
}

class GamblingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gambling App")
        self.geometry("360x640")
        self.configure(bg=COLORS['background'])
        self.balance = 1000
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        
        self.balance_label = tk.Label(self, text=f"Balance: ${self.balance:.2f}", 
                                      font=("Arial", 16), bg=COLORS['background'], fg=COLORS['text'])
        self.balance_label.pack(pady=10)

        games = [
            ("Horse Racing", self.show_horse_racing),
            ("Roulette", self.show_roulette),
            ("Slot Machine", self.show_slot_machine),
            ("Snake Game", self.show_snake_game),
            ("Blackjack", self.show_blackjack)  # Add this line
        ]

        for game_name, game_command in games:
            button = tk.Button(self, text=game_name, command=game_command,
                               font=("Arial", 12), width=15, height=2,
                               bg=COLORS['primary'], fg=COLORS['button_text'], 
                               activebackground=COLORS['secondary'])
            button.pack(pady=5)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_horse_racing(self):
        game = HorseRacing(self, self.balance, COLORS)
        self.balance = game.play()
        self.update_balance()

    def show_roulette(self):
        game = Roulette(self, self.balance, COLORS)
        self.balance = game.play()
        self.update_balance()

    def show_slot_machine(self):
        game = SlotMachine(self, self.balance, COLORS)
        self.balance = game.play()
        self.update_balance()

    def show_snake_game(self):
        game = SnakeGame(self, self.balance, COLORS)
        self.balance = game.play()
        self.update_balance()

    def show_blackjack(self):
        game = Blackjack(self, self.balance, COLORS)
        self.balance = game.play()
        self.update_balance()

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

if __name__ == "__main__":
    app = GamblingApp()
    app.mainloop()