import tkinter as tk
from tkinter import messagebox

# Constants for empty, X, and O
EMPTY = " "
X = "X"
O = "O"

# Initialize the game board (3x3)
board = [EMPTY] * 9

# Score variables
player1_score = 0
player2_score = 0

# Function to update the scoreboard display
def update_scoreboard():
    player1_score_label.config(text=f"Player 1 (O): {player1_score}")
    player2_score_label.config(text=f"Player 2 (X): {player2_score}")

# Function to check for a winner
def check_winner():
    # Check all winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] != EMPTY:
            return True
    return False

# Function to reset the board
def reset_board():
    global board
    board = [EMPTY] * 9
    for button in buttons:
        button.config(text=EMPTY)

# Function to handle button click
def on_click(i):
    global player1_score, player2_score
    if board[i] == EMPTY:
        # Alternate between O (Player 1) and X (Player 2)
        current_player = O if board.count(X) > board.count(O) else X
        board[i] = current_player

        # Update the button text based on the board state
        color = "blue" if current_player == O else "red"
        buttons[i].config(text=current_player, fg=color)

        # Check if there's a winner
        if check_winner():
            winner = "Player 1 (O)" if current_player == O else "Player 2 (X)"
            messagebox.showinfo("Game Over", f"{winner} wins!")
            if current_player == O:
                player1_score += 1
            else:
                player2_score += 1
            update_scoreboard()
            reset_board()
        elif EMPTY not in board:
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()

# Function to display the instructions popup window
def show_instructions():
    messagebox.showinfo("Tic-Tac-Toe Instructions", """
    Welcome to Tic-Tac-Toe!
    
    - The game is played on a 3x3 grid.
    - Player 1 (O) is blue and Player 2 (X) is red.
    - Players take turns to place their mark (X or O) in an empty space.
    - The first player to get 3 marks in a row (horizontally, vertically, or diagonally) wins.
    - If the grid is full and no one has won, the game is a draw.
    
    Click 'OK' to start playing.
    """)

# Function to go back to the main menu
def go_back(window, game_window):
    game_window.destroy()  # Close the game window
    window.deiconify()  # Show the main window again

# Function to start the 2-player game
def play_game(window):
    global buttons, board
    # Show instructions on first run
    show_instructions()

    board = [EMPTY] * 9
    buttons = []

    # Create the game window for 2-player mode
    game_window = tk.Tk()
    game_window.title("2 Player Mode")

    # Create a frame for the title
    title_frame = tk.Frame(game_window)
    title_frame.pack(pady=10)

    # Add the title label above the scoreboard
    title_label = tk.Label(title_frame, text="2 Player Mode", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # Create a frame for the scoreboard and place it below the title
    scoreboard_frame = tk.Frame(game_window)
    scoreboard_frame.pack(pady=10)

    # Create the scoreboard labels
    global player1_score_label, player2_score_label
    player1_score_label = tk.Label(scoreboard_frame, text=f"Player 1 (O): {player1_score}", font=("Arial", 14), fg="blue")
    player1_score_label.pack(pady=5)

    player2_score_label = tk.Label(scoreboard_frame, text=f"Player 2 (X): {player2_score}", font=("Arial", 14), fg="red")
    player2_score_label.pack(pady=5)

    # Create a frame for the game grid and center it
    game_frame = tk.Frame(game_window)
    game_frame.pack(pady=20)

    # Create the Tic-Tac-Toe grid buttons
    for i in range(9):
        button = tk.Button(game_frame, text=EMPTY, width=10, height=3, font=("Arial", 24), bg="lightgray", command=lambda i=i: on_click(i))
        button.grid(row=i // 3, column=i % 3, padx=5, pady=5)  # Adds padding between buttons
        buttons.append(button)

    # Add the "Back" button to go back to the main menu
    back_button = tk.Button(game_window, text="Back", font=("Arial", 14), command=lambda: go_back(window, game_window))
    back_button.pack(pady=20, anchor="ne", padx=20)  # Positioned at the top right corner

    # Start the Tkinter event loop for the game window
    game_window.mainloop()

    # Return the final result after the game ends
    return "Game Over - Check the result in the messagebox."
