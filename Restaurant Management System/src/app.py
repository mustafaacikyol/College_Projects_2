import tkinter as tk
from tkinter import ttk

table = 6
waiter = 3
chef = 2
payment = 1

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
        first_problem_button = tk.Button(self.window, text="First Problem", bg="#99FFFF", fg="#994C00", padx=20, pady=10, font=custom_font, borderwidth=5, relief="ridge", command=self.open_first_problem)
        first_problem_button.place(relx=0.5, rely=0.4, anchor='center')

        second_problem_button = tk.Button(self.window, text="Second Problem", bg="#99FFFF", fg="#994C00", padx=20, pady=10, font=custom_font, borderwidth=5, relief="ridge", command=self.open_second_problem)
        second_problem_button.place(relx=0.5, rely=0.53, anchor='center')

        label = tk.Label(self.window, text="Restaurant Management System", font=("Helvetica", 25, "bold"), fg="brown", pady=100)
        label.pack()

    def run(self):
        # Start the tkinter main loop
        self.window.mainloop()

    def open_first_problem(self):
        first_problem = FirstProblem()
        first_problem.set_step_number()
    
    def open_second_problem(self):
        second_problem = SecondProblem()

class FirstProblem:
    def __init__(self):
        # Create a main window
        self.first_problem_window = tk.Tk()

        # setting attribute
        self.first_problem_window.state('zoomed')

        # Set the title of the window
        self.first_problem_window.title("First Problem")
    
    def set_step_number(self):
        self.step_number_label = tk.Label(self.first_problem_window, text="Enter the number of steps : ", font=("Helvetica", 15, "bold"), fg="brown")
        self.step_number_label.place(relx=0.35, rely=0.4)

        # Create an Entry widget for text input
        self.step_number_field = tk.Entry(self.first_problem_window, width=3, font=('Arial 15'))
        self.step_number_field.place(relx=0.55, rely=0.4)
        
        self.set_step_number_btn = tk.Button(self.first_problem_window, text="Submit", bg="#99FFFF", fg="#994C00", padx=15, pady=4, font=("Helvetica", 12, "bold"), borderwidth=5, relief="ridge", command=self.open_scenario)
        self.set_step_number_btn.place(relx=0.43, rely=0.5)
        
    def open_scenario(self):
        step_number = int(self.step_number_field.get())
        self.first_problem_window.destroy()
        self.scenario_window = tk.Toplevel()
        self.scenario_window.state('zoomed')
        self.scenario_window.title("First Problem")
        # Create a menu bar
        menu = tk.Menu(self.scenario_window)
        self.scenario_window.config(menu=menu)

        # Create a File menu
        interface_menu = tk.Menu(menu)
        menu.add_cascade(label="Interface", menu=interface_menu)
        interface_menu.add_command(label="Waiter", command=self.generate_waiter_gui)
        interface_menu.add_command(label="Chef")
        interface_menu.add_command(label="Payment")
        interface_menu.add_separator()
        interface_menu.add_command(label="Exit", command=self.scenario_window.quit)
        # Lists to store customer and priority values
        customer_values = []
        priority_values = []
        y = 0.1
        for step in range(step_number):
            step_label = tk.Label(self.scenario_window, text=f"Step {step + 1} : ", font=("Helvetica", 15, "bold"), fg="brown")
            step_label.place(relx=0.3, rely=y)

            customer_field = tk.Entry(self.scenario_window, width=3, font=('Arial 15'))
            customer_field.place(relx=0.4, rely=y)

            customer_label = tk.Label(self.scenario_window, text=" Customer", font=("Helvetica", 15, "bold"))
            customer_label.place(relx=0.43, rely=y)

            priority_field = tk.Entry(self.scenario_window, width=3, font=('Arial 15'))
            priority_field.place(relx=0.58, rely=y)

            priority_label = tk.Label(self.scenario_window, text=" Prioritized", font=("Helvetica", 15, "bold"))
            priority_label.place(relx=0.61, rely=y)

            # Append Entry widgets to the lists
            customer_values.append(customer_field)
            priority_values.append(priority_field)

            y += 0.1

        start_app_btn = tk.Button(self.scenario_window, text="Start", bg="#99FFFF", fg="#994C00", padx=15, pady=4, font=("Helvetica", 12, "bold"), borderwidth=5, relief="ridge", command=lambda: self.start_scenario(customer_values, priority_values))
        start_app_btn.place(relx=0.47, rely=y)

    def start_scenario(self, customer_values, priority_values):
        # Access values from the lists
        for customer, priority in zip(customer_values, priority_values):
            customer_value = customer.get()
            priority_value = priority.get()

            # Do something with the values (e.g., print or process them)
            # print(f"Customer: {customer_value}, Priority: {priority_value}")

    def generate_waiter_gui(self):
        self.waiter_gui = tk.Toplevel()
        self.waiter_gui.state('zoomed')
        self.waiter_gui.title("Waiter Interface")

        # Create tabs
        tab_control = ttk.Notebook(self.waiter_gui)
        
        # Tab 1
        self.waiter_one_tab = ttk.Frame(tab_control)
        tab_control.add(self.waiter_one_tab, text="Waiter 1")
        waiter_label = tk.Label(self.waiter_one_tab, text="Table Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        waiter_label.pack()

        # Get the screen width and height
        screen_width = self.waiter_one_tab.winfo_screenwidth()
        screen_height = self.waiter_one_tab.winfo_screenheight()

        # Set the size of each square and the gap between them
        square_size = 200
        gap = 20

        # Calculate the total width and height of all squares and gaps
        total_width = 3 * square_size + 2 * gap
        total_height = 2 * square_size + gap

        # Calculate the starting position to center the squares
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2

        # Create and display six squares in two rows and three columns
        for row in range(2):
            for col in range(3):
                square_frame = tk.Frame(self.waiter_one_tab, width=square_size, height=square_size, bd=2, relief="solid")
                square_frame.place(x=start_x + col * (square_size + gap), y=start_y + row * (square_size + gap))

                # Display information in the top right of each square
                label_table_state = tk.Label(square_frame, text="Table state: empty", anchor="e", padx=5)
                label_order_state = tk.Label(square_frame, text="Order state: empty", anchor="e", padx=5)

                label_table_state.pack(side="top", fill="both")
                label_order_state.pack(side="top", fill="both")

        # Tab 2
        self.waiter_two_tab = ttk.Frame(tab_control)
        tab_control.add(self.waiter_two_tab, text="Waiter 2")
        waiter_label = tk.Label(self.waiter_two_tab, text="Table Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        waiter_label.pack()

        # Get the screen width and height
        screen_width = self.waiter_two_tab.winfo_screenwidth()
        screen_height = self.waiter_two_tab.winfo_screenheight()

        # Set the size of each square and the gap between them
        square_size = 200
        gap = 20

        # Calculate the total width and height of all squares and gaps
        total_width = 3 * square_size + 2 * gap
        total_height = 2 * square_size + gap

        # Calculate the starting position to center the squares
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2

        # Create and display six squares in two rows and three columns
        for row in range(2):
            for col in range(3):
                square_frame = tk.Frame(self.waiter_two_tab, width=square_size, height=square_size, bd=2, relief="solid")
                square_frame.place(x=start_x + col * (square_size + gap), y=start_y + row * (square_size + gap))

                # Display information in the top right of each square
                label_table_state = tk.Label(square_frame, text="Table state: empty", anchor="e", padx=5)
                label_order_state = tk.Label(square_frame, text="Order state: empty", anchor="e", padx=5)

                label_table_state.pack(side="top", fill="both")
                label_order_state.pack(side="top", fill="both")

        # Tab 3
        self.waiter_three_tab = ttk.Frame(tab_control)
        tab_control.add(self.waiter_three_tab, text="Waiter 3")
        waiter_label = tk.Label(self.waiter_three_tab, text="Table Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        waiter_label.pack()

        # Get the screen width and height
        screen_width = self.waiter_three_tab.winfo_screenwidth()
        screen_height = self.waiter_three_tab.winfo_screenheight()

        # Set the size of each square and the gap between them
        square_size = 200
        gap = 20

        # Calculate the total width and height of all squares and gaps
        total_width = 3 * square_size + 2 * gap
        total_height = 2 * square_size + gap

        # Calculate the starting position to center the squares
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2

        # Create and display six squares in two rows and three columns
        for row in range(2):
            for col in range(3):
                square_frame = tk.Frame(self.waiter_three_tab, width=square_size, height=square_size, bd=2, relief="solid")
                square_frame.place(x=start_x + col * (square_size + gap), y=start_y + row * (square_size + gap))

                # Display information in the top right of each square
                label_table_state = tk.Label(square_frame, text="Table state: empty", anchor="e", padx=5)
                label_order_state = tk.Label(square_frame, text="Order state: empty", anchor="e", padx=5)

                label_table_state.pack(side="top", fill="both")
                label_order_state.pack(side="top", fill="both")

        # Set the default tab to open
        tab_control.select(self.waiter_one_tab)

        tab_control.pack(expand=1, fill="both")

        # Start the tkinter main loop
        self.waiter_gui.mainloop()

    #def generate_chef_gui(self):


class SecondProblem:
    def __init__(self):
        # Create a main window
        self.second_problem_window = tk.Tk()

        # setting attribute
        self.second_problem_window.state('zoomed')

        # Set the title of the window
        self.second_problem_window.title("Second Problem")



# Creating an instance of the StartApp class and starting the application
app = StartApp()
app.run()
