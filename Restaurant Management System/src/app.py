import tkinter as tk

class StartApp:
    def __init__(self):
        # Create a main window
        self.window = tk.Tk()

        # setting attribute
        self.window.state('zoomed')

        # Set the title of the window
        self.window.title("Restaurant Management System")

        # Create a custom font with a bold style
        custom_font = ("Helvetica", 12, "bold")

        # Create buttons
        first_problem_button = tk.Button(self.window, text="First Problem", bg="#99FFFF", fg="#994C00", padx=20, pady=10, font=custom_font, borderwidth=5, relief="ridge")
        first_problem_button.place(relx=0.5, rely=0.4, anchor='center')

        second_problem_button = tk.Button(self.window, text="Second Problem", bg="#99FFFF", fg="#994C00", padx=20, pady=10, font=custom_font, borderwidth=5, relief="ridge")
        second_problem_button.place(relx=0.5, rely=0.53, anchor='center')

        label = tk.Label(self.window, text="Restaurant Management System", font=("Helvetica", 25, "bold"), fg="brown", pady=100)
        label.pack()

    def run(self):

        # Start the tkinter main loop
        self.window.mainloop()

# Creating an instance of the StartApp class and starting the application
app = StartApp()
app.run()
