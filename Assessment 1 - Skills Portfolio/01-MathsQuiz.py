# Exercise 1 - Maths Quiz
# inspired by the game Baldi's Basics

import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import random
import pygame #for sound

# Create window
window = ctk.CTk()
ctk.set_appearance_mode("light")
window.configure(fg_color="#fefefe") #window background color

# Get screen width and height of display
width  = window.winfo_screenwidth() 
height  = window.winfo_screenheight()

class MathQuiz:
    def __init__(self, window):
        self.window = window
        self.window.title("Baldynna's Maths Quiz")
        
        # Favicon
        self.window.iconbitmap("Assets/Favicon.ico")

        # Tkinter window size
        self.window.geometry("%dx%d" % (width, height)) #make it fullscreen
        self.mode = None
        self.score = 0
        self.total_questions = 0
        self.attempt = 1  #track attempts per question

        # Pygame mixer for sound effects
        pygame.mixer.init()

        # Load sound effects
        self.correct_sound = pygame.mixer.Sound("Assets/correct.mp3")
        self.wrong_sound = pygame.mixer.Sound("Assets/wrong.mp3")

        # STYLING FOR BUTTONS
        # Multiple Choice
        self.choice_style = {
            "font": ("Comic Sans MS", 18, "bold"),
            "width": 100,
            "height": 50,
            "fg_color": "#9C27B0",
            "hover_color": "#7B1FA2", 
            "text_color": "white",
            "corner_radius": 14,
            "border_width": 2,
            "border_color": "#7B1FA2"
        }

        # Other buttons
        self.button_style = {
            "font": ("Comic Sans MS", 18, "bold"),
            "width": 180,
            "height": 50,
            "fg_color": "#4CAF50",
            "hover_color": "#388E3C",
            "text_color": "white",
            "corner_radius": 14
        }

        self.create_start_screen()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def create_start_screen(self):
        self.clear_window()

        # Create title with different fonts
        title_frame = tk.Frame(self.window)
        title_frame.pack(pady=30)
        
        # Baldynna's
        baldynna_canvas = ctk.CTkCanvas(title_frame, width=280, height=90, highlightthickness=0, bg="#fefefe")
        baldynna_canvas.pack(side="left", padx=(0, 0))
        #rotate canvas
        baldynna_canvas.create_text(5, 65, text="Baldynna's", font=("Comic Sans MS", 40), fill="green", anchor="w", angle=10)

        # Math's Quiz
        maths_quiz_label = ctk.CTkLabel(title_frame, text=" Maths Quiz", font=("Times New Roman", 40, "bold"), 
                                       fg_color="#fefefe", text_color="black")
        maths_quiz_label.pack(side="left", padx=(0, 0))
        
        ctk.CTkLabel(self.window, text="Select Difficulty Level:", font=("Comic Sans MS", 24), 
                    fg_color="#fefefe", text_color="black").pack(pady=10)
        self.displayMenu()

        ctk.CTkLabel(self.window, text="Inspired by Baldi's Basics",
                     font=("Comic Sans MS", 14), fg_color="#fefefe", text_color="black").pack(side="bottom", pady=10)

    # Display the difficulty level menu
    def displayMenu(self):
        # Create a square frame for the difficulty levels
        frame_size = 300
        board_outer = ctk.CTkFrame(self.window, fg_color="brown", width=frame_size, height=frame_size)
        board_outer.pack(padx=20, pady=20)
        board_outer.pack_propagate(False)  #prevent frame from shrinking to fit contents

        board_inner = ctk.CTkFrame(board_outer, fg_color="black")
        board_inner.pack(padx=20, pady=20, fill="both", expand=True)

        # Baldynna
        self.side_image = ImageTk.PhotoImage(Image.open("Assets/Baldynna.png"))
        image_label = ctk.CTkLabel(self.window, image=self.side_image, text="", fg_color="transparent")
        image_label.place(x=390, y=250) #fixed position to the left of the menu

        # Difficulty levels inside the black square
        label_style = {"font": ("Comic Sans MS", 20, "bold"), "bg": "black", "cursor": "hand2"}

        # Center the labels
        center_container = tk.Frame(board_inner, bg="black")
        center_container.pack(fill="both", expand=True)

        # Create colored labels
        easy = tk.Label(center_container, text="EASY", fg="blue", **label_style)
        moderate = tk.Label(center_container, text="MODERATE", fg="green", **label_style)
        advanced = tk.Label(center_container, text="ADVANCED", fg="orange", **label_style)

        # Underline on hover
        def add_underline(event):
            label = event.widget
            if hasattr(label, "_underline"):
                return 
            
            text_length = len(label.cget("text"))
            width = text_length * 15
            
            # Create canvas for underline
            canvas = tk.Canvas(label, width=width, height=3, highlightthickness=0, bg="black")
            canvas.place(relx=0.5, rely=1.0, anchor="n")
            
            color = label.cget("fg")
            
            # Animate from left to right
            def draw_line(progress=0):
                if not hasattr(label, "_underline") or label._underline != canvas:
                    return
                canvas.delete("line")
                current_width = int(width * progress)
                # Draw solid straight line
                canvas.create_line(0, 1, current_width, 1, fill=color, width=2, tags="line")
                
                if progress < 1.0:
                    label.after(20, draw_line, progress + 0.1)
            
            label._underline = canvas
            draw_line()

        def remove_underline(event):
            label = event.widget
            if hasattr(label, "_underline"):
                canvas = label._underline
                color = label.cget("fg")
                width = canvas.winfo_width()
                
                def remove_line(progress=0):
                    if not hasattr(label, "_underline") or label._underline != canvas:
                        return
                    canvas.delete("line")
                    current_start = int(width * progress)
                    canvas.create_line(current_start, 1, width, 1, fill=color, width=2, tags="line")
                    
                    if progress < 1.0:
                        label.after(20, remove_line, progress + 0.1)
                    else:
                        canvas.destroy()
                        del label._underline
                
                remove_line()

        # Grid for perfect centering in the center_container
        center_container.grid_rowconfigure(0, weight=1)
        center_container.grid_rowconfigure(4, weight=1)
        center_container.grid_columnconfigure(0, weight=1)
        
        easy.grid(row=1, column=0, pady=13)
        moderate.grid(row=2, column=0, pady=13)
        advanced.grid(row=3, column=0, pady=13)

        for lbl in (easy, moderate, advanced):
            lbl.bind("<Enter>", add_underline)
            lbl.bind("<Leave>", remove_underline)

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

        try:
            pil_image = Image.open("Assets/brick_kues.jpg")
            self.bg_image = ImageTk.PhotoImage(pil_image)
            bg_label = ctk.CTkLabel(self.window, image=self.bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()  # send background to back
        except Exception as e:
            print(f"Background image loading error: {e}")
            
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
        # Store current question for retry
        self.current_num1 = num1
        self.current_op = op
        self.current_num2 = num2

        # Height based on mode
        frame_height = 700 if self.mode == "Advanced" else 400

        # Main green frame for everything
        main_frame = ctk.CTkFrame(self.window, width=500, height=frame_height, fg_color="#4CAF50", corner_radius=14)
        main_frame.pack(pady=40)
        main_frame.pack_propagate(False)  # prevent frame from shrinking to fit contents
        
        # Question No.
        ctk.CTkLabel(main_frame, text=f"Question {self.total_questions}", 
                     font=("Comic Sans MS", 30, "bold"),
                     fg_color="#4CAF50",
                     text_color="white").pack(pady=10)
        
        # Problem
        ctk.CTkLabel(main_frame, text=f"{num1} {op} {num2} = ?", 
                     font=("Comic Sans MS", 28, "bold"),
                     fg_color="#4CAF50",
                     text_color="white").pack(pady=15)

        if self.mode == "Easy":
            self.show_easy_mode(main_frame)
        elif self.mode == "Moderate":
            self.show_moderate_mode(main_frame)
        else:
            self.show_advanced_mode(main_frame)

    # EASY DIFF ----------------------------
    def show_easy_mode(self, main_frame):
        choices = [self.correct_answer]
        while len(choices) < 3: #three choices
            wrong = self.correct_answer + random.randint(-5, 5)
            if wrong not in choices:
                choices.append(wrong)
        random.shuffle(choices)

        for choice in choices:
            btn = ctk.CTkButton(main_frame, text=str(choice), **self.choice_style)
            btn.configure(command=lambda c=choice: self.check_answer(c))
            btn.pack(pady=14)

    # MODERATE DIFF ----------------------------
    def show_moderate_mode(self, main_frame):
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
            btn = ctk.CTkButton(main_frame, text=str(choice), **self.choice_style)
            btn.configure(command=lambda c=choice: self.check_answer(c))
            btn.pack(pady=14)

    # ADVANCED DIFF ----------------------------
    def show_advanced_mode(self, main_frame):
        self.answer_var = ctk.StringVar(value="")
        
        # Entry Field
        display = ctk.CTkEntry(main_frame, textvariable=self.answer_var, 
                              font=("Comic Sans MS", 18), 
                              justify="center", 
                              state="readonly",
                              width=200,
                              height=50,
                              border_color = "#9C27B0")
        display.pack(pady=20)

        # Keypad
        keypad_frame = ctk.CTkFrame(main_frame, fg_color="#4CAF50")
        keypad_frame.pack(pady=10)

        buttons = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0', '-', '←']
        ]

        # Keypad Button Style
        keypad_style = {
            "width": 70,
            "height": 70,
            "font": ("Comic Sans MS", 18, "bold"),
            "corner_radius": 14,
            "fg_color": "#9C27B0",
            "hover_color": "#7B1FA2", 
            "text_color": "white"
        }

        for row in buttons:
            row_frame = ctk.CTkFrame(keypad_frame, fg_color="#4CAF50")
            row_frame.pack()
            for key in row:
                ctk.CTkButton(row_frame, text=key, **keypad_style,
                          command=lambda k=key: self.keypad_input(k)).pack(side="left", padx=5, pady=5)

        # Submit
        ctk.CTkButton(main_frame, text="Submit", 
                     font=("Comic Sans MS", 18, "bold"),
                     width=120,
                     height=50,
                     fg_color="#9C27B0", 
                     hover_color="#7B1FA2", 
                     text_color="white",
                     corner_radius=14,
                     command=lambda: self.check_answer(self.answer_var.get())).pack(pady=20)

    def keypad_input(self, key):
        current = self.answer_var.get()
        if key == '←':
            self.answer_var.set(current[:-1])
        else:
            self.answer_var.set(current + key)

    # CHECK ANSWER ----------------------------
    def check_answer(self, user_answer):
        try:
            user_answer = int(user_answer)
        except:
            result = f"Invalid input! Try again."
            self.show_retry(result, retry=True)
            return

        if user_answer == self.correct_answer:
            # Play correct sound effect
            if self.correct_sound:
                self.correct_sound.play()
                
            if self.attempt == 1:
                self.score += 10
                result = "Correct! (+10 notebooks)"
            else:
                self.score += 5
                result = "Correct on second try! (+5 notebooks)"
            self.show_result(result)
        else:
            # Play wrong sound effect
            if self.wrong_sound:
                self.wrong_sound.play()
                
            if self.attempt == 1:
                self.attempt += 1
                result = "Wrong! Try again."
                self.show_retry(result, retry=True)
            else:
                result = f"Wrong again! The correct answer was {self.correct_answer}."
                self.show_result(result)

    # Check whether the user's answer was correct
    def isCorrect(self, user_answer):
        return user_answer == self.correct_answer
    
    def show_retry(self, result_text, retry=False):
        self.clear_window()
        # Keep brick background from next_question
        ctk.CTkLabel(self.window, text=result_text, font=("Comic Sans MS", 24), 
                    fg_color="transparent", text_color="black").pack(pady=20)
        ctk.CTkLabel(self.window, text=f"Notebooks: {self.score}", font=("Comic Sans MS", 18),
                    fg_color="transparent", text_color="black").pack(pady=10)

        if retry:
            ctk.CTkButton(self.window, text="Try Again", **self.button_style,
                         command=self.retry_question).pack(pady=10)
        ctk.CTkButton(self.window, text="Back to Menu", **self.button_style,
                     command=self.create_start_screen).pack(pady=10)

    def retry_question(self):
        self.clear_window()
        
        # Recreate the background
        try:
            bg_label = ctk.CTkLabel(self.window, image=self.bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except:
            pass
            
        # Set height based on mode
        frame_height = 700 if self.mode == "Advanced" else 400
        
        # Recreate main frame
        main_frame = ctk.CTkFrame(self.window, fg_color="#4CAF50", corner_radius=14, width=500, height=frame_height)
        main_frame.pack(pady=40)
        main_frame.pack_propagate(False)
        
        # Display attempt info
        ctk.CTkLabel(main_frame, text=f"Attempt 2", 
                     font=("Comic Sans MS", 24, "bold"),
                     fg_color="#4CAF50",
                     text_color="white").pack(pady=5)
        ctk.CTkLabel(main_frame, text=f"Try again!", 
                     font=("Comic Sans MS", 18),
                     fg_color="#4CAF50",
                     text_color="white").pack(pady=5)
        
        # Problem (recreate the question)
        ctk.CTkLabel(main_frame, text=f"{self.current_num1} {self.current_op} {self.current_num2} = ?", 
                     font=("Comic Sans MS", 28, "bold"),
                     fg_color="#4CAF50",
                     text_color="white").pack(pady=15)

        # Rebuild question interface based on mode
        if self.mode == "Easy":
            self.show_easy_mode(main_frame)
        elif self.mode == "Moderate":
            self.show_moderate_mode(main_frame)
        else:
            self.show_advanced_mode(main_frame)

    def show_result(self, result_text):
        self.clear_window()
        # Keep brick background from next_question
        ctk.CTkLabel(self.window, text=result_text, font=("Comic Sans MS", 24),
                    fg_color="transparent", text_color="black").pack(pady=20)
        ctk.CTkLabel(self.window, text=f"Notebooks: {self.score}", font=("Comic Sans MS", 18),
                    fg_color="transparent", text_color="black").pack(pady=10)

        if self.total_questions >= 10:
            ctk.CTkButton(self.window, text="See Final Results", **self.button_style,
                         command=self.displayResults).pack(pady=10)
        else:
            ctk.CTkButton(self.window, text="Next Question", **self.button_style,
                         command=self.next_question).pack(pady=10)
        ctk.CTkButton(self.window, text="Back to Menu", **self.button_style,
                     command=self.create_start_screen).pack(pady=10)

# Run the program
if __name__ == "__main__":
    app = MathQuiz(window)
    window.mainloop()