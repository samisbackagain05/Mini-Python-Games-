import tkinter as tk
import subprocess

def start_2_player_mode():
    subprocess.run(["python", "C:/Users/samue/OneDrive/Documents/Python Games/Pong Game/pong2playermode.py"])

def start_vs_ai():
    subprocess.run(["python", "C:/Users/samue/OneDrive/Documents/Python Games/Pong Game/pongai.py"])

# Create the main tkinter window
root = tk.Tk()
root.title("Pong Game")  # Set the window title

# Set the window size (optional)
root.geometry("300x200")

# Create buttons
button_2_player_mode = tk.Button(root, text="2 Player Mode", command=start_2_player_mode, font=("Arial", 14))
button_2_player_mode.pack(pady=20)  # Add some padding around the button

button_vs_ai = tk.Button(root, text="VS AI", command=start_vs_ai, font=("Arial", 14))
button_vs_ai.pack(pady=20)  # Add some padding around the button

# Start the tkinter main loop
root.mainloop()
