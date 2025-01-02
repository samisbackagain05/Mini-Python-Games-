import tkinter as tk
from tkinter import Canvas, Label, StringVar, messagebox
from random import choice


class Game:
    BOX_SIZE = 20  # Size of each block (square)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tetris")

        # Make the window full screen (or set a fixed size)
        self.WIDTH = 300  # Full screen width
        self.HEIGHT = 500  # Full screen height
        self.LINE_WIDTH = 14  # Number of blocks per complete line to trigger removal
        self.START_POINT = self.WIDTH // 2 - self.BOX_SIZE  # Start position for shapes

        self.level = 1
        self.score = 0
        self.high_score = 0
        self.speed = 500
        self.counter = 0
        self.create_new_game = True
        self.timer_seconds = 0  # Timer for the game duration

        # Frame to hold score, level, and time at the top
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Score and Level
        self.status_var = StringVar()
        self.status_var.set("Level: 1, Score: 0")
        self.status = Label(
            top_frame,
            textvariable=self.status_var,
            font=("Helvetica", 10, "bold"),
        )
        self.status.pack(side=tk.LEFT)

        # High Score Display
        self.high_score_var = StringVar()
        self.high_score_var.set("High Score: 0")
        self.high_score_label = Label(
            top_frame,
            textvariable=self.high_score_var,
            font=("Helvetica", 10, "bold"),
        )
        self.high_score_label.pack(side=tk.RIGHT)

        # Timer display
        self.timer_var = StringVar()
        self.timer_var.set("Time: 0")
        self.timer_label = Label(
            top_frame,
            textvariable=self.timer_var,
            font=("Helvetica", 10, "bold"),
        )
        self.timer_label.pack()

        # Create the canvas for the game inside the root window
        self.canvas = Canvas(
            self.root,
            width=self.WIDTH,
            height=self.HEIGHT - top_frame.winfo_height(),  # Subtract height for the status bar
            bg="black",  # Set the background color to black
        )
        self.canvas.pack()

        self.root.bind("<Key>", self.handle_events)
        self.timer()
        self.root.mainloop()

    def start(self):
        """Starts the game."""
        self.timer()

    def timer(self):
        """Update the game timer every second."""
        if self.create_new_game:
            self.current_shape = Shape(self.canvas, self.WIDTH, self.HEIGHT, self.START_POINT)  # Pass WIDTH and HEIGHT here
            self.create_new_game = False

        # Update the timer every second
        self.timer_seconds += 1
        self.timer_var.set(f"Time: {self.timer_seconds}")

        if not self.current_shape.fall():
            lines = self.remove_complete_lines()
            if lines:
                self.score += 10 * lines
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.high_score_var.set(f"High Score: {self.high_score}")
                self.status_var.set(f"Level: {self.level}, Score: {self.score}")

            self.current_shape = Shape(self.canvas, self.WIDTH, self.HEIGHT, self.START_POINT)
            if self.is_game_over():
                self.create_new_game = True
                self.game_over()

            self.counter += 1
            if self.counter == 5:
                self.level += 1
                self.speed -= 20
                self.counter = 0
                self.status_var.set(f"Level: {self.level}, Score: {self.score}")

        self.root.after(self.speed, self.timer)

    def handle_events(self, event):
        """Handle all user events."""
        if event.keysym == "Left":
            self.current_shape.move(-1, 0)
        if event.keysym == "Right":
            self.current_shape.move(1, 0)
        if event.keysym == "Down":
            self.current_shape.move(0, 1)
        if event.keysym == "Up":
            self.current_shape.rotate()
        if event.keysym == "space":
            self.current_shape.rotate()

    def is_game_over(self):
        """Check if a newly created shape is able to fall."""
        for box in self.current_shape.boxes:
            if not self.current_shape.can_move_box(box, 0, 1):
                return True
        return False

    def remove_complete_lines(self):
        """Remove complete horizontal lines and return the number of lines removed."""
        all_boxes = self.canvas.find_all()
        box_positions = {}

        # Store positions of each box
        for box in all_boxes:
            x1, y1, x2, y2 = self.canvas.coords(box)
            row = int(y2 // Shape.BOX_SIZE)  # Get the row (bottom y-coordinate of the box)
            if row not in box_positions:
                box_positions[row] = []
            box_positions[row].append(box)

        # Find complete lines with exactly 14 blocks
        complete_lines = []
        for row, boxes in box_positions.items():
            if len(boxes) == self.LINE_WIDTH:  # Check if the row has 14 blocks
                complete_lines.append(row)

        # Sort rows to clear from bottom to top
        complete_lines.sort(reverse=True)

        # Clear complete lines and move blocks down
        for row in complete_lines:
            # Remove all boxes in the completed row
            for box in box_positions[row]:
                self.canvas.delete(box)

            # Move all boxes above the completed row down
            for other_row in sorted(box_positions.keys(), reverse=True):
                if other_row < row:
                    for box in box_positions[other_row]:
                        self.canvas.move(box, 0, Shape.BOX_SIZE)

            # Adjust box_positions after moving boxes
            for other_row in sorted(box_positions.keys(), reverse=True):
                if other_row < row:
                    box_positions[other_row + 1] = box_positions.pop(other_row)

        # Award 10 points for each line cleared
        return len(complete_lines)

    def game_over(self):
        """End the game and show game over message."""
        self.canvas.delete(tk.ALL)
        messagebox.showinfo("Game Over", f"You scored {self.score} points.")


class Shape:
    """Defines a tetris shape."""

    BOX_SIZE = 20

    SHAPES = (
        ("yellow", (0, 0), (1, 0), (0, 1), (1, 1)),  # square
        ("lightblue", (0, 0), (1, 0), (2, 0), (3, 0)),  # line
        ("orange", (2, 0), (0, 1), (1, 1), (2, 1)),  # right el
        ("blue", (0, 0), (0, 1), (1, 1), (2, 1)),  # left el
        ("green", (0, 1), (1, 1), (1, 0), (2, 0)),  # right wedge
        ("red", (0, 0), (1, 0), (1, 1), (2, 1)),  # left wedge
        ("purple", (1, 0), (0, 1), (1, 1), (2, 1)),  # symmetrical wedge
    )

    def __init__(self, canvas, width, height, start_point):
        """Create a shape."""
        self.boxes = []
        self.shape = choice(Shape.SHAPES)
        self.color = self.shape[0]
        self.canvas = canvas
        self.width = width
        self.height = height
        self.start_point = start_point  # Store the start point for shape

        for point in self.shape[1:]:
            box = canvas.create_rectangle(
                point[0] * Shape.BOX_SIZE + self.start_point,
                point[1] * Shape.BOX_SIZE,
                point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + self.start_point,
                point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE,
                fill=self.color,
                outline="black",  # Add border to each block
            )
            self.boxes.append(box)

    def move(self, x, y):
        """Moves this shape (x, y) boxes."""
        if not self.can_move_shape(x, y):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, x * Shape.BOX_SIZE, y * Shape.BOX_SIZE)
            return True

    def fall(self):
        """Moves this shape one box-length down."""
        if not self.can_move_shape(0, 1):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, 0 * Shape.BOX_SIZE, 1 * Shape.BOX_SIZE)
            return True

    def rotate(self):
        """Rotates the shape clockwise."""
        boxes = self.boxes[:]
        pivot = boxes.pop(2)

        def get_move_coords(box):
            """Return (x, y) boxes needed to rotate a box around the pivot."""
            box_coords = self.canvas.coords(box)
            pivot_coords = self.canvas.coords(pivot)
            x_diff = box_coords[0] - pivot_coords[0]
            y_diff = box_coords[1] - pivot_coords[1]
            x_move = (-x_diff - y_diff) / self.BOX_SIZE
            y_move = (x_diff - y_diff) / self.BOX_SIZE
            return x_move, y_move

        for box in boxes:
            x_move, y_move = get_move_coords(box)
            if not self.can_move_box(box, x_move, y_move):
                return False

        for box in boxes:
            x_move, y_move = get_move_coords(box)
            self.canvas.move(box, x_move * self.BOX_SIZE, y_move * self.BOX_SIZE)

        return True

    def can_move_box(self, box, x, y):
        """Check if box can move (x, y) boxes."""
        x = x * Shape.BOX_SIZE
        y = y * Shape.BOX_SIZE
        coords = self.canvas.coords(box)

        if coords[3] + y > self.height:
            return False
        if coords[0] + x < 0:
            return False
        if coords[2] + x > self.width:
            return False

        overlap = set(
            self.canvas.find_overlapping(
                (coords[0] + coords[2]) / 2 + x,
                (coords[1] + coords[3]) / 2 + y,
                (coords[0] + coords[2]) / 2 + x,
                (coords[1] + coords[3]) / 2 + y,
            )
        )
        other_items = set(self.canvas.find_all()) - set(self.boxes)
        if overlap & other_items:
            return False

        return True

    def can_move_shape(self, x, y):
        """Check if the shape can move (x, y) boxes."""
        for box in self.boxes:
            if not self.can_move_box(box, x, y):
                return False
        return True


if __name__ == "__main__":
    game = Game()
    game.start()
