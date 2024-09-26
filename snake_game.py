import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame:
    def __init__(self, master, balance, colors):
        # Initialize the Snake game
        self.master = master
        self.balance = balance
        self.colors = colors
        self.width = 20
        self.height = 20
        self.cell_size = 20
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (1, 0)
        self.food = None
        self.bombs = []
        self.max_bombs = 40
        self.bomb_spawn_rate = 0.02
        self.score = 0
        self.game_running = False
        self.bet = 0
        self.message_label = None

    def play(self):
        # Main method to start the game
        self.create_game_screen()
        self.master.wait_window(self.game_window)
        return self.balance

    def create_game_screen(self):
        # Create the main game window and UI elements
        self.game_window = tk.Toplevel(self.master)
        self.game_window.title("Snake Game")
        self.game_window.configure(bg=self.colors['background'])

        # Display balance and score
        self.balance_label = tk.Label(self.game_window, text=f"Balance: ${self.balance:.2f}", 
                 font=("Arial", 14), bg=self.colors['background'], fg=self.colors['text'])
        self.balance_label.pack(pady=5)

        self.score_label = tk.Label(self.game_window, text="Score: 0", 
                                    font=("Arial", 14), bg=self.colors['background'], fg=self.colors['text'])
        self.score_label.pack(pady=5)

        # Bet input
        bet_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        bet_frame.pack(pady=5)
        tk.Label(bet_frame, text="Bet: $", bg=self.colors['background'], fg=self.colors['text']).pack(side=tk.LEFT)
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

        # Game canvas
        self.canvas = tk.Canvas(self.game_window, 
                                width=self.width * self.cell_size, 
                                height=self.height * self.cell_size, 
                                bg='black')
        self.canvas.pack(pady=10)

        # Start and return buttons
        button_frame = tk.Frame(self.game_window, bg=self.colors['background'])
        button_frame.pack(pady=10)

        start_button = tk.Button(button_frame, text="Start Game", command=self.start_game,
                                 bg=self.colors['secondary'], fg=self.colors['button_text'])
        start_button.pack(side=tk.LEFT, padx=5)

        return_button = tk.Button(button_frame, text="Return to Main Menu", command=self.return_to_main_menu,
                                  bg=self.colors['accent'], fg=self.colors['button_text'])
        return_button.pack(side=tk.LEFT, padx=5)

        # Bind arrow keys for snake control
        self.game_window.bind('<Left>', lambda e: self.change_direction((-1, 0)))
        self.game_window.bind('<Right>', lambda e: self.change_direction((1, 0)))
        self.game_window.bind('<Up>', lambda e: self.change_direction((0, -1)))
        self.game_window.bind('<Down>', lambda e: self.change_direction((0, 1)))

        # Add message label
        self.message_label = tk.Label(self.game_window, text="", font=("Arial", 12), 
                                      bg=self.colors['background'], fg=self.colors['text'], wraplength=280)
        self.message_label.pack(pady=10)

    def set_quick_bet(self, amount):
        # Set the bet amount to a predefined quick bet value
        if amount <= self.balance:
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(amount))
        else:
            self.show_message(f"Insufficient Funds. You don't have ${amount}. Your balance is ${self.balance:.2f}")

    def start_game(self):
        # Initialize and start the game
        try:
            self.bet = float(self.bet_entry.get())
            if self.bet <= 0 or self.bet > self.balance:
                raise ValueError
        except ValueError:
            self.show_message("Invalid Bet. Please enter a valid bet amount.")
            return

        self.balance -= self.bet
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (1, 0)
        self.score = 0
        self.bombs = []
        self.food = self.generate_food()
        self.game_running = True
        self.update()
        self.show_message("Game started! Use arrow keys to control the snake.")

    def generate_food(self):
        # Generate food at a random position
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake and food not in self.bombs:
                return food

    def generate_bomb(self):
        # Generate a bomb at a random position
        while True:
            bomb = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if bomb not in self.snake and bomb != self.food and bomb not in self.bombs:
                return bomb

    def change_direction(self, new_direction):
        # Change the snake's direction
        if self.game_running:
            if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
                self.direction = new_direction

    def move_snake(self):
        # Move the snake and check for collisions
        head = self.snake[0]
        new_head = ((head[0] + self.direction[0]) % self.width, 
                    (head[1] + self.direction[1]) % self.height)

        if new_head in self.snake or new_head in self.bombs:
            self.game_over()
            return False

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.food = self.generate_food()
            
            # Chance to spawn a new bomb
            if len(self.bombs) < self.max_bombs and random.random() < self.bomb_spawn_rate:
                self.bombs.append(self.generate_bomb())
        else:
            self.snake.pop()

        return True

    def update(self):
        # Main game loop
        if self.game_running:
            self.canvas.delete("all")
            self.draw_snake()
            self.draw_food()
            self.draw_bombs()

            if self.move_snake():
                self.game_window.after(100, self.update)
            else:
                self.game_over()

    def draw_snake(self):
        # Draw the snake on the canvas
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size, 
                                         (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
                                         fill='green', outline='darkgreen')

    def draw_food(self):
        # Draw the food on the canvas
        x, y = self.food
        self.canvas.create_oval(x * self.cell_size, y * self.cell_size, 
                                (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
                                fill='red', outline='darkred')

    def draw_bombs(self):
        # Draw the bombs on the canvas
        for bomb in self.bombs:
            x, y = bomb
            self.canvas.create_oval(x * self.cell_size, y * self.cell_size, 
                                    (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
                                    fill='black', outline='red')

    def game_over(self):
        # Handle game over
        self.game_running = False
        winnings = self.score * self.bet
        self.balance += winnings
        self.show_message(f"Game Over!\nYour score: {self.score}\nYou won ${winnings:.2f}!\nNew Balance: ${self.balance:.2f}")
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")
        self.game_window.after(3000, self.game_window.destroy)  # Close window after 3 seconds

    def return_to_main_menu(self):
        # Close the game window and return to the main menu
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

    def show_message(self, message):
        self.message_label.config(text=message)