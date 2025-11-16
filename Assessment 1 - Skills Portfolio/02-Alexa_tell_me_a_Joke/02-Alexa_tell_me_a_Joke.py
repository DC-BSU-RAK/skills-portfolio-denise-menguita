# Exercise 02 - Alexa tell me a Joke

import tkinter as tk
from tkinter import messagebox
import random

class AlexaJokes:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa, tell me a joke")
        self.root.state('zoomed')  # full screen
        self.root.resizable(True, True)
        self.root.configure(bg='#f8b936')  # window background color

        # Load jokes from file
        self.jokes = self.load_jokes()
        
        # Current joke variables
        self.current_joke_setup = ""
        self.current_joke_punchline = ""
        
        # Create GUI elements
        self.create_widgets()
    
    def load_jokes(self):
        """Load jokes from the text file"""
        try:
            with open("randomJokes.txt", "r", encoding="utf-8") as file:
                content = file.read()
            
            jokes = []
            lines = content.strip().split('\n')
            
            for line in lines:
                if line.strip():
                    if '\t' in line:
                        parts = line.split('\t')
                    else:
                        # Look for position where punchline starts (after setup question)
                        for i, char in enumerate(line):
                            if char.isupper() and i > 10:  # Find where punchline starts (capital letter after some text)
                                parts = [line[:i].strip(), line[i:].strip()]
                                break
                        else:
                            if '?' in line:
                                parts = line.split('?', 1)
                                parts[0] += '?'  # Add back the question mark
                                parts[1] = parts[1].strip()
                            else:
                                parts = [line, ""]
                    
                    if len(parts) >= 2:
                        setup = parts[0].strip()
                        punchline = parts[1].strip()
                        jokes.append((setup, punchline))
            
            return jokes
        
        except FileNotFoundError:
            messagebox.showerror("Error", "Jokes not found. Make sure 'randomJokes.txt' is in the same directory.")
            return [("Error", "Jokes not found")]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load jokes: {str(e)}")
            return [("Error", "Failed to load jokes")]
    
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#f8b936")
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Joke setup
        self.setup_label = tk.Label(main_frame, text="", 
                                font=("Arial", 12), 
                                wraplength=500, 
                                justify=tk.LEFT,
                                fg="#521903", bg='#f8b936')
        self.setup_label.pack(pady=20, fill=tk.X)
        
        # Punchline
        self.punchline_label = tk.Label(main_frame, text="", 
                                    font=("Arial", 12, "italic"), 
                                    fg="#521903",
                                    wraplength=500,
                                    justify=tk.LEFT,
                                    bg='#f8b936')
        self.punchline_label.pack(pady=10, fill=tk.X)
        
        # Button Frame
        button_frame = tk.Frame(main_frame, bg='#f8b936')
        button_frame.pack(pady=20)
        
        # Style of Buttons
        button_style = {
            "font": ("Arial", 16),
            "fg": "#dc8c18",
            "bg": "#521903"
        }
        
        # Alexa Button
        self.alexa_button = tk.Button(button_frame, text="Alexa, tell me a Joke", 
                                    **button_style,
                                    command=self.get_joke)
        self.alexa_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Show Punchline Button
        self.punchline_button = tk.Button(button_frame, text="Show Punchline", 
                                        **button_style,
                                        command=self.show_punchline)
        self.punchline_button.grid(row=0, column=1, padx=5, pady=5)
        self.punchline_button.grid_remove()  # Hide initially
        
        # Next Joke Button
        self.next_button = tk.Button(button_frame, text="Next Joke", 
                                **button_style,
                                command=self.get_joke)
        self.next_button.grid(row=0, column=2, padx=5, pady=5)
        self.next_button.grid_remove()  # Hide initially
        
        # Quit Button
        self.quit_button = tk.Button(button_frame, text="Quit", 
                                    **button_style,
                                    command=self.root.quit)
        self.quit_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Status
        self.status_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="#521903", bg="#f8b936")
        self.status_label.pack(pady=10)

    def get_joke(self):
        """Get a random joke from the loaded jokes"""
        if not self.jokes:
            self.setup_label.config(text="No more jokes!")
            self.punchline_label.config(text="")
            return
        
        # Select joke
        self.current_joke_setup, self.current_joke_punchline = random.choice(self.jokes)
        
        # Update display
        self.setup_label.config(text=self.current_joke_setup)
        self.punchline_label.config(text="")
        
        # Show punchline button and hide next button
        self.punchline_button.grid()
        self.next_button.grid_remove()
        
        # Update status
        self.status_label.config(text="Click 'Show Punchline' to see the punchline.")

    def show_punchline(self):
        """Display the punchline of the current joke"""
        self.punchline_label.config(text=self.current_joke_punchline)
        
        # Hide punchline button and show next button
        self.punchline_button.grid_remove()
        self.next_button.grid()
        
        # Remove alexa button after punchline is showed
        self.alexa_button.grid_remove()
        
        self.status_label.config(text="Click 'Next Joke' for another one.")

def main():
    window = tk.Tk()
    app = AlexaJokes(window)
    window.mainloop()

if __name__ == "__main__":
    main()