import tkinter as tk
from tkinter import messagebox
import random
import time

class SlotMachine:
    def __init__(self, master, balance, colors):
        # Initialize the Slot Machine game
        self.master = master
        self.balance = balance
        self.colors = colors
        self.symbols = [
            ("red", "🍒"), ("yellow", "🍋"), ("orange", "🍊"),
            ("purple", "🍇"), ("cyan", "💎"), ("gold", "7️⃣")
        ]
        self.message_label = None

    def play(self):
        # Main method to start the game
        self.create_game_screen()
        self.master.wait_window(self.game_window)
        return self.balance

    def create_game_screen(self):
        # Create the main game window and UI elements
        self.game_window = tk.Toplevel(self.master)
        self.game_window.title("Slot Machine")
        self.game_window.configure(bg=self.colors['background'])

        # Display balance
        self.balance_label = tk.Label(self.game_window, text=f"Balance: ${self.balance:.2f}", 
                 font=("Arial", 14), bg=self.colors['background'], fg=self.colors['text'])
        self.balance_label.pack(pady=5)

        # Bet input
        bet_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        bet_frame.pack(pady=5)
        tk.Label(bet_frame, text="Bet amount: $", bg=self.colors['background'], fg=self.colors['text']).pack(side=tk.LEFT)
        self.bet_entry = tk.Entry(bet_frame, width=10)
        self.bet_entry.pack(side=tk.LEFT)

        # Quick bet buttons
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

        # Spin button
        tk.Button(self.game_window, text="Spin", command=self.spin_reels,
                  bg=self.colors['secondary'], fg=self.colors['button_text']).pack(pady=10)

        # Slot machine display
        self.canvas = tk.Canvas(self.game_window, width=300, height=200, bg='white')
        self.canvas.pack(pady=10)

        # Create initial reel display
        self.reels = []
        for i in range(3):
            reel = self.canvas.create_rectangle(100 * i, 50, 100 * (i + 1), 150, fill="white")
            self.reels.append(reel)

        # Add message label
        self.message_label = tk.Label(self.game_window, text="", font=("Arial", 12), 
                                      bg=self.colors['background'], fg=self.colors['text'], wraplength=280)
        self.message_label.pack(pady=10)

        # Return to main menu button
        tk.Button(self.game_window, text="Return to Main Menu", command=self.return_to_main_menu,
                  bg=self.colors['accent'], fg=self.colors['button_text']).pack(pady=10)

    def set_quick_bet(self, amount):
        # Set the bet amount to a predefined quick bet value
        if amount <= self.balance:
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(amount))
        else:
            self.show_message(f"Insufficient Funds. You don't have ${amount}. Your balance is ${self.balance:.2f}")

    def spin_reels(self):
        # Main game logic for spinning the reels and determining results
        try:
            bet = float(self.bet_entry.get())
            if bet <= 0 or bet > self.balance:
                raise ValueError
        except ValueError:
            self.show_message("Invalid Bet. Please enter a valid bet amount.")
            return

        self.balance -= bet
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

        # Animate the spinning reels
        spin_time = 2
        frames = 20
        final_symbols = random.choices(self.symbols, k=3)

        for frame in range(frames):
            for i, reel in enumerate(self.reels):
                if frame < frames - 3 + i:
                    color, _ = random.choice(self.symbols)
                else:
                    color, _ = final_symbols[i]
                self.canvas.itemconfig(reel, fill=color)
            self.game_window.update()
            time.sleep(spin_time / frames)

        # Display final symbols
        for i, (color, symbol) in enumerate(final_symbols):
            self.canvas.create_text(50 + i * 100, 100, text=symbol, font=("Arial", 44))

        # Determine winnings
        if all(symbol == final_symbols[0] for symbol in final_symbols):
            multiplier = self.symbols.index(final_symbols[0]) + 3
            winnings = bet * multiplier
            self.balance += winnings
            self.show_message(f"Jackpot! All {final_symbols[0][1]}\nMultiplier: {multiplier}x\nYou won ${winnings:.2f}!")
        elif final_symbols.count(final_symbols[0]) == 2 or final_symbols.count(final_symbols[1]) == 2:
            winnings = bet * 2
            self.balance += winnings
            self.show_message(f"Two of a kind!\nYou won ${winnings:.2f}!")
        else:
            self.show_message(f"No match. You lost ${bet:.2f}.")

        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

    def show_message(self, message):
        self.message_label.config(text=message)

    def return_to_main_menu(self):
        # Close the game window and return to the main menu
        self.game_window.destroy()