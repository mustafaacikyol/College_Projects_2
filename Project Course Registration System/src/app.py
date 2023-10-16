import tkinter as tk
import psycopg2
from getpass import getpass

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
        admin_button = tk.Button(self.window, text="Admin Panel", bg="#99FFFF", fg="#994C00", padx=20, pady=10, font=custom_font, borderwidth=5, relief="ridge", command=self.open_admin_window)
        admin_button.place(relx=0.5, rely=0.4, anchor='center')

        instructor_button = tk.Button(self.window, text="Instructor Panel", bg="#99FFFF", fg="#994C00", padx=20, pady=10, font=custom_font, borderwidth=5, relief="ridge", command=self.open_instructor_window)
        instructor_button.place(relx=0.5, rely=0.5, anchor='center')

        student_button = tk.Button(self.window, text="Student Panel", bg="#99FFFF", fg="#994C00", padx=20, pady=10, font=custom_font, borderwidth=5, relief="ridge", command=self.open_student_window)
        student_button.place(relx=0.5, rely=0.6, anchor='center')

        label = tk.Label(self.window, text="Project Course Registration System", font=("Helvetica", 25, "bold"), fg="brown", pady=100)
        label.pack()

        # Add widgets and logic here

    def open_admin_window(self):
        new_window = tk.Toplevel(self.window)
        new_window.title("Admin Panel")
        new_window.state("zoomed")
        # Add content and widgets for the admin panel here

    def open_instructor_window(self):
        new_window = tk.Toplevel(self.window)
        new_window.title("Instructor Panel")
        new_window.state("zoomed")
        # Add content and widgets for the instructor panel here

    def open_student_window(self):
        new_window = tk.Toplevel(self.window)
        new_window.title("Student Panel")
        new_window.state("zoomed")
        # Add content and widgets for the student panel here

    def run(self):
        # Start the tkinter main loop
        self.window.mainloop()
    
    

# Creating an instance of the StartApp class and starting the application
app = StartApp()
app.run()

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

# Execute a query
cursor.execute("SELECT * FROM admin")

# Fetch and print the results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Commit and close
conn.commit()
cursor.close()
conn.close()

def check_credentials(username, password):
    try:
        conn = psycopg2.connect(**conn)
        cursor = conn.cursor()

        # Query the database to check the credentials
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()

        if result:
            print("Login successful!")
        else:
            print("Invalid username or password.")

        conn.close()
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

if __name__ == "__main__":
    print("Enter your login credentials:")
    username = input("Username: ")
    password = getpass("Password: ")

    check_credentials(username, password)