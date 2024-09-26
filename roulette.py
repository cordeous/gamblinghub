import tkinter as tk
import random
import math
import time

class Roulette:
    def __init__(self, master, balance, colors):
        self.master = master
        self.balance = balance
        self.colors = colors
        self.history = []
        self.bets = []
        self.message_label = None

    def play(self):
        self.create_game_screen()
        self.master.wait_window(self.game_window)
        return self.balance

    def create_game_screen(self):
        self.game_window = tk.Toplevel(self.master)
        self.game_window.title("Roulette")
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

        self.bet_type_var = tk.StringVar(self.game_window)
        self.bet_type_var.set("Color")
        tk.OptionMenu(self.game_window, self.bet_type_var, "Color", "Number", command=self.update_bet_options).pack(pady=5)

        self.bet_value_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        self.bet_value_frame.pack(pady=5)
        self.update_bet_options()

        tk.Button(self.game_window, text="Add Bet", command=self.add_bet,
                  bg=self.colors['secondary'], fg=self.colors['button_text']).pack(pady=5)

        self.bets_label = tk.Label(self.game_window, text="Current Bets: ", font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text'])
        self.bets_label.pack(pady=5)

        tk.Button(self.game_window, text="Spin", command=self.spin_wheel,
                  bg=self.colors['secondary'], fg=self.colors['button_text']).pack(pady=10)

        self.result_label = tk.Label(self.game_window, text="", font=("Arial", 14), bg=self.colors['background'], fg=self.colors['text'])
        self.result_label.pack(pady=5)

        self.history_label = tk.Label(self.game_window, text="History: ", font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text'])
        self.history_label.pack(pady=5)

        self.message_label = tk.Label(self.game_window, text="", font=("Arial", 12), 
                                      bg=self.colors['background'], fg=self.colors['text'], wraplength=280)
        self.message_label.pack(pady=10)

        tk.Button(self.game_window, text="Return to Main Menu", command=self.return_to_main_menu,
                  bg=self.colors['accent'], fg=self.colors['button_text']).pack(pady=10)

        self.canvas = tk.Canvas(self.game_window, width=300, height=300, bg='white')
        self.canvas.pack(pady=10)
        self.draw_wheel()

    def set_quick_bet(self, amount):
        if amount <= self.balance:
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(amount))
        else:
            self.show_message(f"Insufficient Funds. You don't have ${amount}. Your balance is ${self.balance:.2f}")

    def update_bet_options(self, *args):
        for widget in self.bet_value_frame.winfo_children():
            widget.destroy()

        if self.bet_type_var.get() == "Color":
            self.bet_value_var = tk.StringVar(self.game_window)
            self.bet_value_var.set("Red")
            tk.OptionMenu(self.bet_value_frame, self.bet_value_var, "Red", "Black", "Green").pack()
        else:
            self.bet_value_var = tk.StringVar(self.game_window)
            self.bet_value_var.set("0")
            tk.Spinbox(self.bet_value_frame, from_=0, to=36, textvariable=self.bet_value_var, width=5).pack()

    def add_bet(self):
        try:
            bet_amount = float(self.bet_entry.get())
            if bet_amount <= 0 or bet_amount > self.balance:
                raise ValueError
        except ValueError:
            self.show_message("Invalid Bet. Please enter a valid bet amount.")
            return

        bet_type = self.bet_type_var.get()
        bet_value = self.bet_value_var.get()
        self.bets.append((bet_amount, bet_type, bet_value))
        self.balance -= bet_amount
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")
        self.update_bets_label()

    def update_bets_label(self):
        bets_text = "Current Bets: " + " | ".join([f"${bet[0]} on {bet[2]} ({bet[1]})" for bet in self.bets])
        self.bets_label.config(text=bets_text)

    def draw_wheel(self):
        self.canvas.delete("all")
        center_x, center_y = 150, 150
        radius = 140
        self.canvas.create_oval(10, 10, 290, 290, fill='green', outline='white')
        
        numbers = list(range(37))
        for i, number in enumerate(numbers):
            angle = i * (360 / 37) * math.pi / 180
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            color = 'red' if number % 2 == 1 else 'black'
            if number == 0:
                color = 'green'
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=color)
            self.canvas.create_text(x, y, text=str(number), fill='white')

    def spin_wheel(self):
        if not self.bets:
            self.show_message("Please place at least one bet before spinning.")
            return

        result = random.randint(0, 36)
        color = "Red" if result % 2 == 1 else "Black"
        if result == 0:
            color = "Green"

        # Animate the wheel spinning
        spins = 50
        for _ in range(spins):
            self.canvas.delete("ball")
            angle = random.uniform(0, 2 * math.pi)
            x = 150 + 120 * math.cos(angle)
            y = 150 + 120 * math.sin(angle)
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='white', tags="ball")
            self.canvas.update()
            self.master.after(50)

        # Show final result
        angle = result * (360 / 37) * math.pi / 180
        x = 150 + 120 * math.cos(angle)
        y = 150 + 120 * math.sin(angle)
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='white', tags="ball")

        self.result_label.config(text=f"Result: {result} {color}")

        total_winnings = 0
        for bet_amount, bet_type, bet_value in self.bets:
            if (bet_type == "Color" and bet_value == color) or (bet_type == "Number" and int(bet_value) == result):
                winnings = bet_amount * (2 if bet_type == "Color" else 35)
                total_winnings += winnings

        if total_winnings > 0:
            self.balance += total_winnings
            self.show_message(f"You won ${total_winnings:.2f}!")
        else:
            self.show_message("You lost all bets.")

        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")
        self.history.append(f"{result} {color}")
        self.history = self.history[-10:]
        self.history_label.config(text="History: " + " | ".join(self.history))

        self.bets = []
        self.update_bets_label()

    def show_message(self, message):
        self.message_label.config(text=message)

    def return_to_main_menu(self):
        self.game_window.destroy()