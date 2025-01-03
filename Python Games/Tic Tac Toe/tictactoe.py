import tkinter as tk
import aimode  # Import the VS AI game logic
import _2playermode  # Import the 2-player game logic

# Create the main Tkinter window
window = tk.Tk()

# Set the window title
window.title("Tic Tac Toe")

# Function to start 2-player mode
def start_2_player_mode():
    window.withdraw()  # Hide the main window
    _2playermode.play_game(window)  # Directly call the game function (no need to pass window)
    window.deiconify()  # Show the main window again after the game ends

# Function to start VS AI mode
def start_vs_ai():
    window.withdraw()  # Hide the main window
    aimode.play_game(window)  # Start the VS AI game from aimode.py
    window.deiconify()  # Show the main window again after the game ends

# Function to create the main menu window
def create_main_menu():
    # Create a frame for the title
    title_frame = tk.Frame(window)
    title_frame.pack(pady=20)

    # Add the title label above the buttons
    title_label = tk.Label(title_frame, text="Tic Tac Toe", font=("Arial", 24, "bold"))
    title_label.pack()

    # Create a frame for the buttons
    button_frame = tk.Frame(window)
    button_frame.pack(pady=20)

    # Add the "2 Player Mode" button
    player_button = tk.Button(button_frame, text="2 Player Mode", font=("Arial", 16), command=start_2_player_mode)
    player_button.pack(pady=10)

    # Add the "VS AI" button
    ai_button = tk.Button(button_frame, text="VS AI", font=("Arial", 16), command=start_vs_ai)
    ai_button.pack(pady=10)

    # Start the Tkinter main loop
    window.mainloop()

# Create the main menu
create_main_menu()
