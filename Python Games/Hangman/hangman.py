import random
import tkinter as tk

WORDLIST_FILENAME = "C:/Users/samue/OneDrive/Documents/Python Games/Hangman/hangman_categories.txt"

# Load word categories and words
def loadWords():
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    categories_dict = {}
    current_category = None
    for line in inFile:
        line = line.strip()
        if line.isupper():
            current_category = line
            categories_dict[current_category] = []
        elif current_category:
            categories_dict[current_category].append(line.lower())
        else:
            print(f"Warning: Skipping invalid line (no category set): {line}")
    print("Word list loaded with categories:", ", ".join(categories_dict.keys()))
    return categories_dict

def chooseWord(categories_dict):
    category = random.choice(list(categories_dict.keys()))
    word = random.choice(categories_dict[category])
    return category, word

# Check if word is fully guessed
def isWordGuessed(secretWord, lettersGuessed):
    return all(letter in lettersGuessed for letter in secretWord)

# Hangman Game Logic
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        
        self.categories_dict = loadWords()
        self.category, self.secretWord = chooseWord(self.categories_dict)
        self.lettersGuessed = []
        self.mistakesMade = 0
        
        self.max_mistakes = 8
        
        self.create_widgets()
        self.update_game_display()
        self.bind_keyboard_input()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text="Welcome to Hangman!", font=('Helvetica', 16))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Category Label
        self.category_label = tk.Label(self.root, text=f"Category: {self.category}", font=('Helvetica', 14))
        self.category_label.grid(row=1, column=0, columnspan=2)

        # Number of letters in the word
        self.word_length_label = tk.Label(self.root, text=f"Word length: {len(self.secretWord)} letters", font=('Helvetica', 14))
        self.word_length_label.grid(row=2, column=0, columnspan=2)

        # Word Display
        self.word_label = tk.Label(self.root, text="", font=('Helvetica', 14))
        self.word_label.grid(row=3, column=0, columnspan=2)

        # Available Letters
        self.available_letters_label = tk.Label(self.root, text="", font=('Helvetica', 14))
        self.available_letters_label.grid(row=4, column=0, columnspan=2)

        # Hangman Canvas
        self.canvas = tk.Canvas(self.root, width=200, height=200)
        self.canvas.grid(row=5, column=0, columnspan=2, pady=10)

        # Alphabet Buttons
        self.alphabet_frame = tk.Frame(self.root)
        self.alphabet_frame.grid(row=6, column=0, columnspan=2, pady=10)
        self.create_alphabet_buttons()

        # Messages (Win / Loss)
        self.game_message = tk.Label(self.root, text="", font=("Helvetica", 16), fg="green")
        self.game_message.grid(row=7, column=0, columnspan=2, pady=10)

    def create_alphabet_buttons(self):
        letters = "abcdefghijklmnopqrstuvwxyz"
        self.buttons = {}
        for i, letter in enumerate(letters):
            button = tk.Button(self.alphabet_frame, text=letter, width=3, height=2, command=lambda letter=letter: self.guess_letter(letter))
            button.grid(row=i // 13, column=i % 13)
            self.buttons[letter] = button

    def bind_keyboard_input(self):
        for letter in "abcdefghijklmnopqrstuvwxyz":
            self.root.bind(letter, lambda event, letter=letter: self.guess_letter(letter))

    def update_game_display(self):
        self.word_label.config(text=self.getGuessedWord(self.secretWord, self.lettersGuessed))
        self.available_letters_label.config(text=f"Available Letters: {self.getAvailableLetters(self.lettersGuessed)}")
        self.draw_hangman()

        # Check win condition
        if isWordGuessed(self.secretWord, self.lettersGuessed):
            self.show_win()

    def draw_hangman(self):
        self.canvas.delete("all")
        
        # Adjusted positions for smaller hangman parts
        if self.mistakesMade > 0:
            self.canvas.create_oval(70, 30, 130, 90)  # Head
        if self.mistakesMade > 1:
            self.canvas.create_line(100, 90, 100, 150)  # Body
        if self.mistakesMade > 2:
            self.canvas.create_line(100, 150, 50, 200)  # Left Leg
        if self.mistakesMade > 3:
            self.canvas.create_line(100, 150, 150, 200)  # Right Leg
        if self.mistakesMade > 4:
            self.canvas.create_line(100, 120, 50, 100)  # Left Arm
        if self.mistakesMade > 5:
            self.canvas.create_line(100, 120, 150, 100)  # Right Arm
        if self.mistakesMade > 6:
            self.canvas.create_line(70, 30, 130, 30)  # Rope
        if self.mistakesMade > 7:
            self.canvas.create_line(70, 30, 70, 60)  # Gallows

    def getGuessedWord(self, secretWord, lettersGuessed):
        # Create the word string with spaces between words and no dashes between them
        result = []
        for letter in secretWord:
            if letter in lettersGuessed:
                result.append(letter)
            elif letter == " ":
                result.append(" ")
            else:
                result.append("_")
        return " ".join(result)

    def getAvailableLetters(self, lettersGuessed):
        import string
        return ''.join([letter for letter in string.ascii_lowercase if letter not in lettersGuessed])

    def guess_letter(self, letter):
        if letter in self.lettersGuessed:
            return
        self.lettersGuessed.append(letter)
        self.buttons[letter].config(state=tk.DISABLED)  # Disable the button after guessing
        
        if letter not in self.secretWord:
            self.mistakesMade += 1
        
        self.update_game_display()

        if isWordGuessed(self.secretWord, self.lettersGuessed):
            self.show_win()
        elif self.mistakesMade >= self.max_mistakes:
            self.show_loss()

    def show_win(self):
        self.game_message.config(text="You Won!", fg="green")

    def show_loss(self):
        self.game_message.config(text=f"You Lost! The word was: {self.secretWord}", fg="red")

# Start Tkinter Window
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)  # Allow resizing of the window
    game = HangmanGame(root)
    root.mainloop()
