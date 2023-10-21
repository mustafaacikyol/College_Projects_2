import tkinter as tk
import psycopg2
#from getpass import getpass
from tkinter import ttk
import random
#import time
#import tksheet
#from tksheet import Sheet
from PIL import Image, ImageTk
from tkinter import *

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
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Instructor", menu=file_menu)
        file_menu.add_command(label="Generate", command=self.define_generate_instructor)
        file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=window.quit)

        # Create a Help menu
        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Student", menu=help_menu)
        help_menu.add_command(label="About")

        # Create tabs
        tab_control = ttk.Notebook(window)

        # Tab 1
        general_tab = ttk.Frame(tab_control)
        tab_control.add(general_tab, text="General")
        general_label = tk.Label(general_tab, text="General Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        general_label.pack()

        # Tab 2
        self.instructor_tab = ttk.Frame(tab_control)
        tab_control.add(self.instructor_tab, text="Instructor")
        instructor_label = tk.Label(self.instructor_tab, text="Instructor Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        instructor_label.pack()
        #button1 = tk.Button(tab1, text="Open Tab 2", command=lambda: open_tab(tab2))
        #button1.pack()

        # Create a Treeview widget (the table)
        self.tree = ttk.Treeview(self.instructor_tab, columns=("Registry No", "Title", "Name", "Surname", "Quota", "Lesson", "Field"), show="headings")
        self.tree.heading("#1", text="Registry No")
        self.tree.heading("#2", text="Title")
        self.tree.heading("#3", text="Name")
        self.tree.heading("#4", text="Surname")
        self.tree.heading("#5", text="Quota")
        self.tree.heading("#6", text="Lesson")
        self.tree.heading("#7", text="Field")
        self.tree.pack()
        self.get_instructor_data()
        
        # Create the context menu
        self.m = tk.Menu(self.tree, tearoff=0)
        self.m.add_command(label="Update", command=self.update_instructor)
        self.m.add_command(label="Delete", command=self.delete_instructor)
        self.m.add_separator()
        
        # Tab 3
        student_tab = ttk.Frame(tab_control)
        tab_control.add(student_tab, text="Student")
        student_label = tk.Label(student_tab, text="Student Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        student_label.pack()
        #button2 = tk.Button(tab2, text="Open Tab 1", command=lambda: open_tab(tab1))
        #button2.pack()

        # Set the default tab to open
        tab_control.select(general_tab)

        tab_control.pack(expand=1, fill="both")

        # Start the tkinter main loop
        window.mainloop()

    def get_instructor_data(self):
        select_data_query = "SELECT i.registry_no, i.title, i.name, i.surname, i.quota, ol.name, inte.field FROM instructor AS i INNER JOIN instructor_opened_lesson AS iol on i.registry_no=iol.registry_no INNER JOIN opened_lesson as ol on iol.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli ON ol.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte on oli.interest_id=inte.interest_id"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        self.tree.bind("<Button-3>", self.do_popup)

    def do_popup(self, event):
        item = self.tree.item(self.tree.selection())  # Get the selected item
        if item:
            self.selected_registry_no = item['values'][0]  # Extract the 'registry_no' value
            self.m.tk_popup(event.x_root, event.y_root)

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
            selected_item = self.tree.selection()
            if selected_item:
                self.tree.delete(selected_item)

            # Optionally clear the selected_registry_no attribute
            del self.selected_registry_no

    def update_instructor(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_values = self.tree.item(selected_item, "values")
            if selected_values:
                # Open the update window with the instructor's data for editing
                self.open_update_window(selected_values)

    def open_update_window(self, selected_values):
        update_window = tk.Toplevel()
        update_window.title("Update Instructor")
        update_window.state("zoomed")
        # Create input fields and labels for updating instructor data
        # You can design and populate this window as needed

        # Example: Create an entry field for updating the instructor's name
        name_label = tk.Label(update_window, text="Title")
        name_label.pack()
        name_entry = tk.Entry(update_window, width=30)
        name_entry.insert(0, selected_values[1])  # Pre-fill with the instructor's current name
        name_entry.pack()

        name_label = tk.Label(update_window, text="Name")
        name_label.pack()
        name_entry = tk.Entry(update_window, width=30)
        name_entry.insert(0, selected_values[2])  # Pre-fill with the instructor's current name
        name_entry.pack()

        name_label = tk.Label(update_window, text="Surname")
        name_label.pack()
        name_entry = tk.Entry(update_window, width=30)
        name_entry.insert(0, selected_values[3])  # Pre-fill with the instructor's current name
        name_entry.pack()

        name_label = tk.Label(update_window, text="Quota")
        name_label.pack()
        name_entry = tk.Entry(update_window, width=30)
        name_entry.insert(0, selected_values[4])  # Pre-fill with the instructor's current name
        name_entry.pack()

        name_label = tk.Label(update_window, text="Lesson")
        name_label.pack()
        name_entry = tk.Entry(update_window, width=30)
        name_entry.insert(0, selected_values[5])  # Pre-fill with the instructor's current name
        name_entry.pack()

        name_label = tk.Label(update_window, text="Field")
        name_label.pack()
        name_entry = tk.Entry(update_window, width=30)
        name_entry.insert(0, selected_values[6])  # Pre-fill with the instructor's current name
        name_entry.pack()

        # Create a button to save the updates
        save_button = tk.Button(update_window, text="Save", command=self.save_instructor_updates, bg="#99FFFF", fg="#994C00", padx=10, pady=3, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge")
        save_button.place(relx=0.48, rely=0.38)

    def save_instructor_updates(self):
        print(1)

    def define_generate_instructor(self):
        self.define_generate_window = tk.Toplevel()
        self.define_generate_window.title("Generate Instructor")
        self.define_generate_window.geometry("300x200+500+250")

        instructor_number_label = tk.Label(self.define_generate_window, text="Instructor Number to Generate : ", font=("Helvetica", 10, "bold"), fg="brown")
        instructor_number_label.place(relx=0.05, rely=0.3)

        self.instructor_number_field = tk.Entry(self.define_generate_window, width=3, font=('Arial 12'))
        self.instructor_number_field.place(relx=0.75, rely=0.3)
        
        instructor_generate_button = tk.Button(self.define_generate_window, text="Generate", bg="#99FFFF", fg="#994C00", padx=5, pady=2, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge", command=self.generate_instructor)
        instructor_generate_button.place(relx=0.35, rely=0.6)

    def generate_instructor(self):
        titles = ["Dr.", "Associate Professor", "Professor"]
        names = ["Ahmet", "Mehmet", "Serap", "Buse", "Hasan", "Kemal"]
        surnames = ["Yılmaz", "Kaya", "Doğan"]
        quotas = [10, 20, 30, 40, 50]
        self.instructor_number = self.instructor_number_field.get()
        number = int(self.instructor_number)
        for i in range(0, number):
            random_number = random.randint(0, 2)
            title = titles[random_number]
            random_number = random.randint(0, 5)
            name = names[random_number]
            random_number = random.randint(0, 2)
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

        self.get_instructor_data()
        success_label = tk.Label(self.define_generate_window, text="SUCCESSFUL", font=("Helvetica", 12, "bold"), fg="green")
        success_label.place(relx=0.3, rely=0.1)

        self.define_generate_window.after(1000, self.define_generate_window.destroy)

class Instructor:
    def __init__(self):
        self.login_window = tk.Tk()

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
        select_query = "SELECT username,password FROM instructor WHERE username = %s AND password = %s"
        data = (username, password)

        self.db.execute_query(select_query, data)
        result = self.db.fetch_data()

        if result:
            Instructor.close_login(self)
        else:
            error_label = tk.Label(self.login_window, text="Invalid username or password!", font=("Helvetica", 15, "bold"), fg="red")
            error_label.place(relx=0.37, rely=0.3)

    def close_login(self):
        self.login_window.destroy()
        Instructor.dashboard()

    def dashboard():
        window = tk.Toplevel()
        window.title("Instructor Dashboard")
        window.state("zoomed")

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
       
        db = DatabaseConnection()
        # Query the database to check the credentials
        select_query = "SELECT username,password FROM student WHERE username = %s AND password = %s"
        data = (username, password)

        db.execute_query(select_query, data)
        result = db.fetch_data()

        if result:
            Student.close_login(self)
        else:
            error_label = tk.Label(self.login_window, text="Invalid username or password!", font=("Helvetica", 15, "bold"), fg="red")
            error_label.place(relx=0.37, rely=0.3)

    def close_login(self):
        self.login_window.destroy()
        Student.dashboard()

    def dashboard():
        window = tk.Toplevel()
        window.title("Student Dashboard")
        window.state("zoomed")

# Creating an instance of the StartApp class and starting the application
app = StartApp()
app.run()






