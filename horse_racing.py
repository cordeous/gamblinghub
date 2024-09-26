import tkinter as tk
from tkinter import messagebox
import random
import time

class HorseRacing:
    def __init__(self, master, balance, colors):
        self.master = master
        self.balance = balance
        self.colors = colors
        self.horses = ['Red Rider', 'Blue Bolt', 'Green Galloper', 'Yellow Yonder']
        self.message_label = None

    def play(self):
        self.create_game_screen()
        self.master.wait_window(self.game_window)
        return self.balance

    def create_game_screen(self):
        self.game_window = tk.Toplevel(self.master)
        self.game_window.title("Horse Racing")
        self.game_window.configure(bg=self.colors['background'])

        self.balance_label = tk.Label(self.game_window, text=f"Balance: ${self.balance:.2f}", 
                 font=("Arial", 14), bg=self.colors['background'], fg=self.colors['text'])
        self.balance_label.pack(pady=5)

        bet_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        bet_frame.pack(pady=5)
        tk.Label(bet_frame, text="Bet amount: $", bg=self.colors['background'], fg=self.colors['text']).pack(side=tk.LEFT)
        self.bet_entry = tk.Entry(bet_frame, width=10)
        self.bet_entry.pack(side=tk.LEFT)

        quick_bet_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        quick_bet_frame.pack(pady=5)

        quick_bets = [5, 10, 25, 50, 100]
        for amount in quick_bets:
            tk.Button(quick_bet_frame, text=f"${amount}", 
                      command=lambda x=amount: self.set_quick_bet(x),
                      bg=self.colors['primary'], fg=self.colors['button_text']).pack(side=tk.LEFT, padx=2)

        tk.Button(quick_bet_frame, text="All In", 
                  command=lambda: self.set_quick_bet(self.balance),
                  bg=self.colors['accent'], fg=self.colors['button_text']).pack(side=tk.LEFT, padx=2)

        self.horse_var = tk.StringVar(self.game_window)
        self.horse_var.set(self.horses[0])
        tk.OptionMenu(self.game_window, self.horse_var, *self.horses).pack(pady=5)

        tk.Button(self.game_window, text="Start Race", command=self.run_race,
                  bg=self.colors['secondary'], fg=self.colors['button_text']).pack(pady=10)

        self.canvas = tk.Canvas(self.game_window, width=300, height=200, bg='white')
        self.canvas.pack(pady=10)

        self.message_label = tk.Label(self.game_window, text="", font=("Arial", 12), 
                                      bg=self.colors['background'], fg=self.colors['text'], wraplength=280)
        self.message_label.pack(pady=10)

        tk.Button(self.game_window, text="Return to Main Menu", command=self.return_to_main_menu,
                  bg=self.colors['accent'], fg=self.colors['button_text']).pack(pady=10)

    def set_quick_bet(self, amount):
        if amount <= self.balance:
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(amount))
        else:
            self.show_message(f"Insufficient Funds. You don't have ${amount}. Your balance is ${self.balance:.2f}")

    def run_race(self):
        try:
            bet = float(self.bet_entry.get())
            if bet <= 0 or bet > self.balance:
                raise ValueError
        except ValueError:
            self.show_message("Invalid Bet. Please enter a valid bet amount.")
            return

        # Clear the previous message
        self.show_message("")

        chosen_horse = self.horse_var.get()
        self.balance -= bet
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

        self.canvas.delete("all")
        horse_objects = []
        for i, horse in enumerate(self.horses):
            y = 50 * i + 25
            self.canvas.create_line(0, y, 300, y, fill='black')
            self.canvas.create_text(10, y - 15, text=horse, anchor='w')
            horse_objects.append(self.canvas.create_oval(0, y-10, 20, y+10, fill=horse.split()[0].lower()))

        winner = None
        while not winner:
            for i, horse in enumerate(horse_objects):
                move = random.randint(0, 10)
                self.canvas.move(horse, move, 0)
                if self.canvas.coords(horse)[2] >= 300:
                    winner = self.horses[i]
                    break
            self.game_window.update()
            time.sleep(0.05)

        if winner == chosen_horse:
            winnings = bet * 4
            self.balance += winnings
            self.show_message(f"Your horse won! You won ${winnings:.2f}!")
        else:
            self.show_message(f"Your horse lost. The winner was {winner}.")

        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

    def show_message(self, message):
        self.message_label.config(text=message)

    def return_to_main_menu(self):
        self.game_window.destroy()
