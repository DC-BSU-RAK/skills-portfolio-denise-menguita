# Exercise 3 - Student Manager

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os

# PALETTE
## white - #FEFEFE
## blue - #2C4674
## dark blue - #1B2D4D
## light gray - #F0F0F0
## dark gray - #3B3B3B

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("BSU Student Manager")
        self.root.state('zoomed')  # full screen
        self.root.resizable(True, True)
        self.root.configure(bg='#2C4674')
        
        # Data file path
        self.data_file = "studentMarks.txt"
        
        # Load student data
        self.students = self.load_students()
        
        # Create GUI
        self.create_gui()
    
    def load_students(self):
        students = []
        try:
            with open(self.data_file, 'r') as file:
                lines = file.readlines()
                if not lines:
                    return students
                
                # Skip first line (number of students)
                for line in lines[1:]:
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) >= 5:
                            student = {
                                'code': parts[0],
                                'name': parts[1],
                                'course_marks': [int(parts[2]), int(parts[3]), int(parts[4])],
                                'exam_mark': int(parts[5])
                            }
                            students.append(student)
        except FileNotFoundError:
            messagebox.showerror("Error", f"File {self.data_file} not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
        
        return students

    def calculate_percentage(self, student):
        total_coursework = sum(student['course_marks'])
        total_marks = total_coursework + student['exam_mark']
        return (total_marks / 160) * 100
    
    def calculate_grade(self, percentage):
        # Calculate grade based on percentage
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
        
    def create_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="BATH SPA UNIVERSITY STUDENT MANAGER", font=('Inter', 20, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Table frame
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=1, column=1, rowspan=8, padx=10, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create treeview for table
        columns = ("Student No", "Name", "Total Coursework", "Exam Mark", "Overall Percentage", "Grade")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.CENTER)
        
        # Adjust column widths
        self.tree.column("Student No", width=100)
        self.tree.column("Name", width=150)
        self.tree.column("Total Coursework", width=120)
        self.tree.column("Exam Mark", width=100)
        self.tree.column("Overall Percentage", width=120)
        self.tree.column("Grade", width=80)
        
        # Scrollbar for treeview
        tree_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
    
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Store selected student
        self.selected_student = None

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        # Display all student records immediately
        self.display_students_table()

    def display_students_table(self):
        # Show all student records
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add student data to table
        for student in self.students:
            total_coursework = sum(student['course_marks'])
            percentage = self.calculate_percentage(student)
            grade = self.calculate_grade(percentage)
            
            self.tree.insert("", tk.END, values=(
                student['code'],
                student['name'],
                f"{total_coursework}/60",
                f"{student['exam_mark']}/100",
                f"{percentage:.2f}%",
                grade
            ))
  
    def on_student_select(self, event):
        # Select student from table
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            student_code = self.tree.item(item)['values'][0]
            self.selected_student = next((s for s in self.students if s['code'] == student_code), None)
        else:
            self.selected_student = None

def main():
    root = tk.Tk()

    # Favicon
    ico = Image.open("BSU Logo.png")
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)

    app = StudentManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()