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

        # Create title with different fonts
        title_frame = tk.Frame(self.window)
        title_frame.pack(pady=30)
        
        # Canvas for rotated "Baldynna's"
        baldynna_canvas = tk.Canvas(title_frame, width=280, height=80, highlightthickness=0, bg=self.window.cget('bg'))
        baldynna_canvas.pack(side="left", padx=(0, 5))
        
        baldynna_canvas.create_text(40, 50, text="Baldynna's", font=("Comic Sans MS", 30), 
                                   fill="green", anchor="w", angle=10)
        
        # "Maths Quiz" in Times New Roman
        maths_quiz_label = tk.Label(title_frame, text=" Maths Quiz", font=("Times New Roman", 30))
        maths_quiz_label.pack(side="left", padx=(5, 0))
        
        tk.Label(self.window, text="Select Difficulty Level:", font=("Comic Sans MS", 14)).pack(pady=10)
        self.displayMenu()

    # Display the difficulty level menu
    def displayMenu(self):
        # Create a square frame for the difficulty levels
        frame_size = 300
        board_outer = tk.Frame(self.window, background="brown", width=frame_size, height=frame_size)
        board_outer.pack(padx=20, pady=20)
        board_outer.pack_propagate(False)  #prevent frame from shrinking to fit contents

        board_inner = tk.Frame(board_outer, bg="black", padx=20, pady=20)
        board_inner.pack(padx=10, pady=10, fill="both", expand=True)

        try:
            self.side_image = tk.PhotoImage(file="Assets/Baldynna.png")
            image_label = tk.Label(self.window, image=self.side_image, borderwidth=0, bg=self.window.cget('bg'))
            image_label.place(x=360, y=250) #fixed position to the left of the menu

        # Fallback if image doesn't load
        except Exception as e:
            print(f"Image loading error: {e}")
            placeholder = tk.Frame(self.window, width=250, height=600, bg="green")
            placeholder.place(x=360, y=250)

        # Difficulty levels inside the black square
        label_style = {"font": ("Comic Sans MS", 18, "bold"), "bg": "black", "cursor": "hand2"}

        # Center the labels
        center_container = tk.Frame(board_inner, bg="black")
        center_container.pack(fill="both", expand=True)

        # Create colored labels
        easy = tk.Label(center_container, text="EASY", fg="blue", **label_style)
        moderate = tk.Label(center_container, text="MODERATE", fg="green", **label_style)
        advanced = tk.Label(center_container, text="ADVANCED", fg="orange", **label_style)

        # Add wavy underline on hover
        def add_wavy_underline(event):
            label = event.widget
            if hasattr(label, "_underline"):
                return 
            
            # Create canvas for wavy line
            text_length = len(label.cget("text"))
            width = text_length * 15
            
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

        # Use grid for perfect centering in the center_container
        center_container.grid_rowconfigure(0, weight=1)
        center_container.grid_rowconfigure(4, weight=1)
        center_container.grid_columnconfigure(0, weight=1)
        
        easy.grid(row=1, column=0, pady=8)
        moderate.grid(row=2, column=0, pady=8)
        advanced.grid(row=3, column=0, pady=8)

        for lbl in (easy, moderate, advanced):
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
        self.displayProblem(num1, op, num2)

    # Display the question to the user and accept their answer
    def displayProblem(self, num1, op, num2):
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

    # MODERATE DIFF ----------------------------
    def show_moderate_mode(self):
        # Multiple choices
        choices = [self.correct_answer]
        while len(choices) < 3:
            # Generate wrong answers
            deviation = random.randint(-20, 20) #deviate 20 numbers away from the correct answer
            wrong = self.correct_answer + deviation
            # Ensure wrong answer is not too close to correct and not already in choices
            if wrong != self.correct_answer and wrong not in choices and abs(deviation) >= 5:
                choices.append(wrong)
        random.shuffle(choices)

        # Create buttons for each choice
        for choice in choices:
            tk.Button(self.window, text=str(choice), width=10, height=2,
                      command=lambda c=choice: self.check_answer(c)).pack(pady=5)

    # ADVANCED DIFF ----------------------------
    def show_advanced_mode(self):
        self.answer_var = tk.StringVar()
        display = tk.Entry(self.window, textvariable=self.answer_var, font=("Comic Sans MS", 20), justify="center", state="readonly")
        display.pack(pady=10)

        # Input answers with keypad
        keypad_frame = tk.Frame(self.window)
        keypad_frame.pack()

        buttons = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0', '-', '←']
        ]
        for row in buttons:
            frame_row = tk.Frame(keypad_frame)
            frame_row.pack()
            for key in row:
                tk.Button(frame_row, text=key, width=5, height=2,
                          command=lambda k=key: self.keypad_input(k)).pack(side="left", padx=2, pady=2)

        tk.Button(self.window, text="Submit", command=lambda: self.check_answer(self.answer_var.get())).pack(pady=10)

    def keypad_input(self, key):
        current = self.answer_var.get()
        if key == '←':
            self.answer_var.set(current[:-1])
        else:
            self.answer_var.set(current + key)

# Run the program
if __name__ == "__main__":
    app = MathQuiz(window)
    window.mainloop()