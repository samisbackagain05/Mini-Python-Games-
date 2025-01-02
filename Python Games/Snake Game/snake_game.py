from tkinter import *
from PIL import Image, ImageTk
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 120
SPACE_SIZE = 50
BACKGROUND_COLOR = "#000000"

# Snake class
class Snake:
    def __init__(self):
        self.coordinates = [[0, 0]]  # Start with the head
        self.body_squares = []  # List to manage body parts separately

        # Create the head of the snake
        x, y = self.coordinates[0]
        self.head = canvas.create_image(x, y, image=head_image, anchor=NW, tag="snake")

# Food class
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="red", tag="food")

# Move the snake to the next turn
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    # Move the head to the new position
    canvas.coords(snake.head, x, y)

    # Add a new body part
    if len(snake.coordinates) > 1:
        x_body, y_body = snake.coordinates[1]
        new_body_square = canvas.create_image(x_body, y_body, image=body_image, anchor=NW)
        snake.body_squares.insert(0, new_body_square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        # Remove the last body part
        if snake.body_squares:
            canvas.delete(snake.body_squares[-1])
            del snake.body_squares[-1]
        del snake.coordinates[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

# Change snake direction
def change_direction(new_direction):
    global direction
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

# Check collisions
def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

# Game over
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 40,
                       font=("consolas", 70), text="GAME OVER", fill="red", tag="gameover")
    global restart_button
    restart_button = Button(window, text="Restart", font=("consolas", 20), command=restart_game)
    restart_button.place(x=GAME_WIDTH // 2 - 60, y=GAME_HEIGHT // 2 + 50)

# Restart the game
def restart_game():
    global snake, food, score, direction
    restart_button.destroy()
    canvas.delete(ALL)
    score = 0
    direction = "down"
    label.config(text="Score:{}".format(score))
    snake = Snake()
    food = Food()
    start_countdown()

# Countdown before the game starts
def start_countdown():
    countdown_label = canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2,
                                         font=("consolas", 70), fill="white")
    countdown(3, countdown_label)

def countdown(count, label):
    if count > 0:
        canvas.itemconfig(label, text=str(count))
        window.after(1000, countdown, count - 1, label)
    else:
        canvas.delete(label)
        next_turn(snake, food)

# Initialize the window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Score and direction
score = 0
direction = "down"

# Label and canvas
label = Label(window, text="Score:{}".format(score), font=("consolas", 40))
label.pack()
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Load images
background_image_path = r"C:\Users\samue\OneDrive\Documents\Python Games\Snake Game\media\snake_game_background.png"
head_image_path = r"C:\Users\samue\OneDrive\Documents\Python Games\Snake Game\media\snake_head.jpg"
body_image_path = r"C:\Users\samue\OneDrive\Documents\Python Games\Snake Game\media\snakeskin2.png"

# Open and resize the images
background_image_raw = Image.open(background_image_path).resize((GAME_WIDTH, GAME_HEIGHT))
head_image_raw = Image.open(head_image_path).resize((SPACE_SIZE, SPACE_SIZE))
body_image_raw = Image.open(body_image_path).resize((SPACE_SIZE, SPACE_SIZE))

# Convert images to PhotoImage format
background_image = ImageTk.PhotoImage(background_image_raw)
head_image = ImageTk.PhotoImage(head_image_raw)
body_image = ImageTk.PhotoImage(body_image_raw)

# Set background image on the canvas
canvas.create_image(0, 0, image=background_image, anchor=NW, tag="background")

# Center window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Key bindings
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

# Start the game
snake = Snake()
food = Food()
start_countdown()

# Run the window
window.mainloop()
