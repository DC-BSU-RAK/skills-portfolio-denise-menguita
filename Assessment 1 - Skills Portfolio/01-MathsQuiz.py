# Exercise 1 - Maths Quiz
# inspired by the game Baldi's Basics

from tkinter import * # Asterisk (*) to import everything
import tkinter as tk
import random

# Create window
window = tk.Tk()

# Get screen width and height of display
width  = window.winfo_screenwidth() 
height  = window.winfo_screenheight()

class MathQuiz:
    def __init__(self, window):
        self.window = window
        self.window.title("Baldynna's Maths Quiz")
        
        # Set tkinter window size
        self.window.geometry("%dx%d" % (width, height)) # make it fullscreen
        self.mode = None

        self.create_start_screen()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def create_start_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Baldynna's Maths Quiz", font=("Times New Roman", 30, "bold")).pack(pady=30)
        tk.Label(self.window, text="Select Difficulty Level:", font=("Arial", 14)).pack(pady=10)

        # Create a black square frame for the difficulty levels
        board_outer = tk.Frame(self.window, background="brown")
        board_outer.pack(padx=20, pady=20)

        # Force window update to get proper coordinates
        self.window.update_idletasks()
        
        # Add image overlapping the frame by 30 pixels
        try:
            self.side_image = tk.PhotoImage(file="Baldynna.png")  # Replace with your image file
            image_label = tk.Label(self.window, image=self.side_image, bg="black", borderwidth=0)
            # Calculate position relative to board_outer
            board_x = board_outer.winfo_x()
            board_y = board_outer.winfo_y()
            image_label.place(x=board_x - 250 + 30, y=board_y)
            image_label.lift()  # Ensure it's on top
        except Exception as e:
            print(f"Image loading error: {e}")
            # Fallback if image doesn't load
            placeholder = tk.Frame(self.window, width=250, height=600, bg="darkgray")
            board_x = board_outer.winfo_x()
            board_y = board_outer.winfo_y()
            placeholder.place(x=board_x - 250 + 30, y=board_y)
            placeholder.lift()  # Ensure it's on top

        board_inner = tk.Frame(board_outer, bg="black", padx=20, pady=20)
        board_inner.pack(padx=10, pady=10)

        # Difficulty levels inside the black square
        label_style = {"font": ("Arial", 18, "bold"), "bg": "black", "cursor": "hand2"}

        # Create colored labels
        easy = tk.Label(board_inner, text="EASY", fg="blue", **label_style)
        moderate = tk.Label(board_inner, text="MODERATE", fg="green", **label_style)
        advanced = tk.Label(board_inner, text="ADVANCED", fg="orange", **label_style)

        # Add wavy underline on hover
        def add_wavy_underline(event):
            label = event.widget
            if hasattr(label, "_underline"):
                return  # Already has underline
            
            # Create canvas for wavy line - use fixed width based on text length
            text_length = len(label.cget("text"))
            width = text_length * 15  # Estimate width based on text
            
            canvas = tk.Canvas(label, width=width, height=6, bg="black", highlightthickness=0)
            canvas.place(relx=0.5, rely=1.0, anchor="n")
            
            # Create wavy line
            color = label.cget("fg")
            for i in range(0, width, 8):
                y1 = 1 if (i // 4) % 2 == 0 else 4
                y2 = 4 if y1 == 1 else 1
                canvas.create_line(i, y1, i + 4, y2, fill=color, width=2)
            label._underline = canvas

        def remove_wavy_underline(event):
            label = event.widget
            if hasattr(label, "_underline"):
                label._underline.destroy()
                del label._underline

        for lbl in (easy, moderate, advanced):
            lbl.pack(pady=8)
            lbl.bind("<Enter>", add_wavy_underline)
            lbl.bind("<Leave>", remove_wavy_underline)
            
        # Make the labels clickable
        easy.bind("<Button-1>", lambda e: self.start_quiz("Easy"))
        moderate.bind("<Button-1>", lambda e: self.start_quiz("Moderate"))
        advanced.bind("<Button-1>", lambda e: self.start_quiz("Advanced"))

    def start_quiz(self, mode):
        self.mode = mode
        self.score = 0
        self.total_questions = 0
        self.next_question()

    def next_question(self):
        self.clear_window()
        self.attempt = 1  #reset attempt

        # Random number generation based on difficulty
        if self.mode == "Easy":
            num1 = random.randint(0, 9)
            num2 = random.randint(0, 9)
        elif self.mode == "Moderate":
            num1 = random.randint(10, 99)
            num2 = random.randint(10, 99)
        else:  # Advanced
            num1 = random.randint(1000, 9999)
            num2 = random.randint(1000, 9999)

        # Randomize operator
        op = random.choice(["+", "-"])
        self.correct_answer = num1 + num2 if op == "+" else num1 - num2

        self.total_questions += 1

        tk.Label(self.window, text=f"Question {self.total_questions}", font=("Comic Sans MS", 16, "bold")).pack(pady=10)
        tk.Label(self.window, text=f"{num1} {op} {num2} = ?", font=("Comic Sans MS", 20)).pack(pady=20)

        if self.mode == "Easy":
            self.show_easy_mode()
        elif self.mode == "Moderate":
            self.show_moderate_mode()
        else:
            self.show_advanced_mode()

    # EASY DIFF ----------------------------
    def show_easy_mode(self):
        choices = [self.correct_answer]
        while len(choices) < 3: #three choices
            wrong = self.correct_answer + random.randint(-5, 5)
            if wrong not in choices:
                choices.append(wrong)
        random.shuffle(choices)

        for choice in choices:
            tk.Button(self.window, text=str(choice), width=10, height=2,
                      command=lambda c=choice: self.check_answer(c)).pack(pady=5)

# Run the program
if __name__ == "__main__":
    app = MathQuiz(window)
    window.mainloop()