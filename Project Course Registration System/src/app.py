import tkinter as tk
import psycopg2
#from getpass import getpass
from tkinter import ttk
import random
import time
#import tksheet
#from tksheet import Sheet
from PIL import Image, ImageTk
#from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PyPDF2 import PdfReader 
from shutil import copyfile
import fitz  # PyMuPDF

character_number = 5
duration = 0

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")

        global duration
        self.running = False
        
        self.label = tk.Label(root, text=f"Time left: {duration} seconds", font=("Helvetica", 16))
        self.label.pack(pady=10)
        
        self.start_button = tk.Button(root, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop Timer", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=10)
        
        self.finish_button = tk.Button(root, text="Finish Time", command=self.finish_timer, state=tk.DISABLED)
        self.finish_button.pack(pady=10)
        
        self.update_timer()

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.finish_button.config(state=tk.NORMAL)

    def stop_timer(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.finish_button.config(state=tk.NORMAL)

    def finish_timer(self):
        self.running = False
        global duration
        duration = 0
        self.label.config(text="Time left: 0 seconds")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.finish_button.config(state=tk.DISABLED)

    def update_timer(self):
        if self.running:
            global duration
            self.label.config(text=f"Time left: {duration} seconds")
            if duration > 0:
                duration -= 1
                self.label.after(1000, self.update_timer)  # Update every 1000ms (1 second)

class DatabaseConnection:
    def __init__(self):
        try:
            # Establish the database connection
            self.conn = psycopg2.connect(
                dbname="Registration System",
                user="postgres",
                password="12345",
                host="localhost",
                port="5432"
            )
            self.cursor = self.conn.cursor()
        except psycopg2.OperationalError as e:
            print(f"Error connecting to the database: {e}")

    def execute_query(self, query, data=None):
        try:
            if data:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error executing query: {e}")
            return None

    def fetch_data(self):
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

class StartApp:
    def __init__(self):
        # Create a main window
        self.window = tk.Tk()

        #getting screen width and height of display
        #width = self.window.winfo_screenwidth() 
        #height = self.window.winfo_screenheight()
        #setting tkinter window size
        #self.window.geometry("%dx%d" % (width, height))

        # setting attribute
        self.window.state('zoomed')

        # Set the title of the window
        self.window.title("Project Course Registration System")

        # Create a custom font with a bold style
        custom_font = ("Helvetica", 12, "bold")

        # Create a button widget to open a new window
        admin_button = tk.Button(self.window, text="Admin Log In", bg="#99FFFF", fg="#994C00", padx=20, pady=10, font=custom_font, borderwidth=5, relief="ridge", command=self.open_admin_login)
        admin_button.place(relx=0.5, rely=0.4, anchor='center')

        instructor_button = tk.Button(self.window, text="Instructor Log In", bg="#99FFFF", fg="#994C00", padx=20, pady=10, font=custom_font, borderwidth=5, relief="ridge", command=self.open_instructor_login)
        instructor_button.place(relx=0.5, rely=0.5, anchor='center')

        student_button = tk.Button(self.window, text="Student Log In", bg="#99FFFF", fg="#994C00", padx=20, pady=10, font=custom_font, borderwidth=5, relief="ridge", command=self.open_student_login)
        student_button.place(relx=0.5, rely=0.6, anchor='center')

        label = tk.Label(self.window, text="Project Course Registration System", font=("Helvetica", 25, "bold"), fg="brown", pady=100)
        label.pack()


        # Add widgets and logic here

    def open_admin_login(self):
        admin_obj = Admin()
        admin_obj.login()

    def open_instructor_login(self):
        instructor_obj = Instructor()
        instructor_obj.login()

    def open_student_login(self):
        student_obj = Student()
        student_obj.login()

    def run(self):
        # Start the tkinter main loop
        self.window.mainloop()
    
class Admin:
    def __init__(self):
        self.login_window = tk.Tk()
        self.db = DatabaseConnection()

    def login(self):
        
        self.login_window.title("Admin Log In")
        self.login_window.state("zoomed")

        # Add content and widgets for the admin panel here
        # Create a Label widget to display text
        username_label = tk.Label(self.login_window, text="Username : ", font=("Helvetica", 15, "bold"), fg="brown")
        username_label.place(relx=0.35, rely=0.4)

        password_label = tk.Label(self.login_window, text="Password : ", font=("Helvetica", 15, "bold"), fg="brown")
        password_label.place(relx=0.35, rely=0.5)

        # Create an Entry widget for text input
        self.username_field = tk.Entry(self.login_window, width=20, font=('Arial 15'))
        self.username_field.place(relx=0.45, rely=0.4)

        self.password_field = tk.Entry(self.login_window, width=20, font=('Arial 15'), show="*")
        self.password_field.place(relx=0.45, rely=0.5)

        submit_button = tk.Button(self.login_window, text="Submit", bg="#99FFFF", fg="#994C00", padx=15, pady=4, font=("Helvetica", 12, "bold"), borderwidth=5, relief="ridge", command=self.check_credentials)
        submit_button.place(relx=0.49, rely=0.6)

    def check_credentials(self):
        username = self.username_field.get()
        password = self.password_field.get()
        
        self.db = DatabaseConnection()
        # Query the database to check the credentials
        select_query = "SELECT username,password FROM admin WHERE username = %s AND password = %s"
        data = (username, password)

        self.db.execute_query(select_query, data)
        result = self.db.fetch_data()

        if result:
            Admin.close_login(self)
        else:
            error_label = tk.Label(self.login_window, text="Invalid username or password!", font=("Helvetica", 15, "bold"), fg="red")
            error_label.place(relx=0.37, rely=0.3)

    def close_login(self):
        self.login_window.destroy()
        self.dashboard()

    def dashboard(self):
        window = tk.Toplevel()
        window.title("Admin Dashboard")
        window.state("zoomed")

        """
        def open_tab(tab_name):
            # Function to open a tab
            tab_control.select(tab_name)
        """

        # Create a menu bar
        menu = tk.Menu(window)
        window.config(menu=menu)

        # Create a File menu
        instructor_menu = tk.Menu(menu)
        menu.add_cascade(label="Instructor", menu=instructor_menu)
        instructor_menu.add_command(label="Generate", command=self.define_generate_instructor)
        #file_menu.add_command(label="Open")
        instructor_menu.add_separator()
        instructor_menu.add_command(label="Exit", command=window.quit)

        # Create a Help menu
        student_menu = tk.Menu(menu)
        menu.add_cascade(label="Student", menu=student_menu)
        student_menu.add_command(label="Generate", command=self.define_generate_student)
        student_menu.add_command(label="Generate without Lessons", command=self.define_generate_student_without_lesson)

        # Create a Help menu
        message_menu = tk.Menu(menu)
        menu.add_cascade(label="Message", menu=message_menu)
        message_menu.add_command(label="Set Number of Characters", command=self.set_number_of_characters_window)

        # Create a Help menu
        time_menu = tk.Menu(menu)
        menu.add_cascade(label="Time", menu=time_menu)
        time_menu.add_command(label="Set Time", command=self.set_time_window)

        # Create a Help menu
        assign_menu = tk.Menu(menu)
        menu.add_cascade(label="Assignment", menu=assign_menu)
        assign_menu.add_command(label="Random Assignment", command=self.random_assignment)
        assign_menu.add_command(label="Assignment by Grade Point Average")
        assign_menu.add_command(label="Assignment by Specific Lessons")

        # Create tabs
        tab_control = ttk.Notebook(window)
        
        # Tab 1
        self.instructor_tab = ttk.Frame(tab_control)
        tab_control.add(self.instructor_tab, text="Instructor")
        instructor_label = tk.Label(self.instructor_tab, text="Instructor Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        instructor_label.pack()
        #button1 = tk.Button(tab1, text="Open Tab 2", command=lambda: open_tab(tab2))
        #button1.pack()

        # Create a Treeview widget (the table)
        self.instructor_tree = ttk.Treeview(self.instructor_tab, columns=("Registry No", "Title", "Name", "Surname", "Quota", "Lesson", "Field"), show="headings")
        self.instructor_tree.column("#1", width=100)
        self.instructor_tree.column("#5", width=100)

        self.instructor_tree.heading("#1", text="Registry No")
        self.instructor_tree.heading("#2", text="Title")
        self.instructor_tree.heading("#3", text="Name")
        self.instructor_tree.heading("#4", text="Surname")
        self.instructor_tree.heading("#5", text="Quota")
        self.instructor_tree.heading("#6", text="Lesson")
        self.instructor_tree.heading("#7", text="Field")
        self.instructor_tree.pack()
        self.get_instructor_data(0)
        
        # Create the context menu
        self.instructor_m = tk.Menu(self.instructor_tree, tearoff=0)
        self.instructor_m.add_command(label="Update", command=self.update_instructor)
        self.instructor_m.add_command(label="Delete", command=self.delete_instructor)
        self.instructor_m.add_separator()

        instructor_refresh_button = tk.Button(self.instructor_tab, text="Refresh", command=lambda: self.get_instructor_data(1))
        instructor_refresh_button.place(relx=0.1, rely=0.03)
        
        # Tab 2
        self.student_tab = ttk.Frame(tab_control)
        tab_control.add(self.student_tab, text="Student")
        student_label = tk.Label(self.student_tab, text="Student Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        student_label.pack()
        #button2 = tk.Button(tab2, text="Open Tab 1", command=lambda: open_tab(tab1))
        #button2.pack()
        
        # Create a Treeview widget (the table)
        self.student_tree = ttk.Treeview(self.student_tab, columns=("Student No", "Name", "Surname", "Status", "Field"), show="headings")
        self.student_tree.heading("#1", text="Student No")
        self.student_tree.heading("#2", text="Name")
        self.student_tree.heading("#3", text="Surname")
        self.student_tree.heading("#4", text="Status")
        self.student_tree.heading("#5", text="Field")
        self.student_tree.pack()
        self.get_student_data(0) 
        
        # Create the context menu
        self.student_m = tk.Menu(self.student_tree, tearoff=0)
        self.student_m.add_command(label="Update", command=self.update_student)
        self.student_m.add_command(label="Delete", command=self.delete_student)
        self.student_m.add_command(label="Assign Instructor", command=self.assign_instructor)
        self.student_m.add_separator()

        student_refresh_button = tk.Button(self.student_tab, text="Refresh", command=lambda: self.get_student_data(1))
        student_refresh_button.place(relx=0.1, rely=0.03)

        # Tab 3
        self.demand_tab = ttk.Frame(tab_control)
        tab_control.add(self.demand_tab, text="Demand")
        student_label = tk.Label(self.demand_tab, text="Demand Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        student_label.pack()
        #button2 = tk.Button(tab2, text="Open Tab 1", command=lambda: open_tab(tab1))
        #button2.pack()

        # Create a Treeview widget (the table)
        self.demand_tree = ttk.Treeview(self.demand_tab, columns=("Lesson Name", "Field", "Title", "Instructor Name", "Instructor Surname", "Student No", "Name", "Surname"), show="headings")
        
        self.demand_tree.column("#1", width=100)  # Set the width of column 1 (Lesson Name) to 100 pixels
        self.demand_tree.column("#2", width=150)  # Set the width of column 2 (Field) to 100 pixels
        self.demand_tree.column("#3", width=150)  # Set the width of column 3 (Title) to 100 pixels
        self.demand_tree.column("#4", width=100)  # Set the width of column 4 (Name) to 100 pixels
        self.demand_tree.column("#5", width=100)  # Set the width of column 5 (Surname) to 100 pixels
        self.demand_tree.column("#6", width=75)  # Set the width of column 6 (Student No) to 100 pixels
        self.demand_tree.column("#7", width=100)  # Set the width of column 7 (Name) to 100 pixels
        self.demand_tree.column("#8", width=100)
        
        self.demand_tree.heading("#1", text="Lesson Name")
        self.demand_tree.heading("#2", text="Field")
        self.demand_tree.heading("#3", text="Title")
        self.demand_tree.heading("#4", text="Name")
        self.demand_tree.heading("#5", text="Surname")
        self.demand_tree.heading("#6", text="Student No")
        self.demand_tree.heading("#7", text="Name")
        self.demand_tree.heading("#8", text="Surname")
        self.demand_tree.pack()
        self.get_demand_data(0) 
        
        demand_refresh_button = tk.Button(self.demand_tab, text="Refresh", command=lambda: self.get_demand_data(1))
        demand_refresh_button.place(relx=0.1, rely=0.03)

        # Create the context menu
        #self.lesson_m = tk.Menu(self.lesson_tree, tearoff=0)
        #self.lesson_m.add_command(label="Update", command=self.update_student)
        #self.lesson_m.add_command(label="Delete", command=self.delete_student)
        #self.lesson_m.add_separator()

        # Tab 4
        self.lesson_tab = ttk.Frame(tab_control)
        tab_control.add(self.lesson_tab, text="Agreed Lesson")
        student_label = tk.Label(self.lesson_tab, text="Agreed Lesson Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        student_label.pack()
        #button2 = tk.Button(tab2, text="Open Tab 1", command=lambda: open_tab(tab1))
        #button2.pack()

        # Create a Treeview widget (the table)
        self.lesson_tree = ttk.Treeview(self.lesson_tab, columns=("Lesson Name", "Field", "Title", "Instructor Name", "Instructor Surname", "Student No", "Name", "Surname"), show="headings")
        
        self.lesson_tree.column("#1", width=100)  # Set the width of column 1 (Lesson Name) to 100 pixels
        self.lesson_tree.column("#2", width=150)  # Set the width of column 2 (Field) to 100 pixels
        self.lesson_tree.column("#3", width=150)  # Set the width of column 3 (Title) to 100 pixels
        self.lesson_tree.column("#4", width=100)  # Set the width of column 4 (Name) to 100 pixels
        self.lesson_tree.column("#5", width=100)  # Set the width of column 5 (Surname) to 100 pixels
        self.lesson_tree.column("#6", width=75)  # Set the width of column 6 (Student No) to 100 pixels
        self.lesson_tree.column("#7", width=100)  # Set the width of column 7 (Name) to 100 pixels
        self.lesson_tree.column("#8", width=100)
        
        self.lesson_tree.heading("#1", text="Lesson Name")
        self.lesson_tree.heading("#2", text="Field")
        self.lesson_tree.heading("#3", text="Title")
        self.lesson_tree.heading("#4", text="Name")
        self.lesson_tree.heading("#5", text="Surname")
        self.lesson_tree.heading("#6", text="Student No")
        self.lesson_tree.heading("#7", text="Name")
        self.lesson_tree.heading("#8", text="Surname")
        self.lesson_tree.pack()
        self.get_lesson_data(0) 
        
        lesson_refresh_button = tk.Button(self.lesson_tab, text="Refresh", command=lambda: self.get_lesson_data(1))
        lesson_refresh_button.place(relx=0.1, rely=0.03)

        # Create the context menu
        #self.lesson_m = tk.Menu(self.lesson_tree, tearoff=0)
        #self.lesson_m.add_command(label="Update", command=self.update_student)
        #self.lesson_m.add_command(label="Delete", command=self.delete_student)
        #self.lesson_m.add_separator()

        # Tab 5
        self.interest_tab = ttk.Frame(tab_control)
        tab_control.add(self.interest_tab, text="Interest Field")
        interest_label = tk.Label(self.interest_tab, text="Interest Field Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        interest_label.pack()
        #button1 = tk.Button(tab1, text="Open Tab 2", command=lambda: open_tab(tab2))
        #button1.pack()

        # Create a Treeview widget (the table)
        self.interest_tree = ttk.Treeview(self.interest_tab, columns=("Field No", "Interest Field"), show="headings")
        
        self.interest_tree.heading("#1", text="Field No")
        self.interest_tree.heading("#2", text="Interest Field")
        self.interest_tree.pack()
        self.get_interest_data(0)
        
        # Create the context menu
        self.interest_m = tk.Menu(self.interest_tree, tearoff=0)
        self.interest_m.add_command(label="Update", command=self.update_interest)
        self.interest_m.add_command(label="Delete", command=self.delete_interest)
        self.interest_m.add_separator()

        # Button to add selected interests to the instructor_interest table
        add_button = tk.Button(self.interest_tab, text="Add Interest", bg="#99FFFF", fg="#994C00", padx=5, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge", command=self.open_add_interest_window)
        add_button.pack(pady=50)

        interest_refresh_button = tk.Button(self.interest_tab, text="Refresh", command=lambda: self.get_instructor_data(1))
        interest_refresh_button.place(relx=0.1, rely=0.03)
        
        # Set the default tab to open
        tab_control.select(self.instructor_tab)

        tab_control.pack(expand=1, fill="both")

        # Start the tkinter main loop
        window.mainloop()

    def random_assignment(self):
        select_data_query = "SELECT s.student_no FROM student s LEFT JOIN deal d ON s.student_no = d.student_no AND d.deal_status = 1 WHERE d.deal_id IS NULL OR d.deal_status = 0"
        self.db.execute_query(select_data_query)
        student_results = self.db.fetch_data()

        select_data_query = "SELECT i.registry_no, iol.opened_lesson_id FROM instructor i INNER JOIN instructor_opened_lesson iol ON i.registry_no=iol.registry_no WHERE i.quota>0"
        self.db.execute_query(select_data_query)
        instructor_results = self.db.fetch_data()
    
        # Insert data into the table
        #for item in results:
            #self.lesson_tree.insert("", "end", values=item)
    
        for i,student in enumerate(student_results):
            insert_query = "INSERT INTO deal (student_no, registry_no, opened_lesson_id, deal_status) VALUES (%s, %s, %s, %s)"
            data_to_insert = (student_results[i][0], instructor_results[i][0], instructor_results[i][1], 1)
            self.db.execute_query(insert_query, data_to_insert)
            self.db.commit()
        
            # Perform the update in the database
            update_query = "UPDATE instructor SET quota = quota-1 WHERE registry_no = %s"
            data = (instructor_results[i][0],)
            self.db.execute_query(update_query, data)
            self.db.commit()
        
        self.make_confirmation_window("Successful")

    def get_instructor_data(self, refresh):
        if(refresh==1):
            # Clear existing data in the Treeview
            for item in self.instructor_tree.get_children():
                self.instructor_tree.delete(item)
        
        select_data_query = "SELECT i.registry_no, i.title, i.name, i.surname, i.quota, ol.name, inte.field FROM instructor AS i INNER JOIN instructor_opened_lesson AS iol on i.registry_no=iol.registry_no INNER JOIN opened_lesson as ol on iol.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli ON ol.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte on oli.interest_id=inte.interest_id"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.instructor_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        self.instructor_tree.bind("<Button-3>", self.do_popup_instructor)

    def refresh_instructor_data(self):
        # Clear existing data in the Treeview
        for item in self.instructor_tree.get_children():
            self.instructor_tree.delete(item)

        # Fetch and insert the updated data
        self.get_instructor_data(0)

    def do_popup_instructor(self, event):
        item = self.instructor_tree.item(self.instructor_tree.selection())  # Get the selected item
        if item:
            self.selected_registry_no = item['values'][0]  # Extract the 'registry_no' value
            self.instructor_m.tk_popup(event.x_root, event.y_root)

    def delete_instructor(self):
        if hasattr(self, 'selected_registry_no'):
            delete_query_1 = "DELETE FROM instructor_opened_lesson WHERE registry_no = %s"
            data = (self.selected_registry_no,)
            self.db.execute_query(delete_query_1, data)
            self.db.commit()

            delete_query_2 = "DELETE FROM instructor_interest WHERE registry_no = %s"
            data = (self.selected_registry_no,)
            self.db.execute_query(delete_query_2, data)
            self.db.commit()

            delete_query_3 = "DELETE FROM instructor WHERE registry_no = %s"
            data = (self.selected_registry_no,)
            self.db.execute_query(delete_query_3, data)
            self.db.commit()

            # Remove the deleted item from the Treeview
            selected_item = self.instructor_tree.selection()
            if selected_item:
                self.instructor_tree.delete(selected_item)

            # Optionally clear the selected_registry_no attribute
            del self.selected_registry_no

    def update_instructor(self):
        selected_item = self.instructor_tree.selection()
        if selected_item:
            selected_values = self.instructor_tree.item(selected_item, "values")
            if selected_values:
                # Open the update window with the instructor's data for editing
                self.open_instructor_update_window(selected_values)

    def open_instructor_update_window(self, selected_values):
        self.update_instructor_window = tk.Toplevel()
        self.update_instructor_window.title("Update Instructor")
        self.update_instructor_window.state("zoomed")
        # Create input fields and labels for updating instructor data
        # You can design and populate this window as needed

        # Example: Create an entry field for updating the instructor's name
        self.title_label = tk.Label(self.update_instructor_window, text="Title")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.update_instructor_window, width=30)
        self.title_entry.insert(0, selected_values[1])  # Pre-fill with the instructor's current name
        self.title_entry.pack()

        self.name_label = tk.Label(self.update_instructor_window, text="Name")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.update_instructor_window, width=30)
        self.name_entry.insert(0, selected_values[2])  # Pre-fill with the instructor's current name
        self.name_entry.pack()

        self.surname_label = tk.Label(self.update_instructor_window, text="Surname")
        self.surname_label.pack()
        self.surname_entry = tk.Entry(self.update_instructor_window, width=30)
        self.surname_entry.insert(0, selected_values[3])  # Pre-fill with the instructor's current name
        self.surname_entry.pack()

        self.quota_label = tk.Label(self.update_instructor_window, text="Quota")
        self.quota_label.pack()
        self.quota_entry = tk.Entry(self.update_instructor_window, width=30)
        self.quota_entry.insert(0, selected_values[4])  # Pre-fill with the instructor's current name
        self.quota_entry.pack()

        self.lesson_label = tk.Label(self.update_instructor_window, text="Lesson")
        self.lesson_label.pack()
        self.lesson_entry = tk.Entry(self.update_instructor_window, width=30)
        self.lesson_entry.insert(0, selected_values[5])  # Pre-fill with the instructor's current name
        self.lesson_entry.pack()

        # Create a button to save the updates
        save_button = tk.Button(self.update_instructor_window, text="Save", command=self.save_instructor_updates, bg="#99FFFF", fg="#994C00", padx=10, pady=2, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge")
        save_button.place(relx=0.48, rely=0.32)

    def save_instructor_updates(self):
        # Get the values from the input fields in the update window
        title = self.title_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        quota = self.quota_entry.get()
        lesson = self.lesson_entry.get()
        
        # Check if all required fields are filled
        if not (title and name and surname and quota and lesson):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        # Perform the update in the database
        update_query = "UPDATE instructor SET title = %s, name = %s, surname = %s, quota = %s WHERE registry_no = %s"
        data = (title, name, surname, quota, self.selected_registry_no)
        self.db.execute_query(update_query, data)
        self.db.commit()

        select_query = "SELECT opened_lesson_id FROM opened_lesson WHERE name = %s"
        data_2 = (lesson,)
        self.db.execute_query(select_query, data_2)
        results = self.db.fetch_data()

        update_query_2 = "UPDATE instructor_opened_lesson SET opened_lesson_id = %s WHERE registry_no = %s"
        data_3 = (results[0], self.selected_registry_no)
        self.db.execute_query(update_query_2, data_3)
        self.db.commit()

        # Close the update window
        self.update_instructor_window.destroy()

        # Refresh the Treeview to reflect the changes
        self.refresh_instructor_data()

    def define_generate_instructor(self):
        self.define_generate_instructor_window = tk.Toplevel()
        self.define_generate_instructor_window.title("Generate Instructor")
        self.define_generate_instructor_window.geometry("300x200+500+250")

        instructor_number_label = tk.Label(self.define_generate_instructor_window, text="Instructor Number to Generate : ", font=("Helvetica", 10, "bold"), fg="brown")
        instructor_number_label.place(relx=0.05, rely=0.3)

        self.instructor_number_field = tk.Entry(self.define_generate_instructor_window, width=3, font=('Arial 12'))
        self.instructor_number_field.place(relx=0.75, rely=0.3)
        
        instructor_generate_button = tk.Button(self.define_generate_instructor_window, text="Generate", bg="#99FFFF", fg="#994C00", padx=5, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge", command=self.generate_instructor)
        instructor_generate_button.place(relx=0.35, rely=0.6)

    def generate_instructor(self):
        titles = ["Dr.", "Associate Professor", "Professor"]
        names = ["Ahmet", "Mehmet", "Serap", "Buse", "Hasan", "Kemal", "Yusuf", "Ömer", "Zeynep", "Mustafa", "Ali", "Fatma", "Hande", "Kerem", "İbrahim", "Yunus", "Cemre", "Derya", "Ekrem", "Fatih", "Füsun", "İsmail", "Leyla", "Mahmut", "Melike", "Nalan", "Nazım", "Perihan", "Reyhan", "Tarık", "Veysel", "Yasemin", "İshak", "İhsan", "Gamze", "Güzide", "Celil", "Selim", "Aynur", "Adem", "Ufuk", "Nilgün", "Zehra", "Hamdi", "Veli"]
        surnames = ["Yılmaz", "Kaya", "Doğan", "Acar", "Açıkalın", "Adıvar", "Ağaoğlu", "Balaban", "Baltacı", "Barbarosoğlu", "Başoğlu", "Baydar", "Berberoğlu", "Beşikçi", "Biçer", "Boduroğlu", "Boz", "Caymaz", "Çetin", "Çolak", "Çörekçi", "Davulcu", "Demirkan", "Duman", "Eğilmez", "Ekici", "Gedik", "Güngör", "Hancı", "İpekçi", "Kahveci", "Karabay", "Karaca", "Karakaş", "Koşar", "Mutlu", "Odabaşı", "Orbay", "Ozansoy", "Ölmez", "Özden", "Özyürek", "Tosun"]
        quotas = [10, 20, 30, 40, 50]
        self.instructor_number = self.instructor_number_field.get()
        number = int(self.instructor_number)
        for i in range(0, number):
            random_number = random.randint(0, 2)
            title = titles[random_number]
            random_number = random.randint(0, 44)
            name = names[random_number]
            random_number = random.randint(0, 42)
            surname = surnames[random_number]
            random_number = random.randint(0, 4)
            quota = quotas[random_number]
            
            insert_query = "INSERT INTO instructor (title, name, surname, quota, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
            data_to_insert = (title, name, surname, quota, name, surname)

            self.db.execute_query(insert_query, data_to_insert)
            self.db.commit()

        select_data_query = "SELECT registry_no FROM instructor"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()

        for result in results:
            random_number = random.randint(1, 10)
            opened_lesson_id = random_number
            insert_query_2 = "INSERT INTO instructor_opened_lesson (registry_no, opened_lesson_id) VALUES (%s, %s)"
            data_to_insert_2 = (result, opened_lesson_id)        
            self.db.execute_query(insert_query_2, data_to_insert_2)
            self.db.commit()    

            select_data_query = "SELECT interest_id FROM opened_lesson_interest WHERE opened_lesson_id = %s"
            data = (opened_lesson_id,)
            self.db.execute_query(select_data_query, data)
            interest_id = self.db.fetch_data()
            insert_query_3 = "INSERT INTO instructor_interest (registry_no, interest_id) VALUES (%s, %s)"
            data_to_insert_3 = (result, interest_id[0])  
            self.db.execute_query(insert_query_3, data_to_insert_3)
            self.db.commit()  

        self.get_instructor_data(0)
        success_label = tk.Label(self.define_generate_instructor_window, text="SUCCESSFUL", font=("Helvetica", 12, "bold"), fg="green")
        success_label.place(relx=0.3, rely=0.1)

        self.define_generate_instructor_window.after(1000, self.define_generate_instructor_window.destroy)

    def get_student_data(self, refresh):
        if(refresh==1):
            # Clear existing data in the Treeview
            for item in self.student_tree.get_children():
                self.student_tree.delete(item)

        select_data_query = "SELECT s.student_no, s.name, s.surname, d.deal_status, i.field FROM student AS s INNER JOIN student_interest AS si on s.student_no=si.student_no INNER JOIN interest as i on si.interest_id=i.interest_id LEFT JOIN deal AS d ON s.student_no=d.student_no"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            item = list(item)
            if item[3]==1:
                item[3]="deal"
            else:
                item[3]="non-deal"
            item = tuple(item)
            self.student_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        self.student_tree.bind("<Button-3>", self.do_popup_student)

    def refresh_student_data(self):
        # Clear existing data in the Treeview
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        # Fetch and insert the updated data
        self.get_student_data(0)

    def do_popup_student(self, event):
        item = self.student_tree.item(self.student_tree.selection())  # Get the selected item
        if item:
            self.selected_student_no = item['values'][0]  # Extract the 'registry_no' value
            self.student_m.tk_popup(event.x_root, event.y_root)

    def delete_student(self):
        if hasattr(self, 'selected_student_no'):
            delete_query_1 = "DELETE FROM student_interest WHERE student_no = %s"
            data = (self.selected_student_no,)
            self.db.execute_query(delete_query_1, data)
            self.db.commit()

            delete_query_2 = "DELETE FROM student WHERE student_no = %s"
            data = (self.selected_student_no,)
            self.db.execute_query(delete_query_2, data)
            self.db.commit()

            # Remove the deleted item from the Treeview
            selected_item = self.student_tree.selection()
            if selected_item:
                self.student_tree.delete(selected_item)

            # Optionally clear the selected_registry_no attribute
            del self.selected_student_no

    def update_student(self):
        selected_item = self.student_tree.selection()
        if selected_item:
            selected_values = self.student_tree.item(selected_item, "values")
            if selected_values:
                self.open_student_update_window(selected_values)

    def open_student_update_window(self, selected_values):
        self.update_student_window = tk.Toplevel()
        self.update_student_window.title("Update Student")
        self.update_student_window.state("zoomed")
        # Create input fields and labels for updating instructor data
        # You can design and populate this window as needed

        # Example: Create an entry field for updating the instructor's name
        self.student_no_label = tk.Label(self.update_student_window, text="Student No")
        self.student_no_label.pack()
        self.student_no_entry = tk.Entry(self.update_student_window, width=30)
        self.student_no_entry.insert(0, selected_values[0])  # Pre-fill with the instructor's current name
        self.student_no_entry.pack()

        self.name_label = tk.Label(self.update_student_window, text="Name")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.update_student_window, width=30)
        self.name_entry.insert(0, selected_values[1])  # Pre-fill with the instructor's current name
        self.name_entry.pack()

        self.surname_label = tk.Label(self.update_student_window, text="Surname")
        self.surname_label.pack()
        self.surname_entry = tk.Entry(self.update_student_window, width=30)
        self.surname_entry.insert(0, selected_values[2])  # Pre-fill with the instructor's current name
        self.surname_entry.pack()

        self.status_label = tk.Label(self.update_student_window, text="Status")
        self.status_label.pack()
        self.status_entry = tk.Entry(self.update_student_window, width=30)
        self.status_entry.insert(0, selected_values[3])  # Pre-fill with the instructor's current name
        self.status_entry.pack()

        self.field_label = tk.Label(self.update_student_window, text="Field")
        self.field_label.pack()
        self.field_entry = tk.Entry(self.update_student_window, width=30)
        self.field_entry.insert(0, selected_values[4])  # Pre-fill with the instructor's current name
        self.field_entry.pack()

        # Create a button to save the updates
        save_button = tk.Button(self.update_student_window, text="Save", command=self.save_student_updates, bg="#99FFFF", fg="#994C00", padx=10, pady=2, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge")
        save_button.place(relx=0.48, rely=0.32)

    def save_student_updates(self):
        # Get the values from the input fields in the update window
        student_no = self.student_no_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        status = self.status_entry.get()
        field = self.field_entry.get()
        
        # Check if all required fields are filled
        if not (student_no and name and surname and status and field):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        
        if status=="deal":
            status = 1
        else:
            status = 0
        # Perform the update in the database
        update_query = "UPDATE student SET student_no = %s, name = %s, surname = %s WHERE student_no = %s"
        data = (student_no, name, surname, self.selected_student_no)
        self.db.execute_query(update_query, data)
        self.db.commit()

        select_query = "SELECT interest_id FROM interest WHERE field = %s"
        data_2 = (field,)
        self.db.execute_query(select_query, data_2)
        results = self.db.fetch_data()

        update_query_2 = "UPDATE student_interest SET interest_id = %s WHERE student_no = %s"
        data_3 = (results[0], self.selected_student_no)
        self.db.execute_query(update_query_2, data_3)
        self.db.commit()

        # Close the update window
        self.update_student_window.destroy()

        # Refresh the Treeview to reflect the changes
        self.refresh_student_data()

    def define_generate_student(self):
        self.define_generate_student_window = tk.Toplevel()
        self.define_generate_student_window.title("Generate Student")
        self.define_generate_student_window.geometry("300x200+500+250")

        student_number_label = tk.Label(self.define_generate_student_window, text="Student Number to Generate : ", font=("Helvetica", 10, "bold"), fg="brown")
        student_number_label.place(relx=0.05, rely=0.3)

        self.student_number_field = tk.Entry(self.define_generate_student_window, width=3, font=('Arial 12'))
        self.student_number_field.place(relx=0.75, rely=0.3)
        
        student_generate_button = tk.Button(self.define_generate_student_window, text="Generate", bg="#99FFFF", fg="#994C00", padx=5, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge", command=self.generate_student)
        student_generate_button.place(relx=0.35, rely=0.6)

    def define_generate_student_without_lesson(self):
        self.define_generate_student_window = tk.Toplevel()
        self.define_generate_student_window.title("Generate Student")
        self.define_generate_student_window.geometry("300x200+500+250")

        student_number_label = tk.Label(self.define_generate_student_window, text="Student Number to Generate : ", font=("Helvetica", 10, "bold"), fg="brown")
        student_number_label.place(relx=0.05, rely=0.3)

        self.student_number_field = tk.Entry(self.define_generate_student_window, width=3, font=('Arial 12'))
        self.student_number_field.place(relx=0.75, rely=0.3)
        
        student_generate_button = tk.Button(self.define_generate_student_window, text="Generate", bg="#99FFFF", fg="#994C00", padx=5, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge", command=lambda: self.generate_student(1))
        student_generate_button.place(relx=0.35, rely=0.6)

    def generate_student(self, param=0):
        names = ["Akasya", "Arda", "Alya", "Baha", "Barış", "Beren", "Berkan", "Cemre", "Ceyda", "Caner", "Çağla", "Çağdaş", "Deren", "Dilara", "Demirkan", "Edis", "Efe", "Ece", "Ezgi", "Ferda", "Fulya", "Cemre", "Hakan", "İlkay", "İlker", "Kaan", "Gizem", "Helin", "Irmak", "Işıl", "İdil", "Kuzey", "Mert", "Nusret", "Olcay", "Jale", "Kumru", "Melda", "Naz", "Nil", "Oya", "Övünç", "Reha", "Sertaç", "Öykü", "Pelin", "Selin", "Şule", "Taner", "Turgay", "Vedat", "Zafer", "Tülin", "Yonca"]
        surnames = ["Şen", "Kandemir", "Çevik", "Tüten", "Yücel", "Sönmez", "Ertekin", "Dede", "Uyanık", "Aslan", "Akbulut", "Uz", "Kaya", "Kulaç", "Selvi", "Akpınar", "Abacıoğlu", "Işık", "Özer", "Özdemir", "Tahtacı", "Büyükcam", "Kulaksız", "Aksel", "Eroğlu", "Karakum", "Dal", "Yiğit", "Gümüşay", "Yılmaz", "Sezer", "Doğan", "Demir", "Kayayurt", "Turgut", "Aldinç", "Tekin", "Almacıoğlu", "Öner", "Yaman", "Şentürk", "Yıldız", "Güler", "Koç", "Korkmaz", "Aydoğan"]
        grades = ["AA", "BA", "BB", "CB", "CC", "DC"]
        lessons = ["Atatürk İlkeleri ve İnkilap Tarihi I (UE)", "Atatürk İlkeleri ve İnkilap Tarihi II (UE)", "Oyun Teorisi", "AFETLER VE ZARALARININ AZALTILMASI", "Türk Dili I (UE)", "Türk Dili II (UE)", "İngilizce I (UE)", "Bilgisayar Laboratuvarı I", "Bilgisayar Mühendisliğine Giriş", "Programlama I", "Fizik I", "Lineer Cebir", "Matematik I", "Bilgisayar Laboratuvarı II", "Elektrik Devre Temelleri ve Uygulamaları", "Programlama II", "Fizik II", "Matematik II", "Veri Yapıları ve Algoritmaları", "Programlama Laboratuvarı - I", "Mantıksal Tasarım ve Uygulamaları", "Diferansiyel Denklemler", "Kesikli Matematik", "Nesneye Yönelik Programlama", "Bilgisayar Organizasyonu ve Mimarisi", "electronic", "Veritabanı Yönetimi", "Programlama Laboratuvarı – II", "Sistem Programlama", "Türkiye İktisat Tarihi", "Olasılık ve Raslantı Değişkenleri", "Elektronik ve Uygulamaları", "İngilizce II (UE)"]
        total_lessons_number = [10, 15, 20, 25, 30]
        self.student_number = self.student_number_field.get()
        number = int(self.student_number)
        for i in range(0, number):
            random_number = random.randint(0, 53)
            name = names[random_number]
            random_number = random.randint(0, 45)
            surname = surnames[random_number]
            
            insert_query = "INSERT INTO student (name, surname, username, password) VALUES (%s, %s, %s, %s)"
            data_to_insert = (name, surname, name, surname)

            self.db.execute_query(insert_query, data_to_insert)
            self.db.commit()

            if(param==0):
                random_number = random.randint(0, 4)
                total_lesson_number = total_lessons_number[random_number]
                for j in range(0, total_lesson_number):
                    select_data_query = "SELECT student_no FROM student ORDER BY student_no DESC LIMIT 1;"
                    self.db.execute_query(select_data_query)
                    results = self.db.fetch_data()

                    random_number = random.randint(0, 5)
                    mark = grades[random_number]
                    insert_query = "INSERT INTO student_lesson (student_no, lesson_id, mark) VALUES (%s, %s, %s)"
                    data_to_insert = (results[0], j+1, mark)

                    self.db.execute_query(insert_query, data_to_insert)
                    self.db.commit()

        select_data_query = "SELECT student_no FROM student ORDER BY student_no DESC LIMIT %s"
        data = (number,)
        self.db.execute_query(select_data_query, data)
        results = self.db.fetch_data()

        for result in results:
            random_number = random.randint(1, 10)
            student_interest_id = random_number
            insert_query_2 = "INSERT INTO student_interest (student_no, interest_id) VALUES (%s, %s)"
            data_to_insert_2 = (result, student_interest_id)        
            self.db.execute_query(insert_query_2, data_to_insert_2)
            self.db.commit()    

        self.refresh_student_data()
        success_label = tk.Label(self.define_generate_student_window, text="SUCCESSFUL", font=("Helvetica", 12, "bold"), fg="green")
        success_label.place(relx=0.3, rely=0.1)

        self.define_generate_student_window.after(1000, self.define_generate_student_window.destroy)

    def set_number_of_characters_window(self):
        self.number_of_characters_window = tk.Toplevel()
        self.number_of_characters_window.title("Set Number of Characters")
        self.number_of_characters_window.geometry("300x250+500+250")

        number_label = tk.Label(self.number_of_characters_window, text=f"Current Character Number : {character_number}", font=("Helvetica", 10, "bold"), fg="brown")
        number_label.place(relx=0.05, rely=0.3)

        character_number_label = tk.Label(self.number_of_characters_window, text="Character Number to Set : ", font=("Helvetica", 10, "bold"), fg="brown")
        character_number_label.place(relx=0.05, rely=0.5)

        self.character_number_field = tk.Entry(self.number_of_characters_window, width=7, font=('Arial 12'))
        self.character_number_field.place(relx=0.70, rely=0.5)
        
        character_generate_button = tk.Button(self.number_of_characters_window, text="Set", bg="#99FFFF", fg="#994C00", padx=5, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge", command=self.set_number_of_characters)
        character_generate_button.place(relx=0.35, rely=0.7)

    def set_number_of_characters(self):
        global character_number
        character_number = self.character_number_field.get()

        if(self.character_number_field.get()):
            self.make_confirmation_window("Successful")

            self.number_of_characters_window.after(1000, self.number_of_characters_window.destroy)
        
    def set_time_window(self):
        self.time_window = tk.Toplevel()
        self.time_window.title("Set Time")
        self.time_window.geometry("300x150+500+250")

        time_label = tk.Label(self.time_window, text="Time to Set : ", font=("Helvetica", 10, "bold"), fg="brown")
        time_label.place(relx=0.05, rely=0.3)

        self.time_field = tk.Entry(self.time_window, width=7, font=('Arial 12'))
        self.time_field.place(relx=0.70, rely=0.3)
        
        set_time_button = tk.Button(self.time_window, text="Set", bg="#99FFFF", fg="#994C00", padx=5, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge", command=self.set_time)
        set_time_button.place(relx=0.35, rely=0.6)

    def set_time(self):
        if(self.time_field.get()):
            self.make_confirmation_window("Successful")

            self.time_window.after(1000, self.time_window.destroy)

        timer_window = tk.Tk()
        global duration
        duration = int(self.time_field.get())
        application = TimerApp(timer_window)
        timer_window.mainloop()

    def make_confirmation_window(self, str):
        confirmation_window = tk.Tk()
        confirmation_window.title("Confirmation Window")
        confirmation_window.geometry("300x150+500+250")

        confirmation_label = tk.Label(confirmation_window, text=str, font=("Helvetica", 12, "bold"), fg="green")
        confirmation_label.place(relx=0.1, rely=0.4)
        confirmation_window.after(1000, confirmation_window.destroy)

    def get_lesson_data(self, refresh):
        if(refresh==1):
            # Clear existing data in the Treeview
            for item in self.lesson_tree.get_children():
                self.lesson_tree.delete(item)
        select_data_query = "SELECT ol.name, inte.field, i.title, i.name, i.surname, s.student_no, s.name, s.surname FROM deal AS d INNER JOIN student AS s on d.student_no=s.student_no INNER JOIN instructor as i on d.registry_no=i.registry_no INNER JOIN instructor_opened_lesson AS iol ON d.registry_no=iol.registry_no AND d.opened_lesson_id=iol.opened_lesson_id INNER JOIN opened_lesson AS ol ON d.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli ON d.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte ON oli.interest_id=inte.interest_id WHERE d.deal_status=1"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.lesson_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        #self.lesson_tree.bind("<Button-3>", self.do_popup_student)

    def get_demand_data(self, refresh):
        if(refresh==1):
            # Clear existing data in the Treeview
            for item in self.demand_tree.get_children():
                self.demand_tree.delete(item)
        select_data_query = "SELECT ol.name, inte.field, i.title, i.name, i.surname, s.student_no, s.name, s.surname FROM deal AS d INNER JOIN student AS s on d.student_no=s.student_no INNER JOIN instructor as i on d.registry_no=i.registry_no INNER JOIN instructor_opened_lesson AS iol ON d.registry_no=iol.registry_no AND d.opened_lesson_id=iol.opened_lesson_id INNER JOIN opened_lesson AS ol ON d.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli ON d.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte ON oli.interest_id=inte.interest_id WHERE d.deal_status=0"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.demand_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        #self.lesson_tree.bind("<Button-3>", self.do_popup_student)

    def assign_instructor(self):
        selected_item = self.student_tree.selection()
        if selected_item:
            selected_values = self.student_tree.item(selected_item, "values")
            if selected_values:
                self.open_assign_instructor_window(selected_values)

    def open_assign_instructor_window(self, selected_values):
        self.assign_instructor_window = tk.Toplevel()
        self.assign_instructor_window.title("Assign Instructor")
        self.assign_instructor_window.state("zoomed")
        # Create input fields and labels for updating instructor data
        # You can design and populate this window as needed

        select_data_query = "SELECT i.registry_no, i.title, i.name, i.surname, ol.name, iol.opened_lesson_id FROM instructor i INNER JOIN instructor_opened_lesson iol ON i.registry_no=iol.registry_no INNER JOIN opened_lesson AS ol ON iol.opened_lesson_id=ol.opened_lesson_id WHERE i.quota>0"
        self.db.execute_query(select_data_query)
        instructor_results = self.db.fetch_data()

        selected_instructor_var = tk.StringVar(value="")  # Variable to track the selected instructor
        
        for instructor in instructor_results:
            # Create a Radio button for each instructor
            info = (instructor[0], instructor[5])
            radio_button = ttk.Radiobutton(self.assign_instructor_window, text=f"{instructor[1]} {instructor[2]} {instructor[3]}    {instructor[4]}", value=info, variable=selected_instructor_var)

            # Place the Radio button in the window
            radio_button.pack()

        # Create a button to save the updates
        assign_instructor_button = tk.Button(self.assign_instructor_window, text="Assign Instructor", command=lambda: self.save_assign_instructor(selected_instructor_var.get()), bg="#99FFFF", fg="#994C00", padx=10, pady=2, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge")
        assign_instructor_button.place(relx=0.7, rely=0.15)

    def save_assign_instructor(self, selected_instructor_info):
        # Split the string by whitespace
        registry_no, lesson = selected_instructor_info.split()

        # Convert the resulting substrings to integers if needed
        registry_no = int(registry_no)
        lesson = int(lesson)

        insert_query = "INSERT INTO deal (student_no, registry_no, opened_lesson_id, deal_status) VALUES (%s, %s, %s, %s)"
        data_to_insert = (self.selected_student_no, registry_no, lesson, 1)
        self.db.execute_query(insert_query, data_to_insert)
        self.db.commit()        

        # Perform the update in the database
        update_query = "UPDATE instructor SET quota = quota-1 WHERE registry_no = %s"
        data = (registry_no,)
        self.db.execute_query(update_query, data)
        self.db.commit()

        self.make_confirmation_window("Successful")

    def get_interest_data(self, refresh):
        if(refresh==1):
            # Clear existing data in the Treeview
            for item in self.interest_tree.get_children():
                self.interest_tree.delete(item)
        
        select_data_query = "SELECT interest_id, field FROM interest"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.interest_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        self.interest_tree.bind("<Button-3>", self.do_popup_interest)

    def do_popup_interest(self, event):
        item = self.interest_tree.item(self.interest_tree.selection())  # Get the selected item
        if item:
            self.selected_interest_id = item['values'][0]  # Extract the 'registry_no' value
            self.interest_m.tk_popup(event.x_root, event.y_root)

    def open_add_interest_window(self):
        self.add_interest_window = tk.Toplevel()
        self.add_interest_window.title("Add Interest")
        self.add_interest_window.state("zoomed")
        # Create input fields and labels for updating instructor data
        # You can design and populate this window as needed

        # Example: Create an entry field for updating the instructor's name
        self.interest_field_label = tk.Label(self.add_interest_window, text="Interest Field")
        self.interest_field_label.pack(pady=50)
        self.interest_field_entry = tk.Entry(self.add_interest_window, width=30)
        self.interest_field_entry.pack()

        # Create a button to save the updates
        add_button = tk.Button(self.add_interest_window, text="Add",  bg="#99FFFF", fg="#994C00", padx=10, pady=2, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge", command=self.add_interest)
        add_button.place(relx=0.48, rely=0.3)

    def add_interest(self):
        # Get the values from the input fields in the update window
        field = self.interest_field_entry.get()
        
        # Check if all required fields are filled
        if not (field):
            messagebox.showerror("Error", "Field must be filled.")
            return

        insert_query = "INSERT INTO interest (field) VALUES (%s)"
        data_to_insert = (field,)
        self.db.execute_query(insert_query, data_to_insert)
        self.db.commit()

        select_query = "SELECT opened_lesson_id, name FROM opened_lesson ORDER BY opened_lesson_id DESC LIMIT 1"
        self.db.execute_query(select_query)
        results = self.db.fetch_data()

        number = int(results[0][0])+1

        insert_query = "INSERT INTO opened_lesson (name) VALUES (%s)"
        data_to_insert = (f"Lesson {number}",)
        self.db.execute_query(insert_query, data_to_insert)
        self.db.commit()

        select_query = "SELECT interest_id FROM interest ORDER BY interest_id DESC LIMIT 1"
        self.db.execute_query(select_query)
        interest_id = self.db.fetch_data()

        select_query = "SELECT opened_lesson_id FROM opened_lesson ORDER BY opened_lesson_id DESC LIMIT 1"
        self.db.execute_query(select_query)
        opened_lesson_id = self.db.fetch_data()

        insert_query = "INSERT INTO opened_lesson_interest (opened_lesson_id, interest_id) VALUES (%s, %s)"
        data_to_insert = (opened_lesson_id[0], interest_id[0])
        self.db.execute_query(insert_query, data_to_insert)
        self.db.commit()

        # Close the update window
        self.add_interest_window.destroy()

        # Refresh the Treeview to reflect the changes
        self.get_interest_data(1)

    def update_interest(self):
        selected_item = self.interest_tree.selection()
        if selected_item:
            selected_values = self.interest_tree.item(selected_item, "values")
            if selected_values:
                # Open the update window with the instructor's data for editing
                self.open_interest_update_window(selected_values)

    def open_interest_update_window(self, selected_values):
        self.update_interest_window = tk.Toplevel()
        self.update_interest_window.title("Update Interest Field")
        self.update_interest_window.state("zoomed")
        # Create input fields and labels for updating instructor data
        # You can design and populate this window as needed

        # Example: Create an entry field for updating the instructor's name
        self.interest_label = tk.Label(self.update_interest_window, text="Interest Field")
        self.interest_label.pack(pady=50)
        self.interest_entry = tk.Entry(self.update_interest_window, width=30)
        self.interest_entry.insert(0, selected_values[1])  # Pre-fill with the instructor's current name
        self.interest_entry.pack()

        # Create a button to save the updates
        save_button = tk.Button(self.update_interest_window, text="Save", command=self.save_interest_updates, bg="#99FFFF", fg="#994C00", padx=10, pady=2, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge")
        save_button.place(relx=0.48, rely=0.3)

    def save_interest_updates(self):
        # Get the values from the input fields in the update window
        interest = self.interest_entry.get()
        
        # Check if all required fields are filled
        if not (interest):
            messagebox.showerror("Error", "Field must be filled.")
            return

        # Perform the update in the database
        update_query = "UPDATE interest SET field = %s WHERE interest_id = %s"
        data = (interest, self.selected_interest_id)
        self.db.execute_query(update_query, data)
        self.db.commit()

        # Close the update window
        self.update_interest_window.destroy()

        # Refresh the Treeview to reflect the changes
        self.get_interest_data(1)

    def delete_interest(self):
        if hasattr(self, 'selected_interest_id'):
            select_query = "SELECT opened_lesson_id FROM opened_lesson_interest WHERE interest_id = %s"
            data = (self.selected_interest_id,)
            self.db.execute_query(select_query, data)
            opened_lesson_id = self.db.fetch_data()

            delete_query_1 = "DELETE FROM opened_lesson_interest WHERE interest_id = %s AND opened_lesson_id = %s"
            data = (self.selected_interest_id, opened_lesson_id[0])
            self.db.execute_query(delete_query_1, data)
            self.db.commit()

            delete_query_2 = "DELETE FROM interest WHERE interest_id = %s"
            data = (self.selected_interest_id,)
            self.db.execute_query(delete_query_2, data)
            self.db.commit()

            delete_query_3 = "DELETE FROM opened_lesson WHERE opened_lesson_id = %s"
            data = (opened_lesson_id[0],)
            self.db.execute_query(delete_query_3, data)
            self.db.commit()

            # Remove the deleted item from the Treeview
            selected_item = self.interest_tree.selection()
            if selected_item:
                self.interest_tree.delete(selected_item)

            # Optionally clear the selected_registry_no attribute
            del self.selected_interest_id

class Instructor:
    def __init__(self):
        self.login_window = tk.Tk()
        self.db = DatabaseConnection()

    def login(self):
        
        self.login_window.title("Instructor Log In")
        self.login_window.state("zoomed")

        # Add content and widgets for the admin panel here
        # Create a Label widget to display text
        username_label = tk.Label(self.login_window, text="Username : ", font=("Helvetica", 15, "bold"), fg="brown")
        username_label.place(relx=0.35, rely=0.4)

        password_label = tk.Label(self.login_window, text="Password : ", font=("Helvetica", 15, "bold"), fg="brown")
        password_label.place(relx=0.35, rely=0.5)

        # Create an Entry widget for text input
        self.username_field = tk.Entry(self.login_window, width=20, font=('Arial 15'))
        self.username_field.place(relx=0.45, rely=0.4)

        self.password_field = tk.Entry(self.login_window, width=20, font=('Arial 15'), show="*")
        self.password_field.place(relx=0.45, rely=0.5)

        submit_button = tk.Button(self.login_window, text="Submit", bg="#99FFFF", fg="#994C00", padx=15, pady=4, font=("Helvetica", 12, "bold"), borderwidth=5, relief="ridge", command=self.check_credentials)
        submit_button.place(relx=0.49, rely=0.6)

    def check_credentials(self):
        username = self.username_field.get()
        password = self.password_field.get()
        
        # Query the database to check the credentials
        select_query = "SELECT registry_no, title, name, surname, username,password FROM instructor WHERE username = %s AND password = %s"
        data = (username, password)

        self.db.execute_query(select_query, data)
        self.result = self.db.fetch_data()

        if self.result:
            self.close_login()
        else:
            error_label = tk.Label(self.login_window, text="Invalid username or password!", font=("Helvetica", 15, "bold"), fg="red")
            error_label.place(relx=0.37, rely=0.3)

    def close_login(self):
        self.login_window.destroy()
        self.dashboard()

    def dashboard(self):
        window = tk.Toplevel()
        window.title("Instructor Dashboard")
        window.state("zoomed")

        # Create tabs
        tab_control = ttk.Notebook(window)

        # Tab 1
        self.interest_tab = ttk.Frame(tab_control)
        tab_control.add(self.interest_tab, text="Interest Field")
        interest_label = tk.Label(self.interest_tab, text="Interest Field", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        interest_label.pack()
        #button1 = tk.Button(tab1, text="Open Tab 2", command=lambda: open_tab(tab2))
        #button1.pack()

        self.get_instructor_name_surname(self.interest_tab)

        select_data_query = "SELECT ii.interest_id, i.field FROM instructor_interest AS ii INNER JOIN interest AS i ON ii.interest_id=i.interest_id WHERE ii.registry_no = %s"
        data = (self.result[0][0],)
        self.db.execute_query(select_data_query, data)
        instructor_interests = self.db.fetch_data()

        for (id, interest) in instructor_interests:
            interest_field_label = tk.Label(self.interest_tab, text=interest, padx=80, font=("Helvatica", 9, "bold"), fg="brown")
            interest_field_label.pack(anchor='ne')

        select_data_query = "SELECT interest_id, field FROM interest"
        self.db.execute_query(select_data_query)
        self.interests = self.db.fetch_data()

        # Create and initialize variables to track checkbox states
        self.checkbox_vars = [tk.IntVar() for _ in self.interests]

        # Create checkboxes for each interest
        for i, (interest_id, field) in enumerate(self.interests):
            checkbox = tk.Checkbutton(self.interest_tab, text=field, variable=self.checkbox_vars[i])
            checkbox.pack(anchor="w", padx=600)

        # Button to add selected interests to the instructor_interest table
        add_button = tk.Button(self.interest_tab, text="Add Interests", bg="#99FFFF", fg="#994C00", padx=5, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge", command=self.add_interests)
        add_button.pack(pady=50)

        # Tab 2
        self.score_tab = ttk.Frame(tab_control)
        tab_control.add(self.score_tab, text="Lesson Scoring")
        score_label = tk.Label(self.score_tab, text="Lesson Scoring", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        score_label.pack()
        #button2 = tk.Button(tab2, text="Open Tab 1", command=lambda: open_tab(tab1))
        #button2.pack()

        # Create a Canvas for scrollable area
        self.canvas = tk.Canvas(self.score_tab)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar for the Canvas
        scrollbar = tk.Scrollbar(self.score_tab, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Canvas to work with the Scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Create a Frame inside the Canvas to place your labels
        content_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=content_frame, anchor=tk.NW)

        self.get_instructor_name_surname(self.score_tab)

        select_data_query = "SELECT lesson_id, name FROM lesson"
        self.db.execute_query(select_data_query)
        self.lesson_results = self.db.fetch_data()

        self.lesson_field = []
        for i,lesson_result in enumerate(self.lesson_results):
            frame = tk.Frame(content_frame)
            frame.pack(fill=tk.X)  # Ensure the frame takes up the full width

            lesson_label = tk.Label(frame, text=lesson_result[1])
            lesson_label.pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=3)
            entry.pack(side=tk.LEFT)

            self.lesson_field.append(entry)

        submit_button = tk.Button(content_frame, text="Submit", command=self.insert_coefficient_table)
        submit_button.pack(pady=15)

        # Bind the Canvas to the scrollbar to enable scrolling
        content_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Bind the mouse wheel event to scroll the canvas
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)

        # Tab 3
        self.student_tab = ttk.Frame(tab_control)
        tab_control.add(self.student_tab, text="Student")
        student_label = tk.Label(self.student_tab, text="Student Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        student_label.pack()
        #button2 = tk.Button(tab2, text="Open Tab 1", command=lambda: open_tab(tab1))
        #button2.pack()

        self.get_instructor_name_surname(self.student_tab)

        self.sub_student_tab = ttk.Frame(self.student_tab)
        self.sub_student_tab.pack()

        # Create a variable to store the selected option
        self.score_selected_option = tk.StringVar(self.sub_student_tab)

        # List of options for the dropdown
        score_options = ["Select Point", "1 point and above", "2 point and above", "3 point and above"]

        # Create the OptionMenu widget
        score_option_menu = tk.OptionMenu(self.sub_student_tab, self.score_selected_option, *score_options)
        score_option_menu.pack(side="left",padx=30, pady=30)

        # Set the default selected option (optional)
        self.score_selected_option.set(score_options[0])

        # Bind the function to the selection event
        self.score_selected_option.trace("w", self.on_score_option_selected)

        # Create a variable to store the selected option
        self.sort_selected_option = tk.StringVar(self.sub_student_tab)

        # List of options for the dropdown
        sort_options = ["Select Sort", "Sort by Score"]

        # Create the OptionMenu widget
        sort_option_menu = tk.OptionMenu(self.sub_student_tab, self.sort_selected_option, *sort_options)
        sort_option_menu.pack(side="left",padx=30, pady=30)

        # Set the default selected option (optional)
        self.sort_selected_option.set(score_options[0])

        # Bind the function to the selection event
        self.sort_selected_option.trace("w", self.on_sort_option_selected)

        # Create a Treeview widget (the table)
        self.student_tree = ttk.Treeview(self.student_tab, columns=("Student No", "Name", "Surname", "Status", "Field"), show="headings")
        self.student_tree.heading("#1", text="Student No")
        self.student_tree.heading("#2", text="Name")
        self.student_tree.heading("#3", text="Surname")
        self.student_tree.heading("#4", text="Status")
        self.student_tree.heading("#5", text="Field")
        self.student_tree.pack()
        self.get_same_field_student_data(0) 
        
        # Create the context menu
        self.student_m = tk.Menu(self.student_tree, tearoff=0)
        self.student_m.add_command(label="Inspect", command=self.get_student_lesson_data)
        self.student_m.add_command(label="Make Demand", command=self.make_demand)
        self.student_m.add_separator()

        # Tab 4
        self.message_tab = ttk.Frame(tab_control)
        tab_control.add(self.message_tab, text="Messages")
        message_label = tk.Label(self.message_tab, text="Messages", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        message_label.pack()
        #button1 = tk.Button(tab1, text="Open Tab 2", command=lambda: open_tab(tab2))
        #button1.pack()

        self.get_instructor_name_surname(self.message_tab)

        # Create a Treeview widget (the table)
        self.message_tree = ttk.Treeview(self.message_tab, columns=("Name", "Surname", "Message"), show="headings")
        self.message_tree.heading("#1", text="Name")
        self.message_tree.heading("#2", text="Surname")
        self.message_tree.heading("#3", text="Message")
        self.message_tree.pack()
        self.get_message_data(0)

        message_refresh_button = tk.Button(self.message_tab, text="Refresh", command=lambda: self.get_message_data(1))
        message_refresh_button.place(relx=0.1, rely=0.03)

        # Tab 5
        self.demand_tab = ttk.Frame(tab_control)
        tab_control.add(self.demand_tab, text="Demand")
        student_label = tk.Label(self.demand_tab, text="Demand Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        student_label.pack()
        #button2 = tk.Button(tab2, text="Open Tab 1", command=lambda: open_tab(tab1))
        #button2.pack()

        self.get_instructor_name_surname(self.demand_tab)

        # Create a Treeview widget (the table)
        self.demand_tree = ttk.Treeview(self.demand_tab, columns=("Lesson Name", "Interest Field", "Student No", "Student Name", "Student Surname", "Quota"), show="headings")
        self.demand_tree.heading("#1", text="Lesson Name")
        self.demand_tree.heading("#2", text="Interest Field")
        self.demand_tree.heading("#3", text="Student No")
        self.demand_tree.heading("#4", text="Student Name")
        self.demand_tree.heading("#5", text="Student Surname")
        self.demand_tree.heading("#6", text="Quota")
        self.demand_tree.pack()
        self.get_demand_data(0)

        # Create the context menu
        self.demand_m = tk.Menu(self.demand_tree, tearoff=0)
        self.demand_m.add_command(label="Inspect", command=self.get_student_lesson_data)
        self.demand_m.add_command(label="Approve", command=self.approve_deal)
        self.demand_m.add_separator()

        demand_refresh_button = tk.Button(self.demand_tab, text="Refresh", command=lambda: self.get_demand_data(1))
        demand_refresh_button.place(relx=0.1, rely=0.03)
        
        # Set the default tab to open
        tab_control.select(self.interest_tab)

        tab_control.pack(expand=1, fill="both")
        
        # Start the tkinter main loop
        window.mainloop()
        
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_interests(self):
        selected_interests = [self.interests[i][0] for i, var in enumerate(self.checkbox_vars) if var.get()]
        if selected_interests:
            registry_no = self.result[0][0]
            for interest_id in selected_interests:
                self.db.cursor.execute("INSERT INTO instructor_interest (registry_no, interest_id) VALUES (%s, %s)", (registry_no, interest_id))
                select_data_query = "SELECT opened_lesson_id FROM opened_lesson_interest WHERE interest_id=%s"
                data = (interest_id,)
                self.db.execute_query(select_data_query, data)
                opened_lesson_id_results = self.db.fetch_data()
            self.db.commit()
            for opened_lesson_id_result in opened_lesson_id_results:
                self.db.cursor.execute("INSERT INTO instructor_opened_lesson (registry_no, opened_lesson_id) VALUES (%s, %s)", (registry_no, opened_lesson_id_result))
            self.db.commit()
            self.make_confirmation_window("Interest Field Added")

    def get_message_data(self, refresh):
        if(refresh==1):
            # Clear existing data in the Treeview
            for item in self.message_tree.get_children():
                self.message_tree.delete(item)

        select_data_query = "SELECT s.name, s.surname, m.content FROM message AS m INNER JOIN student AS s on m.student_no=s.student_no"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.message_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        #self.message_tree.bind("<Button-3>", self.do_popup_interest)

    def get_demand_data(self, refresh):
        if(refresh==1):
            # Clear existing data in the Treeview
            for item in self.demand_tree.get_children():
                self.demand_tree.delete(item)

        select_data_query = "SELECT ol.name, inte.field, s.student_no, s.name, s.surname, i.quota FROM deal AS d INNER JOIN student AS s ON d.student_no=s.student_no INNER JOIN instructor AS i ON d.registry_no=i.registry_no INNER JOIN instructor_opened_lesson AS iol ON d.registry_no=iol.registry_no AND d.opened_lesson_id=iol.opened_lesson_id INNER JOIN opened_lesson AS ol ON iol.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli ON ol.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte ON oli.interest_id=inte.interest_id WHERE d.deal_status=0 AND d.registry_no=%s"
        data = (self.result[0][0],)
        self.db.execute_query(select_data_query, data)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.demand_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        global duration
        if duration != 0:
            self.demand_tree.bind("<Button-3>", self.do_popup_demand)
        elif duration == 0:
            self.demand_m = None
            self.demand_tree.unbind("<Button-3>")

    def get_same_field_student_data(self, refresh):
        if(refresh==1):
            # Clear existing data in the Treeview
            for item in self.student_tree.get_children():
                self.student_tree.delete(item)

        select_data_query = "SELECT interest_id FROM instructor_interest WHERE registry_no = %s"
        data = (self.result[0][0],)
        self.db.execute_query(select_data_query, data)
        interest_ids = self.db.fetch_data()

        for interest_id in interest_ids:
            select_data_query = "SELECT s.student_no, s.name, s.surname, d.deal_status, inte.field FROM student AS s INNER JOIN student_interest AS si ON s.student_no=si.student_no INNER JOIN interest AS inte ON si.interest_id=inte.interest_id LEFT JOIN deal AS d ON si.student_no=d.student_no WHERE si.interest_id=%s"
            data = (interest_id[0],)
            self.db.execute_query(select_data_query, data)
            results = self.db.fetch_data()
            # Insert data into the table
            for item in results:
                item = list(item)
                if item[3]==1:
                    item[3]="deal"
                else:
                    item[3]="non-deal"
                item = tuple(item)
                self.student_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        self.student_tree.bind("<Button-3>", self.do_popup_student)

    def do_popup_demand(self, event):
        item = self.demand_tree.item(self.demand_tree.selection())  # Get the selected item
        if item:
            self.selected_student_no = item['values'][2]  # Extract the 'registry_no' value
            self.demand_m.tk_popup(event.x_root, event.y_root)

    def do_popup_student(self, event):
        item = self.student_tree.item(self.student_tree.selection())  # Get the selected item
        if item:
            self.selected_student_no = item['values'][0]  # Extract the 'registry_no' value
            self.selected_field = item['values'][4]
            self.student_m.tk_popup(event.x_root, event.y_root)

    def get_student_lesson_data(self):
        student_lesson_window = tk.Tk()
        student_lesson_window.title("Student Taken Lessons")
        student_lesson_window.state("zoomed")

        # Create a Treeview widget (the table)
        self.lesson_tree = ttk.Treeview(student_lesson_window, columns=("Lesson Name", "AKTS", "Mark"), show="headings")
        self.lesson_tree.column('#1', width=300)
        self.lesson_tree.column('#2', width=150)
        self.lesson_tree.column('#3', width=150)
        self.lesson_tree.heading("#1", text="Lesson Name")
        self.lesson_tree.heading("#2", text="AKTS")
        self.lesson_tree.heading("#3", text="Mark")
        self.lesson_tree.pack(pady=100)

        select_data_query = "SELECT l.name, l.AKTS, sl.mark FROM student_lesson AS sl INNER JOIN lesson AS l on sl.lesson_id=l.lesson_id WHERE sl.student_no = %s"
        data_to_insert = (self.selected_student_no,)
        self.db.execute_query(select_data_query, data_to_insert)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.lesson_tree.insert("", "end", values=item)

        select_data_query = "SELECT name, surname FROM student WHERE student_no = %s"
        data_to_insert = (self.selected_student_no,)
        self.db.execute_query(select_data_query, data_to_insert)
        name_results = self.db.fetch_data()
        name, surname = name_results[0]

        name_surname_label = tk.Label(student_lesson_window, text=f"{name} {surname}", font=("Helvetica", 12, "bold"), fg="brown")
        name_surname_label.place(relx=0.85, rely=0.13)
        gpa = self.calculate_student_GPA()
        gpa_label = tk.Label(student_lesson_window, text=f"GPA : {gpa}", font=("Helvetica", 12, "bold"), fg="brown")
        gpa_label.place(relx=0.85, rely=0.18)

        score = self.student_score_calculation(0)

        score_label = tk.Label(student_lesson_window, text=f"SCORE : {score}", font=("Helvetica", 25, "bold"), fg="brown", pady=100)
        score_label.pack()

        # Bind the right-click context menu to the Treeview
        #self.lesson_tree.bind("<Button-3>", self.do_popup_instructor)

    def calculate_student_GPA(self):
        select_data_query = "SELECT sl.mark, l.AKTS FROM student_lesson AS sl INNER JOIN lesson AS l on sl.lesson_id=l.lesson_id WHERE sl.student_no = %s"
        data = (self.selected_student_no,)
        self.db.execute_query(select_data_query, data)
        results = self.db.fetch_data()

        total_point = 0
        divider = 0
        for result in results:
            mark, akts = result
            if mark == "AA":
                point = 4
            elif mark == "BA":
                point = 3.5
            elif mark == "BB":
                point = 3
            elif mark == "CB":
                point = 2.5
            elif mark == "CC":
                point = 2
            elif mark == "DC":
                point = 1.5

            total_point += point*akts
            divider += akts

        if divider != 0:
            gpa = total_point / divider
        else:
            gpa = "enter coefficient for score calculation"

        formatted_gpa = f"{gpa:.2f}"
        return formatted_gpa

    def approve_deal(self):
        update_query = "UPDATE deal SET deal_status = %s WHERE student_no = %s"
        data = (1, self.selected_student_no)

        update_query_2 = "UPDATE instructor SET quota =quota-1 WHERE registry_no = %s"
        data_2 = (self.result[0][0],)

        try:
            self.db.execute_query(update_query, data)
            self.db.commit()

            self.db.execute_query(update_query_2, data_2)
            self.db.commit()

            self.make_confirmation_window("Deal Approved")
        except Exception as e:
            print(e)

    def make_confirmation_window(self, str):
        confirmation_window = tk.Tk()
        confirmation_window.title("Confirmation Window")
        confirmation_window.geometry("300x150+500+250")

        confirmation_label = tk.Label(confirmation_window, text=str, font=("Helvetica", 12, "bold"), fg="green")
        confirmation_label.place(relx=0.1, rely=0.4)
        confirmation_window.after(1000, confirmation_window.destroy)

    def get_instructor_name_surname(self, tab):
        name_surname_label = tk.Label(tab, text=f"{self.result[0][1]} {self.result[0][2]} {self.result[0][3]}", font=("Helvetica", 12, "bold"), fg="brown")
        name_surname_label.place(relx=0.85, rely=0.03)

    def insert_coefficient_table(self):
        
        for i, lesson_result in enumerate(self.lesson_results):
            number = self.lesson_field[i].get()
            if number == "":
                number = 1
            else:
                number = int(number)

            insert_data_query = """INSERT INTO coefficient (registry_no, lesson_id, number) VALUES (%s, %s, %s)"""
            data_to_insert = (self.result[0][0], lesson_result[0] , number)
            self.db.execute_query(insert_data_query, data_to_insert)
            self.db.commit()
        
        self.make_confirmation_window("Successful")

    def student_score_calculation(self, number):
        select_data_query = "SELECT sl.lesson_id, sl.mark, c.number FROM student_lesson AS sl INNER JOIN coefficient AS c ON sl.lesson_id=c.lesson_id WHERE sl.student_no = %s AND c.registry_no = %s"
        if number == 0:
            data_to_insert = (self.selected_student_no, self.result[0][0])
        else:
            data_to_insert = (self.item_student_no, self.result[0][0])

        self.db.execute_query(select_data_query, data_to_insert)
        results = self.db.fetch_data()

        total_point = 0
        divider = 0
        for result in results:
            if result[1] == "AA":
                point = 4
            elif result[1] == "BA":
                point = 3.5
            elif result[1] == "BB":
                point = 3
            elif result[1] == "CB":
                point = 2.5
            elif result[1] == "CC":
                point = 2
            elif result[1] == "DC":
                point = 1.5

            total_point += point*result[2]
            divider += result[2]

        if divider != 0:
            score = total_point / divider
        else:
            score = "enter coefficient for score calculation"

        formatted_score = f"{score:.2f}"
        return formatted_score

    def refresh_student_for_score_data(self):
        # Clear existing data in the Treeview
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

    def on_score_option_selected(self, *args):
        self.refresh_student_for_score_data()
        self.selected_score = self.score_selected_option.get()
        self.selected_sort = ""
        self.get_same_field_student_data_with_score()

        # Bind the right-click context menu to the Treeview
        #self.lesson_tree.bind("<Button-3>", self.do_popup_instructor)

    def on_sort_option_selected(self, *args):
        self.refresh_student_for_score_data()
        self.selected_sort = self.sort_selected_option.get()
        self.get_same_field_student_data_with_score()

        # Bind the right-click context menu to the Treeview
        #self.lesson_tree.bind("<Button-3>", self.do_popup_instructor)

    def get_same_field_student_data_with_score(self):
        select_data_query = "SELECT interest_id FROM instructor_interest WHERE registry_no = %s"
        data = (self.result[0][0],)
        self.db.execute_query(select_data_query, data)
        interest_ids = self.db.fetch_data()

        for interest_id in interest_ids:
            select_data_query = "SELECT s.student_no, s.name, s.surname, d.deal_status, inte.field FROM student AS s INNER JOIN student_interest AS si ON s.student_no=si.student_no INNER JOIN interest AS inte ON si.interest_id=inte.interest_id LEFT JOIN deal AS d ON si.student_no=d.student_no WHERE si.interest_id=%s"
            data = (interest_id,)
            self.db.execute_query(select_data_query, data)
            self.student_results = self.db.fetch_data()

            student_score_dict = {}
            for item in self.student_results:
                self.item_student_no = item[0]
                score = self.student_score_calculation(1)
                student_score_dict[self.item_student_no] = score

            # Sort the dictionary by score in descending order
            sorted_scores = sorted(student_score_dict.items(), key=lambda item: item[1], reverse=True)

            # Create a new dictionary from the sorted list of tuples
            sorted_student_scores = dict(sorted_scores)
            key_list = list(sorted_student_scores.keys())

            # Insert data into the table
            for i,item in enumerate(self.student_results):
                item = list(item)
                if item[3]==1:
                    item[3]="deal"
                else:
                    item[3]="non-deal"
                item = tuple(item)

                if self.selected_sort == "Sort by Score":
                    select_data_query = "SELECT s.student_no, s.name, s.surname, d.deal_status, inte.field FROM student AS s INNER JOIN student_interest AS si ON s.student_no=si.student_no INNER JOIN interest AS inte ON si.interest_id=inte.interest_id LEFT JOIN deal AS d ON si.student_no=d.student_no WHERE si.interest_id=%s AND s.student_no = %s"
                    data = (interest_id, key_list[i])
                    self.db.execute_query(select_data_query, data)
                    student_result = self.db.fetch_data()

                    self.student_tree.insert("", "end", values=student_result[0])
                else:    
                    if self.selected_score == "1 point and above" and score>=1:
                        self.student_tree.insert("", "end", values=item)
                    elif self.selected_score == "2 point and above" and score>=2:
                        self.student_tree.insert("", "end", values=item)
                    elif self.selected_score == "3 point and above" and score>=3:
                        self.student_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        self.student_tree.bind("<Button-3>", self.do_popup_student)

    def make_demand(self):
        select_query = "SELECT oli.opened_lesson_id FROM interest AS i INNER JOIN opened_lesson_interest AS oli ON i.interest_id=oli.interest_id WHERE i.field=%s"
        data = (self.selected_field,)
        self.db.execute_query(select_query, data)
        results = self.db.fetch_data()
        
        insert_query = "INSERT INTO deal (student_no, registry_no, opened_lesson_id, deal_status) VALUES (%s, %s, %s, %s)"
        data_to_insert = (self.selected_student_no, self.result[0][0], results[0][0], 0)
        self.db.execute_query(insert_query, data_to_insert)
        self.db.commit()

        self.make_confirmation_window("Request Send Successfully")
        #self.refresh_demand_data()

class Student:
    def __init__(self):
        self.login_window = tk.Tk()

    def login(self):
        
        self.login_window.title("Student Log In")
        self.login_window.state("zoomed")

        # Add content and widgets for the admin panel here
        # Create a Label widget to display text
        username_label = tk.Label(self.login_window, text="Username : ", font=("Helvetica", 15, "bold"), fg="brown")
        username_label.place(relx=0.35, rely=0.4)

        password_label = tk.Label(self.login_window, text="Password : ", font=("Helvetica", 15, "bold"), fg="brown")
        password_label.place(relx=0.35, rely=0.5)

        # Create an Entry widget for text input
        self.username_field = tk.Entry(self.login_window, width=20, font=('Arial 15'))
        self.username_field.place(relx=0.45, rely=0.4)

        self.password_field = tk.Entry(self.login_window, width=20, font=('Arial 15'), show="*")
        self.password_field.place(relx=0.45, rely=0.5)

        submit_button = tk.Button(self.login_window, text="Submit", bg="#99FFFF", fg="#994C00", padx=15, pady=4, font=("Helvetica", 12, "bold"), borderwidth=5, relief="ridge", command=self.check_credentials)
        submit_button.place(relx=0.49, rely=0.6)

    def check_credentials(self):
        username = self.username_field.get()
        password = self.password_field.get()
       
        self.db = DatabaseConnection()
        # Query the database to check the credentials
        select_query = "SELECT student_no, name, surname, username,password FROM student WHERE username = %s AND password = %s"
        data = (username, password)

        self.db.execute_query(select_query, data)
        self.result = self.db.fetch_data()

        if self.result:
            Student.close_login(self)
        else:
            error_label = tk.Label(self.login_window, text="Invalid username or password!", font=("Helvetica", 15, "bold"), fg="red")
            error_label.place(relx=0.37, rely=0.3)

    def close_login(self):
        self.login_window.destroy()
        Student.dashboard(self)

    def dashboard(self):
        window = tk.Tk()
        window.title("Student Dashboard")
        window.state("zoomed")

        # Create a menu bar
        menu = tk.Menu(window)
        window.config(menu=menu)

        # Create a File menu
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Transcript", menu=file_menu)
        file_menu.add_command(label="Upload", command=self.upload_pdf_file)
        #file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=window.quit)

        # Create tabs
        tab_control = ttk.Notebook(window)

        # Tab 1
        self.lesson_taken_tab = ttk.Frame(tab_control)
        tab_control.add(self.lesson_taken_tab, text="Lessons Taken")
        lesson_taken_label = tk.Label(self.lesson_taken_tab, text="Lessons Taken and Grades", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        lesson_taken_label.pack()
        #button1 = tk.Button(tab1, text="Open Tab 2", command=lambda: open_tab(tab2))
        #button1.pack()

        self.get_student_name_surname(self.lesson_taken_tab)

        # Create a Treeview widget (the table)
        self.lesson_taken_tree = ttk.Treeview(self.lesson_taken_tab, columns=("Lesson Name", "AKTS", "Mark"), show="headings")
        self.lesson_taken_tree.column('#1', width=300)
        self.lesson_taken_tree.column('#2', width=150)
        self.lesson_taken_tree.column('#3', width=150)
        self.lesson_taken_tree.heading("#1", text="Lesson Name")
        self.lesson_taken_tree.heading("#2", text="AKTS")
        self.lesson_taken_tree.heading("#3", text="Mark")
        self.lesson_taken_tree.pack()
        self.get_lesson_taken_data()

        gpa = self.calculate_GPA()
        gpa_label = tk.Label(self.lesson_taken_tab, text=f"GPA : {gpa}", font=("Helvetica", 12, "bold"), fg="brown")
        gpa_label.place(relx=0.85, rely=0.1)

        # Tab 2
        self.interest_tab = ttk.Frame(tab_control)
        tab_control.add(self.interest_tab, text="Interest Field")
        student_label = tk.Label(self.interest_tab, text="Interest Field Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        student_label.pack()
        #button2 = tk.Button(tab2, text="Open Tab 1", command=lambda: open_tab(tab1))
        #button2.pack()

        self.get_student_name_surname(self.interest_tab)

        interest_refresh_button = tk.Button(self.interest_tab, text="Refresh", command=lambda: self.get_interest_data(1))
        interest_refresh_button.place(relx=0.1, rely=0.03)

        self.sub_interest_tab = ttk.Frame(self.interest_tab)
        self.sub_interest_tab.pack()

        #def on_option_selected(*args):
            #selected = selected_option.get()

        # Create a variable to store the selected option
        self.lesson_selected_option = tk.StringVar(self.sub_interest_tab)

        # List of options for the dropdown
        lesson_options = ["Select Lesson"]

        select_data_query = "SELECT name FROM opened_lesson"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()
        for result in results:
            lesson_name = result[0]
            lesson_options.append(lesson_name)

        # Create the OptionMenu widget
        lesson_option_menu = tk.OptionMenu(self.sub_interest_tab, self.lesson_selected_option, *lesson_options)
        lesson_option_menu.pack(side="left", padx=30, pady=30)

        # Set the default selected option (optional)
        self.lesson_selected_option.set(lesson_options[0])

        # Bind the function to the selection event
        self.lesson_selected_option.trace("w", self.on_lesson_option_selected)


        # Create a variable to store the selected option
        self.interest_selected_option = tk.StringVar(self.sub_interest_tab)

        # List of options for the dropdown
        interest_options = ["Select Interest"]

        select_data_query = "SELECT field FROM interest"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()
        for result in results:
            interest_name = result[0]
            interest_options.append(interest_name)

        # Create the OptionMenu widget
        interest_option_menu = tk.OptionMenu(self.sub_interest_tab, self.interest_selected_option, *interest_options)
        interest_option_menu.pack(side="left",padx=30, pady=30)

        # Set the default selected option (optional)
        self.interest_selected_option.set(interest_options[0])

        # Bind the function to the selection event
        self.interest_selected_option.trace("w", self.on_interest_option_selected)

         # Create a Treeview widget (the table)
        self.interest_tree = ttk.Treeview(self.interest_tab, columns=("Lesson Name", "Interest Field", "Instructor No", "Instructor Title", "Instructor Name", "Instructor Surname", "Quota"), show="headings")
        self.interest_tree.column('#1', width=150)
        self.interest_tree.column('#3', width=150)
        self.interest_tree.column('#7', width=75)
        self.interest_tree.heading("#1", text="Lesson Name")
        self.interest_tree.heading("#2", text="Interest Field")
        self.interest_tree.heading("#3", text="Instructor No")
        self.interest_tree.heading("#4", text="Instructor Title")
        self.interest_tree.heading("#5", text="Instructor Name")
        self.interest_tree.heading("#6", text="Instructor Surname")
        self.interest_tree.heading("#7", text="Quota")
        self.interest_tree.pack()
        self.get_interest_data(0)

        # Create the context menu
        self.interest_m = tk.Menu(self.interest_tree, tearoff=0)
        self.interest_m.add_command(label="Demand", command=self.make_demand)
        self.interest_m.add_command(label="Demand with Message", command=self.write_message)
        self.interest_m.add_separator()

        # Tab 3
        self.demand_tab = ttk.Frame(tab_control)
        tab_control.add(self.demand_tab, text="Demand")
        student_label = tk.Label(self.demand_tab, text="Demand Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        student_label.pack()
        #button2 = tk.Button(tab2, text="Open Tab 1", command=lambda: open_tab(tab1))
        #button2.pack()

        self.get_student_name_surname(self.demand_tab)

        # Create a Treeview widget (the table)
        self.demand_tree = ttk.Treeview(self.demand_tab, columns=("Lesson Name", "Interest Field", "Instructor Title", "Instructor Name", "Instructor Surname", "Quota"), show="headings")
        self.demand_tree.heading("#1", text="Lesson Name")
        self.demand_tree.heading("#2", text="Interest Field")
        self.demand_tree.heading("#3", text="Instructor Title")
        self.demand_tree.heading("#4", text="Instructor Name")
        self.demand_tree.heading("#5", text="Instructor Surname")
        self.demand_tree.heading("#6", text="Quota")
        self.demand_tree.pack()
        self.get_demand_data()

        # Create the context menu
        self.demand_m = tk.Menu(self.demand_tree, tearoff=0)
        self.demand_m.add_command(label="Withdraw", command=self.withdraw_demand)
        self.demand_m.add_separator()

        # Tab 4
        self.lesson_tab = ttk.Frame(tab_control)
        tab_control.add(self.lesson_tab, text="Lesson")
        student_label = tk.Label(self.lesson_tab, text="Lesson Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        student_label.pack()
        #button2 = tk.Button(tab2, text="Open Tab 1", command=lambda: open_tab(tab1))
        #button2.pack()

        self.get_student_name_surname(self.lesson_tab)

        # Create a Treeview widget (the table)
        self.lesson_tree = ttk.Treeview(self.lesson_tab, columns=("Lesson Name", "Interest Field", "Instructor Title", "Instructor Name", "Instructor Surname", "Quota"), show="headings")
        self.lesson_tree.heading("#1", text="Lesson Name")
        self.lesson_tree.heading("#2", text="Interest Field")
        self.lesson_tree.heading("#3", text="Instructor Title")
        self.lesson_tree.heading("#4", text="Instructor Name")
        self.lesson_tree.heading("#5", text="Instructor Surname")
        self.lesson_tree.heading("#6", text="Quota")
        self.lesson_tree.pack()
        self.get_lesson_data(0)

        lesson_refresh_button = tk.Button(self.lesson_tab, text="Refresh", command=lambda: self.get_lesson_data(1))
        lesson_refresh_button.place(relx=0.1, rely=0.03)

        # Create the context menu
        #self.lesson_m = tk.Menu(self.lesson_tree, tearoff=0)
        #self.lesson_m.add_command(label="Withdraw", command=self.withdraw_demand)
        #self.lesson_m.add_separator()
        
        # Set the default tab to open
        tab_control.select(self.lesson_taken_tab)

        tab_control.pack(expand=1, fill="both")
        
        # Start the tkinter main loop
        window.mainloop()

    def get_student_name_surname(self, tab):
        name_surname_label = tk.Label(tab, text=f"{self.result[0][1]} {self.result[0][2]}", font=("Helvetica", 12, "bold"), fg="brown")
        name_surname_label.place(relx=0.85, rely=0.03)

    def upload_pdf_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")],
            title="Select a PDF file"
        )

        if file_path:
            # Destination directory where you want to copy the file
            destination_directory = r"D:\projects 2\first term\first project\Project Course Registration System\upload"
            destination_file_path = f"{destination_directory}/{file_path.split('/')[-1]}"
            copyfile(file_path, destination_file_path)
            self.pdf_reader = PdfReader(open(file_path, "rb"))
            self.num_pages = len(self.pdf_reader.pages)

            doc = fitz.open(file_path)
            text = ""

            for page in doc:
                extracted_text = page.get_text()
                text += extracted_text

            lesson_names = []
            marks = []

            # Split the page text by line breaks and filter out empty lines
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            # Check for lines that match your lesson name pattern (e.g., AIT109, AIT110, etc.)
            for i in range(len(lines) - 1):
                if lines[i].startswith("AIT") or lines[i].startswith("IKT") or lines[i].startswith("JFZ") or lines[i].startswith("TDB") or lines[i].startswith("YDB") or lines[i].startswith("BLM") or lines[i].startswith("FEF") or lines[i].startswith("TDB") or lines[i].startswith("MAT") or lines[i].startswith("MUH"):
                    lesson_names.append(lines[i + 1])
                
                if lines[i].startswith("AA") or lines[i].startswith("BA") or lines[i].startswith("BB") or lines[i].startswith("CB") or lines[i].startswith("CC") or lines[i].startswith("DC"):
                    marks.append(lines[i])

            for i in range(0, 32):
                
                select_data_query = "SELECT lesson_id FROM lesson WHERE name = %s"
                data = (lesson_names[i], )
                self.db.execute_query(select_data_query, data)
                results = self.db.fetch_data()

                insert_data_query = """INSERT INTO student_lesson (student_no, lesson_id, mark) VALUES (%s, %s, %s)"""
                data_to_insert = (self.result[0][0], results[0], marks[i])
                self.db.execute_query(insert_data_query, data_to_insert)
                self.db.commit()
            
            insert_data_query = """INSERT INTO pdf (student_no, file_name, file_data) VALUES (%s, %s, %s)"""
            data_to_insert = (self.result[0][0], "transcript.pdf", text)
            self.db.execute_query(insert_data_query, data_to_insert)
            self.db.commit()

            self.get_lesson_taken_data()

    def get_lesson_taken_data(self):
        select_data_query = "SELECT l.name, l.AKTS, sl.mark FROM student_lesson AS sl INNER JOIN lesson AS l on sl.lesson_id=l.lesson_id WHERE sl.student_no = %s"
        data_to_insert = (self.result[0][0],)
        self.db.execute_query(select_data_query, data_to_insert)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.lesson_taken_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        #self.lesson_tree.bind("<Button-3>", self.do_popup_instructor)

    def get_interest_data(self, refresh):
        if(refresh==1):
            # Clear existing data in the Treeview
            for item in self.interest_tree.get_children():
                self.interest_tree.delete(item)

        select_data_query = "SELECT ol.name, inte.field, i.registry_no, i.title, i.name, i.surname, i.quota FROM instructor AS i INNER JOIN instructor_opened_lesson AS iol on i.registry_no=iol.registry_no INNER JOIN opened_lesson as ol on iol.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli ON ol.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte on oli.interest_id=inte.interest_id"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.interest_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        global duration
        if duration != 0:
            self.interest_tree.bind("<Button-3>", self.do_popup_interest)
        elif duration == 0:
            self.interest_m = None
            self.interest_tree.unbind("<Button-3>")

    def get_demand_data(self):
        select_data_query = "SELECT ol.name, inte.field, i.title, i.name, i.surname, i.quota, d.deal_id FROM deal AS d INNER JOIN instructor AS i on d.registry_no=i.registry_no INNER JOIN opened_lesson AS ol on d.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli on ol.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte on oli.interest_id=inte.interest_id WHERE d.student_no = %s"
        data = (self.result[0][0],)
        self.db.execute_query(select_data_query, data)
        self.results = self.db.fetch_data()

        # Insert data into the table
        for item in self.results:
            self.demand_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        self.demand_tree.bind("<Button-3>", self.do_popup_demand)
    
    def get_lesson_data(self, refresh):
        if(refresh==1):
            # Clear existing data in the Treeview
            for item in self.lesson_tree.get_children():
                self.lesson_tree.delete(item)
        select_data_query = "SELECT ol.name, inte.field, i.title, i.name, i.surname, i.quota, d.deal_id FROM deal AS d INNER JOIN instructor AS i on d.registry_no=i.registry_no INNER JOIN opened_lesson AS ol on d.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli on ol.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte on oli.interest_id=inte.interest_id WHERE d.student_no = %s AND d.deal_status=1"
        data = (self.result[0][0],)
        self.db.execute_query(select_data_query, data)
        self.results = self.db.fetch_data()

        # Insert data into the table
        for item in self.results:
            self.lesson_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        #self.demand_tree.bind("<Button-3>", self.do_popup_demand)

    def refresh_interest_data(self):
        # Clear existing data in the Treeview
        for item in self.interest_tree.get_children():
            self.interest_tree.delete(item)

    def refresh_demand_data(self):
        # Clear existing data in the Treeview
        for item in self.demand_tree.get_children():
            self.demand_tree.delete(item)

        # Fetch and insert the updated data
        self.get_demand_data()

    def on_lesson_option_selected(self, *args):
        self.refresh_interest_data()
        selected_lesson = self.lesson_selected_option.get()
        select_data_query = "SELECT ol.name, inte.field, i.registry_no, i.title, i.name, i.surname, i.quota FROM instructor AS i INNER JOIN instructor_opened_lesson AS iol on i.registry_no=iol.registry_no INNER JOIN opened_lesson as ol on iol.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli ON ol.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte on oli.interest_id=inte.interest_id  WHERE ol.name = %s"
        data_to_insert = (selected_lesson,)
        self.db.execute_query(select_data_query, data_to_insert)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.interest_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        #self.lesson_tree.bind("<Button-3>", self.do_popup_lesson)

    def on_interest_option_selected(self, *args):
        self.refresh_interest_data()
        selected_interest = self.interest_selected_option.get()
        select_data_query = "SELECT ol.name, inte.field, i.registry_no, i.title, i.name, i.surname, i.quota FROM instructor AS i INNER JOIN instructor_opened_lesson AS iol on i.registry_no=iol.registry_no INNER JOIN opened_lesson as ol on iol.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli ON ol.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte on oli.interest_id=inte.interest_id  WHERE inte.field = %s"
        data_to_insert = (selected_interest,)
        self.db.execute_query(select_data_query, data_to_insert)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.interest_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        #self.lesson_tree.bind("<Button-3>", self.do_popup_instructor)

    def do_popup_interest(self, event):
        item = self.interest_tree.item(self.interest_tree.selection())  # Get the selected item
        if item:
            self.selected_opened_lesson_name = item['values'][0]  # Extract the 'registry_no' value
            self.selected_registry_no = item['values'][2] 
            self.interest_m.tk_popup(event.x_root, event.y_root)
            
    def do_popup_demand(self, event):
        item = self.demand_tree.item(self.demand_tree.selection())  # Get the selected item
        if item:
            self.selected_deal_id = item['values'][6]  # Extract the 'registry_no' value
            self.demand_m.tk_popup(event.x_root, event.y_root)

    def write_message(self):
        global character_number
        self.message_window = tk.Tk()
        self.message_window.title("Message Window")
        self.message_window.geometry("600x400+300+200")

        character_limit_label = tk.Label(self.message_window, text=f"Character Limit : {character_number}", font=("Helvetica", 12, "bold"), fg="green")
        character_limit_label.place(relx=0.1, rely=0.2)

        # Create a text entry field
        self.message_entry = tk.Text(self.message_window, width=60, height=10)
        self.message_entry.place(relx=0.1, rely=0.3)

        def enforce_character_limit(event):
            # Get the current text in the text widget
            current_text = self.message_entry.get("1.0", "end-1c")
            character_limit = int(character_number)-1  # You can set your desired character limit

            # Check if the character limit is reached
            if len(current_text) > character_limit:
                # Prevent further input by disabling the widget
                self.message_entry.config(state=tk.DISABLED)

        # Bind the enforce_character_limit function to the text widget
        self.message_entry.bind("<Key>", enforce_character_limit)

        send_demand_message_button = tk.Button(self.message_window, text="Send Demand", bg="#99FFFF", fg="#994C00", padx=5, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge", command=self.make_demand_with_message)
        send_demand_message_button.place(relx=0.4, rely=0.8)

    def make_demand_with_message(self):
        select_query = "SELECT i.registry_no, iol.opened_lesson_id FROM instructor AS i INNER JOIN instructor_opened_lesson AS iol on i.registry_no=iol.registry_no INNER JOIN opened_lesson AS ol on iol.opened_lesson_id=ol.opened_lesson_id WHERE ol.name = %s"
        data = (self.selected_opened_lesson_name,)
        self.db.execute_query(select_query, data)
        results = self.db.fetch_data()
        
        insert_query = "INSERT INTO deal (student_no, registry_no, opened_lesson_id, deal_status) VALUES (%s, %s, %s, %s)"
        data_to_insert = (self.result[0][0], results[0][0], results[0][1], 0)
        self.db.execute_query(insert_query, data_to_insert)
        self.db.commit()

        text = self.message_entry.get("1.0", "end-1c")
        insert_query = "INSERT INTO message (student_no, registry_no, content) VALUES (%s, %s, %s)"
        data_to_insert = (self.result[0][0], results[0][0], text)
        self.db.execute_query(insert_query, data_to_insert)
        self.db.commit()

        confirmation_label = tk.Label(self.message_window, text="Request Send Successfully", font=("Helvetica", 12, "bold"), fg="green")
        confirmation_label.place(relx=0.1, rely=0.1)
        self.message_window.after(1000, self.message_window.destroy)

        self.refresh_demand_data()
        
    def make_demand(self):
        select_query = "SELECT i.registry_no, iol.opened_lesson_id FROM instructor AS i INNER JOIN instructor_opened_lesson AS iol on i.registry_no=iol.registry_no INNER JOIN opened_lesson AS ol on iol.opened_lesson_id=ol.opened_lesson_id WHERE ol.name = %s AND i.registry_no=%s"
        data = (self.selected_opened_lesson_name, self.selected_registry_no)
        self.db.execute_query(select_query, data)
        results = self.db.fetch_data()
        
        insert_query = "INSERT INTO deal (student_no, registry_no, opened_lesson_id, deal_status) VALUES (%s, %s, %s, %s)"
        data_to_insert = (self.result[0][0], results[0][0], results[0][1], 0)
        self.db.execute_query(insert_query, data_to_insert)
        self.db.commit()

        self.make_confirmation_window("Request Send Successfully")
        self.refresh_demand_data()
        
    def withdraw_demand(self):
        if hasattr(self, "selected_deal_id"):
            delete_query_1 = "DELETE FROM deal WHERE deal_id = %s"
            data = (self.selected_deal_id,)
            self.db.execute_query(delete_query_1, data)
            self.db.commit()

            # Remove the deleted item from the Treeview
            selected_item = self.demand_tree.selection()
            if selected_item:
                self.demand_tree.delete(selected_item)

    def make_confirmation_window(self, str):
        confirmation_window = tk.Tk()
        confirmation_window.title("Confirmation Window")
        confirmation_window.geometry("300x150+500+250")

        confirmation_label = tk.Label(confirmation_window, text=str, font=("Helvetica", 12, "bold"), fg="green")
        confirmation_label.place(relx=0.1, rely=0.4)
        confirmation_window.after(1000, confirmation_window.destroy)

    def calculate_GPA(self):
        select_data_query = "SELECT sl.mark, l.AKTS FROM student_lesson AS sl INNER JOIN lesson AS l on sl.lesson_id=l.lesson_id WHERE sl.student_no = %s"
        data = (self.result[0][0],)
        self.db.execute_query(select_data_query, data)
        results = self.db.fetch_data()

        total_point = 0
        divider = 0
        for result in results:
            mark, akts = result
            if mark == "AA":
                point = 4
            elif mark == "BA":
                point = 3.5
            elif mark == "BB":
                point = 3
            elif mark == "CB":
                point = 2.5
            elif mark == "CC":
                point = 2
            elif mark == "DC":
                point = 1.5

            total_point += point*akts
            divider += akts

        if divider != 0:
            gpa = total_point / divider
        else:
            gpa = "enter coefficient for score calculation"

        formatted_gpa = f"{gpa:.2f}"
        return formatted_gpa

# Creating an instance of the StartApp class and starting the application
app = StartApp()
app.run()







