import tkinter as tk
from time import time
import random
from PIL import Image, ImageTk  # Import Image and ImageTk to handle image resizing

# List of predefined long sentences
sentence_set = [
    "Psalm 23:1-6 The Lord is my shepherd; I shall not want. He makes me "
    "lie down in green pastures. He leads me beside still waters; "
    "he restores my soul. He leads me in the right paths for his "
    "name's sake. Even though I walk through the darkest valley, I "
    "fear no evil; for you are with me; your rod and your staff "
    "-- they comfort me. You anoint my head with oil; my cup overflows. "
    "Surely goodness and mercy shall follow me all the days of my life, "
    "and I shall dwell in the house of the Lord my whole life long.",


    "This pookie wookie wanted to say Hi to the other pookie wookie but "
    "this pookie wookie was too shy and decided to sit quietly at a corner. "
    "The other pookie wookie saw what the other pookie wookie did and "
    "decided to approach that other pookie wookie. That pookie wookie "
    "saw the other pookie wookie approaching and hid herself in the corner. "
    "The other pookie wookie then asked,'You alright, my little pookie bear?'",


    "Ephesian 6:10-18 (the Armor of God): Finally,  be strong in the Lord "
    "and in the strength of his power. Put on the whole armor of God, so "
    "that you may be able to stand against enemies of blood and flesh, "
    "but agaisnt the rulers, against the authorities, against the cosmic "
    "powers of this present darkness, against the spiritual forces of evil "
    "in the heavenly places. Therefore take up the whole armor of God, "
    "so that you may be able to withstand on that evil day, and having "
    "dont everything, to stand firm. Stand therefore, and fasten the belt of truth "
    "around your waist, and put on the breastplate of righteouness. "
    "As shoes for your feet put on whatever will make you ready to "
    "proclaim the gospel of peace. With all of these, take the shield "
    "of faith, with which you will be able to quench all of the "
    "flaming arrows of the evil one. Take the helmet of salvation, "
    "and the sword of the Spirit, which is the word of God. Pray "
    "in the Spirit at all times in every prayer and supplication. "
    "To that end keep alert and always persevere in supplication "
    "for all the saints. ",


    "1 Timothy 2:12 I permit no woman to teach or to have authority over a man; she is to keep silent. ",


    "Romans 5:3 And not only that, but we also boast in our sufferings, knowing that suffering produces endurance. ",


    "Exodus 8:4 "
    "And the frogs shall come up on you and on your people and on all your officials. ",


    "1 John 4:15 "
    "God abides in those who confess that Jesus is the Son of God, and they abide in God. ",


    "Psalm 91 "
    "You who live in the shelter of the Most High, who abide in the shadow of the Almighty, "
    "will say to the Lord, 'My refuge and my fortress; my God, in whom I trust.' "
    "For he will deliver you from the snare of the fowler and from the deadly pestilence; "
    "he will cover you with his pinions, and under his wings you will find refuge; "
    "his faithfulness is a shield and buckler. You will not fear the terror of the night, "
    "or the arrow that flies by day, or the pestilence that stalks in darkness, "
    "or the destruction that wastes at noonday. A thousand may fall at your side, "
    "ten thousand at your right hand, but it will not come near you. You will only "
    "look with your eyes and see the punishment of the wicked. Because you have made "
    "the Lord your refuge, the Most High your dwelling place, no evil shall befall you, "
    "no scourge come near your tent. For he will command his angels concerning you "
    "to guard you in all your ways. On their hands they will bear you up, "
    "so that you will not dash your foot against a stone. You will tread on "
    "the lion and the adder, the young lion and the serpent you will trample underfoot. "
    "Those who love me, I will deliver; I will protect those who know my name. "
    "When they call to me, I will answer them; I will be with them in trouble, "
    "I will rescue them and honor them. With long life I will satisfy them, "
    "and show them my salvation. ",


    "Psalm 100 "
    "Make a joyful noise to the Lord, all the earth. Worship the Lord with gladness; "
    "come into his presence with singing. Know that the Lord is God. It is he that "
    "made us, and we are his; we are his people, and the sheep of his pasture. "
    "Enter his gates with thanksgiving, and his courts with praise. Give thanks to him, "
    "bless his name. For the Lord is good; his steadfast love endures forever, "
    "and his faithfulness to all generations. ",


    "Romans 8:18"
    "I consider that the sufferings of this present time are not worth comparing with the glory"
    "about to be revealed to us.",


    "John 15:4-5 "
    "Abide in me as I abide in you. Just as the branch cannot bear fruit "
    "by itself unless it abides in the vine, neither can you unless you abide in me. "
    "I am the vine, you are the branches. Those who abide in me and I in them "
    "bear much fruit, because apart from me you can do nothing. ",


    "Luke 12:27 "
    "Consider the lilies, how they grow: they neither toil nor spin; yet I tell you, "
    "even Solomon in all his glory was not clothed like one of these. ",


    "Lamentations 3:22-23 "
    "The steadfast love of the Lord never ceases, his mercies never come to an end; "
    "they are new every morning; great is your faithfulness. ",


    "John 11:35 "
    "Jesus began to weep. ",


    "Malachi 2:3 "
    "I will rebuke your offspring, and spread dung on your faces, the dung of your offerings, "
    "and I will put you out of my presence. ",


    "Psalm 61 "
    "Hear my cry, O God; listen to my prayer. From the end of the earth I call "
    "to you, when my heart is faint. Lead me to the rock that is higher than I; "
    "for you are my refuge, a strong tower against the enemy. Let me abide in your tent forever, "
    "find refuge under the shelter of your wings. For you, O God, have heard my vows; "
    "you have given me the heritage of those who fear your name. Prolong the life "
    "of the king; may his years endure to all generations! May he be enthroned "
    "forever before God; appoint steadfast love and faithfulness to watch over him! "
    "So I will always sing praises to your name, as I pay my vows day after day. ",


    "Ephesians 6:10-11 "
    "Finally, be strong in the Lord and in the strength of his power. Put on the whole "
    "armor of God, so that you may be able to stand against the wiles of the devil. ",

    "Romans 8:38-39"
    "For I am convinced that neither death, nor life, nor angels, nor rulers, nor things present, "
    "nor things to come, nor powers, nor height, nor depth, nor anything else in all creation, "
    "will be able to separate us from the love of God in Christ Jesus our Lord.",

    "Matthew 11:28-30"
    "Come to me, all you that are weary and are carrying heavy burdens, and I will give "
    "you rest. Take my yoke upon you, and learn from me; for I am gentle and humble in heart, "
    "and you will find rest for your souls. For my yoke is easy, and my burden is light.v",

    "2 Kings 2:23-24 "
    "From there Elisha went up to Bethel. As he was walking along the road, some boys came "
    "out of the city and jeered at him. 'Get out of here, baldy!' they said. 'Get out of here, "
    "baldy!' He turned around, looked at them, and called down a curse on them in the name of "
    "the Lord. Then two bears came out of the woods and mauled forty-two of the boys.",
]

