import tkinter as tk
import psycopg2
#from getpass import getpass
from tkinter import ttk
import random
#import time
#import tksheet
#from tksheet import Sheet
from PIL import Image, ImageTk
#from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PyPDF2 import PdfReader 
from shutil import copyfile
import fitz  # PyMuPDF

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
        #file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=window.quit)

        # Create a Help menu
        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Student", menu=help_menu)
        help_menu.add_command(label="Generate", command=self.define_generate_student)

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
        self.instructor_tree = ttk.Treeview(self.instructor_tab, columns=("Registry No", "Title", "Name", "Surname", "Quota", "Lesson", "Field"), show="headings")
        self.instructor_tree.heading("#1", text="Registry No")
        self.instructor_tree.heading("#2", text="Title")
        self.instructor_tree.heading("#3", text="Name")
        self.instructor_tree.heading("#4", text="Surname")
        self.instructor_tree.heading("#5", text="Quota")
        self.instructor_tree.heading("#6", text="Lesson")
        self.instructor_tree.heading("#7", text="Field")
        self.instructor_tree.pack()
        self.get_instructor_data()
        
        # Create the context menu
        self.instructor_m = tk.Menu(self.instructor_tree, tearoff=0)
        self.instructor_m.add_command(label="Update", command=self.update_instructor)
        self.instructor_m.add_command(label="Delete", command=self.delete_instructor)
        self.instructor_m.add_separator()
        
        # Tab 3
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
        self.get_student_data() 
        
        # Create the context menu
        self.student_m = tk.Menu(self.student_tree, tearoff=0)
        self.student_m.add_command(label="Update", command=self.update_student)
        self.student_m.add_command(label="Delete", command=self.delete_student)
        self.student_m.add_separator()
        
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
            self.instructor_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        self.instructor_tree.bind("<Button-3>", self.do_popup_instructor)

    def refresh_instructor_data(self):
        # Clear existing data in the Treeview
        for item in self.instructor_tree.get_children():
            self.instructor_tree.delete(item)

        # Fetch and insert the updated data
        self.get_instructor_data()

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

        self.get_instructor_data()
        success_label = tk.Label(self.define_generate_instructor_window, text="SUCCESSFUL", font=("Helvetica", 12, "bold"), fg="green")
        success_label.place(relx=0.3, rely=0.1)

        self.define_generate_instructor_window.after(1000, self.define_generate_instructor_window.destroy)

    def get_student_data(self):
        select_data_query = "SELECT s.student_no, s.name, s.surname, s.deal_status, i.field FROM student AS s INNER JOIN student_interest AS si on s.student_no=si.student_no INNER JOIN interest as i on si.interest_id=i.interest_id"
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
        self.get_student_data()

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
        update_query = "UPDATE student SET student_no = %s, name = %s, surname = %s, deal_status = %s WHERE student_no = %s"
        data = (student_no, name, surname, status, self.selected_student_no)
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

    def generate_student(self):
        names = ["Akasya", "Arda", "Alya", "Baha", "Barış", "Beren", "Berkan", "Cemre", "Ceyda", "Caner", "Çağla", "Çağdaş", "Deren", "Dilara", "Demirkan", "Edis", "Efe", "Ece", "Ezgi", "Ferda", "Fulya", "Cemre", "Hakan", "İlkay", "İlker", "Kaan", "Gizem", "Helin", "Irmak", "Işıl", "İdil", "Kuzey", "Mert", "Nusret", "Olcay", "Jale", "Kumru", "Melda", "Naz", "Nil", "Oya", "Övünç", "Reha", "Sertaç", "Öykü", "Pelin", "Selin", "Şule", "Taner", "Turgay", "Vedat", "Zafer", "Tülin", "Yonca"]
        surnames = ["Şen", "Kandemir", "Çevik", "Tüten", "Yücel", "Sönmez", "Ertekin", "Dede", "Uyanık", "Aslan", "Akbulut", "Uz", "Kaya", "Kulaç", "Selvi", "Akpınar", "Abacıoğlu", "Işık", "Özer", "Özdemir", "Tahtacı", "Büyükcam", "Kulaksız", "Aksel", "Eroğlu", "Karakum", "Dal", "Yiğit", "Gümüşay", "Yılmaz", "Sezer", "Doğan", "Demir", "Kayayurt", "Turgut", "Aldinç", "Tekin", "Almacıoğlu", "Öner", "Yaman", "Şentürk", "Yıldız", "Güler", "Koç", "Korkmaz", "Aydoğan"]
        grades = ["AA", "BA", "BB", "CB", "CC", "DC"]
        lessons = ["history 1", "turkish 1", "english 1", "physics 1", "linear algebra", "maths 1", "computer laboratory 1", "introduction to computer engineering", "programming 1", "history 2", "turkish 2", "english 2", "physics 2", "maths 2", "computer laboratory 2", "programming 2", "electrical circuit basic", "differential equations", "object oriented programming", "data structures and algorithms", "programming laboratory 1", "logic", "internship 1", "discrete maths", "probability and random variables", "electronic", "computer organization and architecture", "database management", "programming laboratory 2", "system programming", "internship 2", "numerical methods", "sign and systems", "operating systems", "software laboratory 1", "internship 3", "automata theory", "digital data communication", "software laboratory 2", "software engineering", "internship 4"]
        total_lessons_number = [10, 15, 20, 25, 30, 35, 40]
        self.student_number = self.student_number_field.get()
        number = int(self.student_number)
        for i in range(0, number):
            random_number = random.randint(0, 53)
            name = names[random_number]
            random_number = random.randint(0, 45)
            surname = surnames[random_number]
            
            insert_query = "INSERT INTO student (name, surname, username, password, deal_status) VALUES (%s, %s, %s, %s, %s)"
            data_to_insert = (name, surname, name, surname, 0)

            self.db.execute_query(insert_query, data_to_insert)
            self.db.commit()

            random_number = random.randint(0, 6)
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

        select_data_query = "SELECT student_no FROM student"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()

        for result in results:
            random_number = random.randint(1, 10)
            student_interest_id = random_number
            insert_query_2 = "INSERT INTO student_interest (student_no, interest_id) VALUES (%s, %s)"
            data_to_insert_2 = (result, student_interest_id)        
            self.db.execute_query(insert_query_2, data_to_insert_2)
            self.db.commit()    

        self.get_student_data()
        success_label = tk.Label(self.define_generate_student_window, text="SUCCESSFUL", font=("Helvetica", 12, "bold"), fg="green")
        success_label.place(relx=0.3, rely=0.1)

        self.define_generate_student_window.after(1000, self.define_generate_student_window.destroy)

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
        file_menu.add_command(label="Upload", command=self.open_upload_transcript_window)
        #file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=window.quit)

        # Create a Help menu
        help_menu = tk.Menu(menu)
        menu.add_cascade(label="About", menu=help_menu)
        help_menu.add_command(label="About")
        
        # Create tabs
        tab_control = ttk.Notebook(window)

        # Tab 1
        general_tab = ttk.Frame(tab_control)
        tab_control.add(general_tab, text="General")
        general_label = tk.Label(general_tab, text="General Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        general_label.pack()

        name_surname_label = tk.Label(general_tab, text=f"{self.result[0][1]} {self.result[0][2]}", font=("Helvetica", 12, "bold"), fg="brown")
        name_surname_label.place(relx=0.85, rely=0.03)

        # Tab 2
        self.lesson_tab = ttk.Frame(tab_control)
        tab_control.add(self.lesson_tab, text="Lessons")
        instructor_label = tk.Label(self.lesson_tab, text="Lessons Taken and Grades", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        instructor_label.pack()
        #button1 = tk.Button(tab1, text="Open Tab 2", command=lambda: open_tab(tab2))
        #button1.pack()

        name_surname_label = tk.Label(self.lesson_tab, text=f"{self.result[0][1]} {self.result[0][2]}", font=("Helvetica", 12, "bold"), fg="brown")
        name_surname_label.place(relx=0.85, rely=0.03)

        # Create a Treeview widget (the table)
        self.lesson_tree = ttk.Treeview(self.lesson_tab, columns=("Lesson Name", "AKTS", "Mark"), show="headings")
        self.lesson_tree.heading("#1", text="Lesson Name")
        self.lesson_tree.heading("#2", text="AKTS")
        self.lesson_tree.heading("#3", text="Mark")
        self.lesson_tree.pack()
        self.get_lesson_data()

        # Tab 3
        self.interest_tab = ttk.Frame(tab_control)
        tab_control.add(self.interest_tab, text="Interest Field")
        student_label = tk.Label(self.interest_tab, text="Interest Field Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        student_label.pack()
        #button2 = tk.Button(tab2, text="Open Tab 1", command=lambda: open_tab(tab1))
        #button2.pack()

        name_surname_label = tk.Label(self.interest_tab, text=f"{self.result[0][1]} {self.result[0][2]}", font=("Helvetica", 12, "bold"), fg="brown")
        name_surname_label.place(relx=0.85, rely=0.03)

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
        self.interest_tree = ttk.Treeview(self.interest_tab, columns=("Lesson Name", "Interest Field", "Instructor Title", "Instructor Name", "Instructor Surname", "Quota"), show="headings")
        self.interest_tree.heading("#1", text="Lesson Name")
        self.interest_tree.heading("#2", text="Interest Field")
        self.interest_tree.heading("#3", text="Instructor Title")
        self.interest_tree.heading("#4", text="Instructor Name")
        self.interest_tree.heading("#5", text="Instructor Surname")
        self.interest_tree.heading("#6", text="Quota")
        self.interest_tree.pack()
        self.get_interest_data()

        # Create the context menu
        self.interest_m = tk.Menu(self.interest_tree, tearoff=0)
        self.interest_m.add_command(label="Demand")
        self.interest_m.add_separator()
        
        # Set the default tab to open
        tab_control.select(general_tab)

        tab_control.pack(expand=1, fill="both")
        
        # Start the tkinter main loop
        window.mainloop()

    def open_upload_transcript_window(self):
        self.upload_transcript_window = tk.Toplevel()
        self.upload_transcript_window.title("Upload Transcript")
        self.upload_transcript_window.state("zoomed")

        # Label to display the selected file and number of pages
        self.status_label = tk.Label(self.upload_transcript_window, text="", wraplength=300)
        self.status_label.pack()

        upload_transcript_button = tk.Button(self.upload_transcript_window, text="Upload File", bg="#99FFFF", fg="#994C00", padx=5, font=("Helvetica", 10, "bold"), borderwidth=5, relief="ridge", command=self.upload_pdf_file)
        upload_transcript_button.place(relx=0.47, rely=0.8)

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
            pdf_reader = PdfReader(open(file_path, "rb"))
            num_pages = len(pdf_reader.pages)
            self.status_label.config(text=f"Selected File: {file_path}\nNumber of Pages: {num_pages}")
            # Create a text display area to show the extracted text
            text_display = tk.Text(self.upload_transcript_window, height=30, width=120)
            text_display.pack()
            doc = fitz.open(file_path)
            text = ""

            for page in doc:
                extracted_text = page.get_text()
                text += extracted_text

            text_display.delete(1.0, tk.END)
            text_display.insert(tk.END, text)

    def get_lesson_data(self):
        select_data_query = "SELECT l.name, l.AKTS, sl.mark FROM student_lesson AS sl INNER JOIN lesson AS l on sl.lesson_id=l.lesson_id WHERE sl.student_no = %s"
        data_to_insert = (self.result[0][0],)
        self.db.execute_query(select_data_query, data_to_insert)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.lesson_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        #self.lesson_tree.bind("<Button-3>", self.do_popup_instructor)

    def get_interest_data(self):
        select_data_query = "SELECT ol.name, inte.field, i.title, i.name, i.surname, i.quota FROM instructor AS i INNER JOIN instructor_opened_lesson AS iol on i.registry_no=iol.registry_no INNER JOIN opened_lesson as ol on iol.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli ON ol.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte on oli.interest_id=inte.interest_id"
        self.db.execute_query(select_data_query)
        results = self.db.fetch_data()

        # Insert data into the table
        for item in results:
            self.interest_tree.insert("", "end", values=item)

        # Bind the right-click context menu to the Treeview
        self.interest_tree.bind("<Button-3>", self.do_popup_interest)
    
    def refresh_interest_data(self):
        # Clear existing data in the Treeview
        for item in self.interest_tree.get_children():
            self.interest_tree.delete(item)

    def on_lesson_option_selected(self, *args):
        self.refresh_interest_data()
        selected_lesson = self.lesson_selected_option.get()
        select_data_query = "SELECT ol.name, inte.field, i.title, i.name, i.surname, i.quota FROM instructor AS i INNER JOIN instructor_opened_lesson AS iol on i.registry_no=iol.registry_no INNER JOIN opened_lesson as ol on iol.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli ON ol.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte on oli.interest_id=inte.interest_id  WHERE ol.name = %s"
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
        select_data_query = "SELECT ol.name, inte.field, i.title, i.name, i.surname, i.quota FROM instructor AS i INNER JOIN instructor_opened_lesson AS iol on i.registry_no=iol.registry_no INNER JOIN opened_lesson as ol on iol.opened_lesson_id=ol.opened_lesson_id INNER JOIN opened_lesson_interest AS oli ON ol.opened_lesson_id=oli.opened_lesson_id INNER JOIN interest AS inte on oli.interest_id=inte.interest_id  WHERE inte.field = %s"
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
            self.interest_m.tk_popup(event.x_root, event.y_root)

            select_query = "SELECT i.registry_no, iol.opened_lesson_id FROM instructor AS i INNER JOIN instructor_opened_lesson AS iol on i.registry_no=iol.registry_no INNER JOIN opened_lesson AS ol on iol.opened_lesson_id=ol.opened_lesson_id WHERE ol.name = %s"
            data = (self.selected_opened_lesson_name,)
            self.db.execute_query(select_query, data)
            results = self.db.fetch_data()
            
            insert_query = "INSERT INTO deal (student_no, registry_no, opened_lesson_id, deal_status) VALUES (%s, %s, %s, %s)"
            data_to_insert = (self.result[0][0], results[0][0], results[0][1], 0)
            self.db.execute_query(insert_query, data_to_insert)
            self.db.commit()

            confirmation_window = tk.Tk()
            confirmation_window.title("Confirmation Window")
            confirmation_window.geometry("300x150+500+300")

            confirmation_label = tk.Label(confirmation_window, text="Request Send Successfully", font=("Helvetica", 12, "bold"), fg="green")
            confirmation_label.place(relx=0.1, rely=0.3)

# Creating an instance of the StartApp class and starting the application
app = StartApp()
app.run()







