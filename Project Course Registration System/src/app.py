import tkinter as tk
import psycopg2
#from getpass import getpass
from tkinter import ttk

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
    
class Admin():
    def __init__(self):
        self.login_window = tk.Tk()

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
        try:
            # Establish the connection
            conn = psycopg2.connect(
            dbname="Registration System",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432"
            )

            # Create a cursor
            cursor = conn.cursor()
            # Query the database to check the credentials
            cursor.execute("SELECT username,password FROM admin WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()

            if result:
                Admin.close_login(self)
            else:
                error_label = tk.Label(self.login_window, text="Invalid username or password!", font=("Helvetica", 15, "bold"), fg="red")
                error_label.place(relx=0.37, rely=0.3)

            conn.close()
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)
        
        # Commit and close
        #conn.commit()
        #cursor.close()
        #conn.close()

    def close_login(self):
        self.login_window.destroy()
        Admin.dashboard()

    def dashboard():
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
        file_menu.add_command(label="New")
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
        instructor_tab = ttk.Frame(tab_control)
        tab_control.add(instructor_tab, text="Instructor")
        instructor_label = tk.Label(instructor_tab, text="Instructor Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        instructor_label.pack()
        #button1 = tk.Button(tab1, text="Open Tab 2", command=lambda: open_tab(tab2))
        #button1.pack()

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

class Instructor():
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
        try:
            # Establish the connection
            conn = psycopg2.connect(
            dbname="Registration System",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432"
            )

            # Create a cursor
            cursor = conn.cursor()
            # Query the database to check the credentials
            cursor.execute("SELECT username,password FROM instructor WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()

            if result:
                Instructor.close_login(self)
            else:
                error_label = tk.Label(self.login_window, text="Invalid username or password!", font=("Helvetica", 15, "bold"), fg="red")
                error_label.place(relx=0.37, rely=0.3)

            conn.close()
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)
        
        # Commit and close
        #conn.commit()
        #cursor.close()
        #conn.close()

    def close_login(self):
        self.login_window.destroy()
        Instructor.dashboard()

    def dashboard():
        window = tk.Toplevel()
        window.title("Instructor Dashboard")
        window.state("zoomed")

class Student():
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
        try:
            # Establish the connection
            conn = psycopg2.connect(
            dbname="Registration System",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432"
            )

            # Create a cursor
            cursor = conn.cursor()
            # Query the database to check the credentials
            cursor.execute("SELECT username,password FROM student WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()

            if result:
                Student.close_login(self)
            else:
                error_label = tk.Label(self.login_window, text="Invalid username or password!", font=("Helvetica", 15, "bold"), fg="red")
                error_label.place(relx=0.37, rely=0.3)

            conn.close()
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)
        
        # Commit and close
        #conn.commit()
        #cursor.close()
        #conn.close()

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

"""
if __name__ == "__main__":
    print("Enter your login credentials:")
    username = input("Username: ")
    password = getpass("Password: ")

    check_credentials(username, password)
"""