# Select a random sentence from the sentence set
def get_random_sentence():
    return random.choice(sentence_set)

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Type Racer Bible Version(Sam)")
        self.root.geometry("1000x800")
        
        self.start_time = None
        self.completed_chars = 0
        self.countdown = 3
        
        # Initialize with a random sentence
        self.sentence = get_random_sentence()
        self.words = len(self.sentence.split())
        
        # Load the road and car images
        self.road_image_path = "C:/Users/samue/OneDrive/Documents/Python Games/TypeRacer/images/road.png"  # Replace with your road image path
        self.car_image_path = "C:/Users/samue/OneDrive/Documents/Python Games/TypeRacer/images/f1 car.png"    # Replace with your car image path
        
        # Initialize the images with default sizes
        self.road_image = Image.open(self.road_image_path)
        self.car_image = Image.open(self.car_image_path)
        
        # Set default scaling factor
        self.road_scale_factor = 2.5
        self.car_scale_factor = 0.2

        # Resize images based on scale factors
        self.road_image_resized = self.resize_image(self.road_image, self.road_scale_factor)
        self.car_image_resized = self.resize_image(self.car_image, self.car_scale_factor)
        
        # Convert resized images for Tkinter compatibility
        self.road_image_tk = ImageTk.PhotoImage(self.road_image_resized)
        self.car_image_tk = ImageTk.PhotoImage(self.car_image_resized)
        
        # Main layout
        self.create_widgets()
        
    def create_widgets(self):
        # Configure grid to center elements in a fixed width area
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        
        # Only one column, set its width
        self.root.grid_columnconfigure(0, weight=0)
        
        # Create a frame for centering the content
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, columnspan=1, pady=20, padx=50)
        
        # Sentence Text Area
        self.sentence_text = tk.Text(
            frame, wrap="word", font=("Helvetica", 14), height=10, width=70, bg="white", fg="black"
        )
        self.sentence_text.insert(tk.END, self.sentence)
        self.sentence_text.config(state=tk.DISABLED)  # Make it read-only
        self.sentence_text.grid(row=0, column=0, pady=10)
        
        # User Typing Area
        self.entry = tk.Text(frame, font=("Helvetica", 16), width=70, height=5)
        self.entry.grid(row=1, column=0, pady=10)
        self.entry.bind("<KeyRelease>", self.update_typing_progress)
        
        # Feedback Area
        self.feedback_label = tk.Label(frame, text="", font=("Helvetica", 12), fg="red")
        self.feedback_label.grid(row=2, column=0, pady=10)
        
        # Road and Car Canvas
        self.canvas = tk.Canvas(frame, width=700, height=100, bg="gray")
        self.canvas.grid(row=3, column=0, pady=10)
        self.canvas.create_image(0, -15, anchor="nw", image=self.road_image_tk)
        self.car = self.canvas.create_image(-10, 30, anchor="nw", image=self.car_image_tk)
        
        # Results
        self.result_label = tk.Label(frame, text="", font=("Helvetica", 14), fg="blue")
        self.result_label.grid(row=4, column=0, pady=10)
        
        # Start Button
        self.start_button = tk.Button(
            frame, text="Start Typing Test", font=("Helvetica", 14), command=self.start_test
        )
        self.start_button.grid(row=5, column=0, pady=10)
        
        # Current WPM and Timer display
        self.wpm_label = tk.Label(
            frame, text="Current WPM: 0 | Time: 0s", font=("Helvetica", 24), anchor="center"
        )
        self.wpm_label.grid(row=6, column=0, pady=10)
        
    def resize_image(self, image, scale_factor):
        width, height = image.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        return image.resize((new_width, new_height), Image.LANCZOS)
        
    def start_test(self):
        # Select a new random sentence
        self.sentence = get_random_sentence()
        self.words = len(self.sentence.split())
        self.start_time = time()
        self.entry.delete("1.0", tk.END)
        self.entry.config(state=tk.NORMAL)
        self.feedback_label.config(text="")
        self.result_label.config(text="")
        self.completed_chars = 0
        self.countdown = 3
        self.move_car(0)
        
        # Update the displayed sentence
        self.sentence_text.config(state=tk.NORMAL)
        self.sentence_text.delete("1.0", tk.END)
        self.sentence_text.insert(tk.END, self.sentence)
        self.sentence_text.config(state=tk.DISABLED)
        
        self.countdown_timer()

    def countdown_timer(self):
        if self.countdown > 0:
            self.feedback_label.config(text=str(self.countdown))
            self.countdown -= 1
            self.root.after(1000, self.countdown_timer)
        else:
            self.feedback_label.config(text="Go!")
            self.entry.focus()
            self.root.after(1000, lambda: self.feedback_label.config(text=""))
    
    def update_typing_progress(self, event):
        typed_text = self.entry.get("1.0", "end-1c")
        self.completed_chars = len(typed_text)
        correct_chars = sum(1 for i, c in enumerate(typed_text) if i < len(self.sentence) and c == self.sentence[i])
        progress = correct_chars / len(self.sentence)
        self.move_car(progress)
        elapsed_time = time() - self.start_time
        current_wpm = int(self.completed_chars / 5 / (elapsed_time / 60)) if elapsed_time > 0 else 0
        elapsed_time_seconds = int(elapsed_time)  # Get the time in seconds
        self.wpm_label.config(text=f"Current WPM: {current_wpm} | Time: {elapsed_time_seconds}s")
        if typed_text.strip() == self.sentence.strip():
            self.end_test()
    
    def move_car(self, progress):
        x_pos = int(700 * progress)  # Adjust width to match canvas
        self.canvas.coords(self.car, x_pos, 30)
    
    def end_test(self):
        self.entry.config(state=tk.DISABLED)
        end_time = time()
        total_time = round(end_time - self.start_time, 2)
        wpm = int(self.words / (total_time / 60)) if total_time > 0 else 0
        self.result_label.config(
            text=f"Well done! You completed the typing test.\nTime: {total_time} seconds | Speed: {wpm} WPM"
        )

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()
