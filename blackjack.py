import tkinter as tk
import random
import time

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}" if self.suit != "Hidden" else "Hidden"

    def get_ascii_art(self):
        if self.suit == "Hidden":
            return [
                "┌─────┐",
                "│░░░░░│",
                "│░░░░░│",
                "│░░░░░│",
                "└─────┘"
            ]
        suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
        return [
            "┌─────┐",
            f"│{self.value:<2}   │",
            f"│  {suit_symbols[self.suit]}  │",
            f"│   {self.value:>2}│",
            "└─────┘"
        ]

class Blackjack:
    def __init__(self, master, balance, colors):
        self.master = master
        self.balance = balance
        self.colors = colors
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.bet = 0
        self.game_running = False
        self.message_label = None

    def play(self):
        self.create_game_screen()
        self.master.wait_window(self.game_window)
        return self.balance

    def create_game_screen(self):
        self.game_window = tk.Toplevel(self.master)
        self.game_window.title("Blackjack")
        self.game_window.configure(bg=self.colors['background'])
        self.game_window.geometry("360x640")  # Set a mobile-friendly size

        self.balance_label = tk.Label(self.game_window, text=f"Balance: ${self.balance:.2f}", 
                 font=("Arial", 16), bg=self.colors['background'], fg=self.colors['text'])
        self.balance_label.pack(pady=10)

        bet_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        bet_frame.pack(pady=10)
        tk.Label(bet_frame, text="Bet: $", font=("Arial", 14), bg=self.colors['background'], fg=self.colors['text']).pack(side=tk.LEFT)
        self.bet_entry = tk.Entry(bet_frame, width=10, font=("Arial", 14))
        self.bet_entry.pack(side=tk.LEFT)

        quick_bet_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        quick_bet_frame.pack(pady=10)

        quick_bets = [5, 10, 25, 50, 100]
        for amount in quick_bets:
            tk.Button(quick_bet_frame, text=f"${amount}", 
                      command=lambda x=amount: self.set_quick_bet(x),
                      font=("Arial", 12), width=5, height=2,
                      bg=self.colors['primary'], fg=self.colors['button_text']).pack(side=tk.LEFT, padx=2)

        tk.Button(quick_bet_frame, text="All In", 
                  command=lambda: self.set_quick_bet(self.balance),
                  font=("Arial", 12), width=5, height=2,
                  bg=self.colors['accent'], fg=self.colors['button_text']).pack(side=tk.LEFT, padx=2)

        self.start_button = tk.Button(self.game_window, text="Start Game", command=self.start_game,
                                      font=("Arial", 14), width=15, height=2,
                                      bg=self.colors['secondary'], fg=self.colors['button_text'])
        self.start_button.pack(pady=10)

        action_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        action_frame.pack(pady=10)

        self.hit_button = tk.Button(action_frame, text="Hit", command=self.hit, state=tk.DISABLED,
                                    font=("Arial", 14), width=10, height=2,
                                    bg=self.colors['primary'], fg=self.colors['button_text'])
        self.hit_button.pack(side=tk.LEFT, padx=5)

        self.stand_button = tk.Button(action_frame, text="Stand", command=self.stand, state=tk.DISABLED,
                                      font=("Arial", 14), width=10, height=2,
                                      bg=self.colors['primary'], fg=self.colors['button_text'])
        self.stand_button.pack(side=tk.LEFT, padx=5)

        self.dealer_label = tk.Label(self.game_window, text="Dealer's hand: ", font=("Arial", 14),
                                     bg=self.colors['background'], fg=self.colors['text'])
        self.dealer_label.pack(pady=5)

        self.dealer_cards_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        self.dealer_cards_frame.pack(pady=5)

        self.player_label = tk.Label(self.game_window, text="Your hand: ", font=("Arial", 14),
                                     bg=self.colors['background'], fg=self.colors['text'])
        self.player_label.pack(pady=5)

        self.player_cards_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        self.player_cards_frame.pack(pady=5)

        self.message_label = tk.Label(self.game_window, text="", font=("Arial", 14), 
                                      bg=self.colors['background'], fg=self.colors['text'], wraplength=320)
        self.message_label.pack(pady=10)

        tk.Button(self.game_window, text="Return to Main Menu", command=self.return_to_main_menu,
                  font=("Arial", 14), width=20, height=2,
                  bg=self.colors['accent'], fg=self.colors['button_text']).pack(pady=10)

    def set_quick_bet(self, amount):
        if amount <= self.balance:
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(amount))
        else:
            self.show_message(f"Insufficient Funds. You don't have ${amount}. Your balance is ${self.balance:.2f}")

    def start_game(self):
        try:
            self.bet = float(self.bet_entry.get())
            if self.bet <= 0 or self.bet > self.balance:
                raise ValueError
        except ValueError:
            self.show_message("Invalid Bet. Please enter a valid bet amount.")
            return

        self.balance -= self.bet
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

        self.deck = self.create_deck()
        random.shuffle(self.deck)

        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

        self.update_hands()
        self.update_card_display(animate=True)
        self.game_running = True
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

        if self.calculate_hand(self.player_hand) == 21:
            self.blackjack()

    def hit(self):
        new_card = self.deck.pop()
        self.player_hand.append(new_card)
        self.update_hands()
        self.update_card_display(animate=True, new_card=new_card)
        if self.calculate_hand(self.player_hand) > 21:
            self.bust()

    def stand(self):
        self.game_running = False
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        
        self.update_card_display(show_dealer=True, animate=True)
        
        while self.calculate_hand(self.dealer_hand) < 17:
            new_card = self.deck.pop()
            self.dealer_hand.append(new_card)
            self.update_hands()
            self.update_card_display(show_dealer=True, animate=True, new_card=new_card)
            self.game_window.update()
            time.sleep(1)
        
        self.check_winner()

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [Card(suit, value) for suit in suits for value in values]

    def calculate_hand(self, hand):
        value = 0
        aces = 0
        for card in hand:
            if card.value in ['J', 'Q', 'K']:
                value += 10
            elif card.value == 'A':
                aces += 1
            else:
                value += int(card.value)
        
        for _ in range(aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1
        
        return value

    def update_hands(self):
        self.player_label.config(text=f"Your hand: {', '.join(str(card) for card in self.player_hand)} (Value: {self.calculate_hand(self.player_hand)})")
        if self.game_running:
            self.dealer_label.config(text=f"Dealer's hand: {self.dealer_hand[0]}, Hidden")
        else:
            self.dealer_label.config(text=f"Dealer's hand: {', '.join(str(card) for card in self.dealer_hand)} (Value: {self.calculate_hand(self.dealer_hand)})")

    def update_card_display(self, show_dealer=False, animate=False, new_card=None):
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()

        if show_dealer:
            for card in self.dealer_hand:
                self.display_card(self.dealer_cards_frame, card, animate and card == new_card)
        else:
            self.display_card(self.dealer_cards_frame, self.dealer_hand[0])
            self.display_card(self.dealer_cards_frame, Card("Hidden", "?"))

        for card in self.player_hand:
            self.display_card(self.player_cards_frame, card, animate and card == new_card)

    def display_card(self, frame, card, animate=False):
        card_frame = tk.Frame(frame, bg=self.colors['background'])
        card_frame.pack(side=tk.LEFT, padx=2)
        
        ascii_art = card.get_ascii_art()
        labels = []
        for line in ascii_art:
            label = tk.Label(card_frame, text=line, font=("Courier", 8), bg=self.colors['background'], fg=self.colors['text'])
            labels.append(label)
            if animate:
                label.pack_forget()
            else:
                label.pack()

        if animate:
            for label in labels:
                label.pack()
                self.game_window.update()
                time.sleep(0.05)

    def blackjack(self):
        self.game_running = False
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        winnings = self.bet * 2.5
        self.balance += winnings
        self.show_message(f"Blackjack! You win ${winnings:.2f}!")
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")
        self.start_button.config(state=tk.NORMAL)
        self.update_card_display(show_dealer=True, animate=True)

    def bust(self):
        self.game_running = False
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.show_message(f"Bust! You lose ${self.bet:.2f}.")
        self.start_button.config(state=tk.NORMAL)
        self.update_card_display(show_dealer=True, animate=True)

    def check_winner(self):
        player_value = self.calculate_hand(self.player_hand)
        dealer_value = self.calculate_hand(self.dealer_hand)

        if dealer_value > 21:
            winnings = self.bet * 2
            self.balance += winnings
            self.show_message(f"Dealer busts! You win ${winnings:.2f}!")
        elif player_value > dealer_value:
            winnings = self.bet * 2
            self.balance += winnings
            self.show_message(f"You win ${winnings:.2f}!")
        elif player_value < dealer_value:
            self.show_message(f"Dealer wins. You lose ${self.bet:.2f}.")
        else:
            self.balance += self.bet
            self.show_message("It's a tie. Your bet is returned.")

        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")
        self.start_button.config(state=tk.NORMAL)
        self.update_card_display(show_dealer=True, animate=True)

    def show_message(self, message):
        self.message_label.config(text=message)

    def return_to_main_menu(self):
        if self.game_running:
            self.show_message("Are you sure you want to return to the main menu? Your current game will be lost.")
            yes_button = tk.Button(self.game_window, text="Yes", command=self.confirm_return)
            no_button = tk.Button(self.game_window, text="No", command=self.cancel_return)
            yes_button.pack(side=tk.LEFT, padx=5)
            no_button.pack(side=tk.LEFT, padx=5)
        else:
            self.game_window.destroy()

    def confirm_return(self):
        self.game_running = False
        self.game_window.destroy()

    def cancel_return(self):
        self.show_message("")
        for widget in self.game_window.winfo_children():
            if isinstance(widget, tk.Button) and widget['text'] in ["Yes", "No"]:
                widget.destroy()