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
    
    def save_students(self):
        # Save student data
        try:
            with open(self.data_file, 'w') as file:
                # Write number of students
                file.write(f"{len(self.students)}\n")
                # Write each student record
                for student in self.students:
                    course_marks = student['course_marks']
                    file.write(f"{student['code']},{student['name']},{course_marks[0]},{course_marks[1]},{course_marks[2]},{student['exam_mark']}\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")
            return False
    
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
        main_frame.configure(style='Main.TFrame')
        
        style = ttk.Style()
        style.configure('Main.TFrame', background='#1B2D4D')
        style.configure('Treeview.Heading', font=('Inter', 11, 'bold')) #style headings
        
        # Title
        title_label = ttk.Label(main_frame, text="BATH SPA UNIVERSITY STUDENT MANAGER", font=('Inter', 26, 'bold'),
                                foreground='#FEFEFE',
                                background='#1B2D4D')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Menu buttons
        buttons = [
            ("Show all students", self.display_students_table),
            ("View individual student record", self.view_individual_student),
            ("Student with highest total mark", self.show_highest_student),
            ("Student with lowest total mark", self.show_lowest_student),
            ("Sort student records", self.sort_students),
            ("Add record", self.add_student),
            ("Delete record", self.delete_student),  
            ("Update record", self.update_student)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                main_frame, 
                text=text, 
                command=command, 
                width=240,
                height=40,
                corner_radius=10,
                font=('Inter', 14, 'bold'),
                fg_color="#FEFEFE",
                text_color="#2C4674",
                hover_color="#F0F0F0",
                border_width=1,
                border_color="#2C4674"
            )
            btn.grid(row=i+1, column=0, pady=5, padx=10, sticky=tk.W)

        # Table frame
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=1, column=1, rowspan=9, padx=10, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
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
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_student_select)
        
        # Store selected student
        self.selected_student = None

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(9, weight=1)
        
        # Display all student records immediately
        self.display_students_table()

    def display_students_table(self):
        '''Show all student records'''
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add student data to table
        for student in self.students:
            total_coursework = sum(student['course_marks'])
            percentage = self.calculate_percentage(student)
            grade = self.calculate_grade(percentage)
            
            self.tree.insert("", tk.END, values=(
                str(student['code']),  #convert to string
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
            # Convert to string
            student_code = str(student_code).strip()
            
            # Debug
            print(f"Looking for student code: '{student_code}'")
            print(f"Available codes: {[str(s['code']).strip() for s in self.students]}")
            
            # Find student in actual data list
            self.selected_student = next((s for s in self.students if str(s['code']).strip() == student_code), None)
            print(f"Selected student: {self.selected_student}")
        else:
            self.selected_student = None
            print("No selection")
        
    def view_individual_student(self):
        # Display individual student record
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
        
        # Create selection dialog
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Student")
        selection_window.geometry("300x200")
        
        ttk.Label(selection_window, text="Select a student:").pack(pady=10)
        
        # Create listbox with student names and codes
        listbox = tk.Listbox(selection_window, width=40, height=10)
        listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        for student in self.students:
            listbox.insert(tk.END, f"{student['code']} - {student['name']}")
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                student = self.students[index]
                
                percentage = self.calculate_percentage(student)
                grade = self.calculate_grade(percentage)
                total_coursework = sum(student['course_marks'])
                
                output = f"INDIVIDUAL STUDENT RECORD\n"
                output += "=" * 50 + "\n\n"
                output += f"Name: {student['name']}\n"
                output += f"Student Number: {student['code']}\n"
                output += f"Coursework Marks: {student['course_marks']}\n"
                output += f"Total Coursework: {total_coursework}/60\n"
                output += f"Exam Mark: {student['exam_mark']}/100\n"
                output += f"Overall Percentage: {percentage:.2f}%\n"
                output += f"Grade: {grade}\n"
                
                messagebox.showinfo("Student Record", output)
                selection_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please select a student.")
        
        ttk.Button(selection_window, text="Select", command=on_select).pack(pady=10)
    
    def show_highest_student(self):
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
        
        highest_student = max(self.students, key=self.calculate_percentage)
        percentage = self.calculate_percentage(highest_student)
        
        # Clear table and show only highest student
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_coursework = sum(highest_student['course_marks'])
        grade = self.calculate_grade(percentage)
        
        self.tree.insert("", tk.END, values=(
            highest_student['code'],
            highest_student['name'],
            f"{total_coursework}/60",
            f"{highest_student['exam_mark']}/100",
            f"{percentage:.2f}%",
            grade
        ))
    
    def show_lowest_student(self):
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
        
        lowest_student = min(self.students, key=self.calculate_percentage)
        percentage = self.calculate_percentage(lowest_student)
        
        # Clear table and show only lowest student
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_coursework = sum(lowest_student['course_marks'])
        grade = self.calculate_grade(percentage)
        
        self.tree.insert("", tk.END, values=(
            lowest_student['code'],
            lowest_student['name'],
            f"{total_coursework}/60",
            f"{lowest_student['exam_mark']}/100",
            f"{percentage:.2f}%",
            grade
        ))
    
    def sort_students(self):
        # Sort student records
        if not self.students:
            messagebox.showinfo("Info", "No student records found.")
            return
        
        # Create sorting dialog
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Students")
        sort_window.geometry("300x200")
        
        ttk.Label(sort_window, text="Sort by:").pack(pady=10)
        
        sort_option = tk.StringVar(value="percentage")
        
        ttk.Radiobutton(sort_window, text="Percentage (High to Low)", 
                       variable=sort_option, value="percentage_desc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_window, text="Percentage (Low to High)", 
                       variable=sort_option, value="percentage_asc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_window, text="Name (A-Z)", 
                       variable=sort_option, value="name_asc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_window, text="Name (Z-A)", 
                       variable=sort_option, value="name_desc").pack(anchor=tk.W)
        
        def perform_sort():
            option = sort_option.get()
            
            if option == "percentage_desc":
                self.students.sort(key=self.calculate_percentage, reverse=True)
            elif option == "percentage_asc":
                self.students.sort(key=self.calculate_percentage)
            elif option == "name_asc":
                self.students.sort(key=lambda x: x['name'].lower())
            elif option == "name_desc":
                self.students.sort(key=lambda x: x['name'].lower(), reverse=True)
            
            sort_window.destroy()
            self.display_students_table()
        
        ttk.Button(sort_window, text="Sort", command=perform_sort).pack(pady=10)
    
    def add_student(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student")
        add_window.geometry("400x300")
        
        # Form fields
        ttk.Label(add_window, text="Student Code (1000-9999):").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        code_entry = ttk.Entry(add_window)
        code_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(add_window, text="Student Name:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(add_window)
        name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(add_window, text="Coursework Marks (0-20 each):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(add_window, text="Mark 1:").grid(row=3, column=0, padx=10, pady=2, sticky=tk.W)
        mark1_entry = ttk.Entry(add_window)
        mark1_entry.grid(row=3, column=1, padx=10, pady=2)
        
        ttk.Label(add_window, text="Mark 2:").grid(row=4, column=0, padx=10, pady=2, sticky=tk.W)
        mark2_entry = ttk.Entry(add_window)
        mark2_entry.grid(row=4, column=1, padx=10, pady=2)
        
        ttk.Label(add_window, text="Mark 3:").grid(row=5, column=0, padx=10, pady=2, sticky=tk.W)
        mark3_entry = ttk.Entry(add_window)
        mark3_entry.grid(row=5, column=1, padx=10, pady=2)
        
        ttk.Label(add_window, text="Exam Mark (0-100):").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        exam_entry = ttk.Entry(add_window)
        exam_entry.grid(row=6, column=1, padx=10, pady=5)
        
        def save_student():
            try:
                # Validate inputs
                code = code_entry.get().strip()
                name = name_entry.get().strip()
                mark1 = int(mark1_entry.get())
                mark2 = int(mark2_entry.get())
                mark3 = int(mark3_entry.get())
                exam = int(exam_entry.get())
                
                # Check if code already exists
                if any(student['code'] == code for student in self.students):
                    messagebox.showerror("Error", "Student code already exists!")
                    return
                
                # Validate ranges
                if not (1000 <= int(code) <= 9999):
                    messagebox.showerror("Error", "Student code must be between 1000 and 9999!")
                    return
                
                if not (0 <= mark1 <= 20) or not (0 <= mark2 <= 20) or not (0 <= mark3 <= 20):
                    messagebox.showerror("Error", "Coursework marks must be between 0 and 20!")
                    return
                
                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100!")
                    return
                
                # Add new student
                new_student = {
                    'code': code,
                    'name': name,
                    'course_marks': [mark1, mark2, mark3],
                    'exam_mark': exam
                }
                
                self.students.append(new_student)
                
                if self.save_students():
                    messagebox.showinfo("Success", "Student added successfully!")
                    add_window.destroy()
                    self.display_students_table()  # Refresh table
                else:
                    self.students.remove(new_student)  # Remove if save failed
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for marks!")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding student: {str(e)}")
        
        ttk.Button(add_window, text="Save", command=save_student).grid(row=7, column=0, columnspan=2, pady=20)
    
    def delete_student(self):
        if not self.selected_student:
            messagebox.showerror("Error", "Please select a student first!")
            print(f"No student selected. Available students: {[s['code'] for s in self.students]}")  #debug
            return
        
        student = self.selected_student
        print(f"Attempting to delete: {student['code']} - {student['name']}")  #debug
        
        if messagebox.askyesno("Confirm Delete", 
                             f"Are you sure you want to delete {student['name']} ({student['code']})?"):
            self.students.remove(student)
            
            if self.save_students():
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.selected_student = None
                self.display_students_table()
            else:
                # Restore if save failed
                self.students.append(student)
    
    def update_student(self):
        if not self.selected_student:
            messagebox.showerror("Error", "Please select a student first!")
            return
        
        student = self.selected_student
        index = self.students.index(student)
        self.show_update_form(student, index)
    
    def show_update_form(self, student, index):
        # Show form to update student details
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Student")
        update_window.geometry("400x300")
        
        # Form fields with current values
        ttk.Label(update_window, text="Student Code:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        code_label = ttk.Label(update_window, text=student['code'])
        code_label.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(update_window, text="Student Name:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(update_window)
        name_entry.insert(0, student['name'])
        name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(update_window, text="Coursework Marks (0-20 each):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(update_window, text="Mark 1:").grid(row=3, column=0, padx=10, pady=2, sticky=tk.W)
        mark1_entry = ttk.Entry(update_window)
        mark1_entry.insert(0, str(student['course_marks'][0]))
        mark1_entry.grid(row=3, column=1, padx=10, pady=2)
        
        ttk.Label(update_window, text="Mark 2:").grid(row=4, column=0, padx=10, pady=2, sticky=tk.W)
        mark2_entry = ttk.Entry(update_window)
        mark2_entry.insert(0, str(student['course_marks'][1]))
        mark2_entry.grid(row=4, column=1, padx=10, pady=2)
        
        ttk.Label(update_window, text="Mark 3:").grid(row=5, column=0, padx=10, pady=2, sticky=tk.W)
        mark3_entry = ttk.Entry(update_window)
        mark3_entry.insert(0, str(student['course_marks'][2]))
        mark3_entry.grid(row=5, column=1, padx=10, pady=2)
        
        ttk.Label(update_window, text="Exam Mark (0-100):").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        exam_entry = ttk.Entry(update_window)
        exam_entry.insert(0, str(student['exam_mark']))
        exam_entry.grid(row=6, column=1, padx=10, pady=5)
        
        def save_changes():
            try:
                # Validate inputs
                name = name_entry.get().strip()
                mark1 = int(mark1_entry.get())
                mark2 = int(mark2_entry.get())
                mark3 = int(mark3_entry.get())
                exam = int(exam_entry.get())
                
                # Validate ranges
                if not (0 <= mark1 <= 20) or not (0 <= mark2 <= 20) or not (0 <= mark3 <= 20):
                    messagebox.showerror("Error", "Coursework marks must be between 0 and 20!")
                    return
                
                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100!")
                    return
                
                # Update student
                self.students[index]['name'] = name
                self.students[index]['course_marks'] = [mark1, mark2, mark3]
                self.students[index]['exam_mark'] = exam
                
                if self.save_students():
                    messagebox.showinfo("Success", "Student updated successfully!")
                    update_window.destroy()
                    self.display_students_table()  # Refresh table
                    self.selected_student = None  # Clear selection
                else:
                    # Revert changes if save failed
                    self.students[index] = student
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for marks!")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating student: {str(e)}")
        
        ttk.Button(update_window, text="Save Changes", command=save_changes).grid(row=7, column=0, columnspan=2, pady=20)
        
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