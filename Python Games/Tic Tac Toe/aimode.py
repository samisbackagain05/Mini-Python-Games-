import tkinter as tk
from tkinter import messagebox

# Constants
X = "X"
O = "O"
EMPTY = " "
TIE = "TIE"
NUM_SQUARES = 9

# Function to display the instructions in a popup
def display_instructions():
    messagebox.showinfo("Tic-Tac-Toe Instructions", """
    Welcome to Tic-Tac-Toe, a showdown between a Human Brain and an
    Intelligent Computer. Choose your moves like this:
    
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    """)

# Function to check for the winner
def winner(board):
    WAYS_TO_WIN = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                   (0, 3, 6), (1, 4, 7), (2, 5, 8),
                   (0, 4, 8), (2, 4, 6))
    for row in WAYS_TO_WIN:
        if board[row[0]] == board[row[1]] == board[row[2]] != EMPTY:
            return board[row[0]]
    if EMPTY not in board:
        return TIE
    return None

# Function to get the legal moves (empty squares)
def legal_moves(board):
    moves = [i for i in range(NUM_SQUARES) if board[i] == EMPTY]
    return moves

# Function to make the human move
def human_move(board, human):
    move = None
    legal = legal_moves(board)
    while move not in legal:
        move = int(input(f"Where will you move? (0-8): "))
        if move not in legal:
            print("That square is already occupied, choose another.")
    return move

# Function to make the computer move
def computer_move(board, computer, human):
    board_copy = board[:]
    BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)
    for move in legal_moves(board_copy):
        board_copy[move] = computer
        if winner(board_copy) == computer:
            return move
        board_copy[move] = EMPTY
    for move in legal_moves(board_copy):
        board_copy[move] = human
        if winner(board_copy) == human:
            return move
        board_copy[move] = EMPTY
    for move in BEST_MOVES:
        if move in legal_moves(board_copy):
            return move

# Function to handle game over and update the score
def game_over(winner, computer, human, score, score_label):
    if winner == computer:
        score['computer'] += 1
        messagebox.showinfo("Game Over", f"You lost to me you buffoon! Score: {score['computer']}-{score['human']}")
    elif winner == human:
        score['human'] += 1
        messagebox.showinfo("Game Over", f"AI the smartest? We made you! Score: {score['computer']}-{score['human']}")
    elif winner == TIE:
        messagebox.showinfo("Game Over", "It's a tie! GGs!!")
    
    # Update the scoreboard label after the game ends
    score_label.config(text=f"Player: {score['human']}  |  AI: {score['computer']}")

# Function to handle the board update and player turns
def play_game(window):
    board = [EMPTY] * 9  # Initialize the board
    human = O
    computer = X
    turn = X

    # Create a new window for the game
    game_window = tk.Tk()
    game_window.title("VS AI Mode")

    # Create a central frame for the layout
    central_frame = tk.Frame(game_window)
    central_frame.pack(padx=20, pady=20)

    # Add a title above the board
    title_label = tk.Label(central_frame, text="VS AI", font=("Arial", 24, "bold"))
    title_label.pack(pady=10)

    # Create a frame for the scoreboard
    score_frame = tk.Frame(central_frame)
    score_frame.pack(pady=10)

    # Initialize score dictionary
    score = {'computer': 0, 'human': 0}
    
    # Display the scores
    score_label = tk.Label(score_frame, text=f"Player: {score['human']}  |  AI: {score['computer']}", font=("Arial", 16))
    score_label.pack()

    # Create a frame for the game buttons (board)
    board_frame = tk.Frame(central_frame)
    board_frame.pack()

    # Create the game buttons (grid)
    buttons = []
    for i in range(NUM_SQUARES):
        button = tk.Button(board_frame, text=EMPTY, width=10, height=3, font=("Arial", 24), command=lambda i=i: on_click(i))
        button.grid(row=i//3, column=i%3, padx=5, pady=5)
        buttons.append(button)

    # Function to handle button clicks for human moves
    def on_click(i):
        nonlocal turn
        if board[i] == EMPTY:
            board[i] = human
            buttons[i].config(text=human, state="disabled")
            winner_check = winner(board)
            if winner_check:
                game_over(winner_check, computer, human, score, score_label)
                reset_board()  # Reset the board after the game ends
            else:
                turn = X
                computer_turn()

    # Function for the computer's turn
    def computer_turn():
        nonlocal turn
        if turn == computer:
            move = computer_move(board, computer, human)
            board[move] = computer
            buttons[move].config(text=computer, state="disabled")
            winner_check = winner(board)
            if winner_check:
                game_over(winner_check, computer, human, score, score_label)
                reset_board()  # Reset the board after the game ends
            else:
                turn = O

    # Function to reset the board after the game ends
    def reset_board():
        nonlocal board
        board = [EMPTY] * 9
        for button in buttons:
            button.config(text=EMPTY, state="normal")
        game_window.update()

    # Start the game with the computer's turn if needed
    if computer == X:
        computer_turn()

    # Start the Tkinter main loop
    game_window.mainloop()
