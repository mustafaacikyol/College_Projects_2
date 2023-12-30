import tkinter as tk
from tkinter import ttk
import threading
import time
import asyncio
import queue
from concurrent.futures import ThreadPoolExecutor
#import schedule

table = 6
waiter = 3
chef = 2
payment = 1
customer_counter = 1
total_customers = 0
total_non_priority = 0
total_priority = 0
total_payment = 0
table_list = []
table_counter = 0
waiter_list = []
#waiter_counter = 0
chef_list = []
empty_chef_list = []
waiter_queue = queue.Queue()
step_counter = 1

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
        second_problem.set_time()

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
        for i in range(4):
            chef_obj = Chef(f'{i+1}')
            chef_list.append(chef_obj)
            empty_chef_list.append(chef_obj)
        
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
        interface_menu.add_command(label="Chef", command=self.generate_chef_gui)
        interface_menu.add_command(label="Payment", command=self.generate_payment_gui)
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
        global total_customers, total_non_priority, total_priority, table_list, table_counter, waiter_list, chef_list, waiter_queue, customer_counter, step_counter
        for i in range(3):
            waiter_obj = Waiter(f"Waiter {i+1}")
            waiter_list.append(waiter_obj)

        # Access values from the lists
        for customer, priority in zip(customer_values, priority_values):
            customer_value = int(customer.get())
            priority_value = int(priority.get())

            # Do something with the values (e.g., print or process them)
            # print(f"Customer: {customer_value}, Priority: {priority_value}")

            total_non_priority += customer_value
            total_priority += priority_value

        # print(f"Total Non Priority: {total_non_priority}, Total Priority: {total_priority}")
        total_customers = total_non_priority + total_priority
        self.update_payment_gui()
        
        for item in range(6):
            self.generate_priority_customer()
            table_list[table_counter].set_state()
            table_list[table_counter].set_customer(customer_counter-1)
            table_counter += 1
        #update_waiter_gui_thread = threading.Thread(target=self.update_waiter_gui).start()

        table_counter = 0
        self.update_waiter_gui()

        self.write_to_txt_file(f'Step {step_counter}: {total_customers} customers came. There are {total_priority} priotity customers.\n')
        step_counter += 1
        self.write_to_txt_file(f'Step {step_counter}: 6 customers placed on tables. {total_customers-6} customers on hold.\n')
        step_counter += 1

        check_waiter_queue_thread = threading.Thread(target=self.check_empty_chef).start() 

        # Schedule the thread to run after 5 seconds
        order_table_to_waiter_thread = threading.Timer(2.0, self.order_table_to_waiter).start()
        order_table_to_waiter_thread = threading.Timer(4.0, self.order_table_to_waiter).start()

    def write_step(self):
        global step_counter
        self.write_to_txt_file(f'Step {step_counter}: ')
        step_counter += 1

    def write_to_txt_file(self, text1, text2 = None):
        with open('D:/projects 2/first term/first project/Restaurant Management System/log/log.txt', 'a') as file:
            if(text2 != None):
                file.write(f'{text1}')
                file.write(f'{text2}')
            else:
                file.write(f'{text1}')

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
        self.generate_waiter_gui_content(self.waiter_one_tab)

        # Tab 2
        self.waiter_two_tab = ttk.Frame(tab_control)
        tab_control.add(self.waiter_two_tab, text="Waiter 2")
        waiter_label = tk.Label(self.waiter_two_tab, text="Table Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        waiter_label.pack()
        self.generate_waiter_gui_content(self.waiter_two_tab)

        # Tab 3
        self.waiter_three_tab = ttk.Frame(tab_control)
        tab_control.add(self.waiter_three_tab, text="Waiter 3")
        waiter_label = tk.Label(self.waiter_three_tab, text="Table Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        waiter_label.pack()
        self.generate_waiter_gui_content(self.waiter_three_tab)

        # Set the default tab to open
        tab_control.select(self.waiter_one_tab)

        tab_control.pack(expand=1, fill="both")

        # Start the tkinter main loop
        self.waiter_gui.mainloop()

    def generate_waiter_gui_content(self, waiter_tab):
        # Get the screen width and height
        screen_width = waiter_tab.winfo_screenwidth()
        screen_height = waiter_tab.winfo_screenheight()

        # Set the size of each square and the gap between them
        square_size = 150
        gap = 20

        # Calculate the total width and height of all squares and gaps
        total_width = 3 * square_size + 2 * gap
        total_height = 2 * square_size + gap

        # Calculate the starting position to center the squares
        start_x = (screen_width - total_width) // 4
        start_y = (screen_height - total_height) // 2

        # Create and display six squares in a single row with six columns
        for col in range(6):
            global table_list
            table_obj = Table(f'Table {col+1}')
            table_list.append(table_obj)
            table_label = tk.Label(waiter_tab, padx=35, text=f"Table {col+1}", font=("Helvatica", 15, "bold"), fg="brown")
            table_label.place(x=start_x + col * (square_size + gap), y=180)
            square_frame = tk.Frame(waiter_tab, width=square_size, height=square_size, bd=2, relief="solid")
            square_frame.place(x=start_x + col * (square_size + gap), y=start_y)

            # Display information in the top right of each square
            label_customer = tk.Label(square_frame, text=f"Customer: {table_list[col].get_customer()}", anchor="e", padx=15)
            label_table_state = tk.Label(square_frame, text=f"Table state: {table_list[col].get_state()}", anchor="e", padx=15)
            label_order_state = tk.Label(square_frame, text=f"Order state: {table_list[col].get_order_state()}", anchor="e", padx=15)
            label_meal = tk.Label(square_frame, text=f"Meal: {table_list[col].get_meal()}", anchor="e", padx=15)

            label_customer.pack(side="top", fill="both")
            label_table_state.pack(side="top", fill="both")
            label_order_state.pack(side="top", fill="both")
            label_meal.pack(side="top", fill="both")

    def update_waiter_gui(self):  
        waiter_tab_list = [self.waiter_one_tab, self.waiter_two_tab, self.waiter_three_tab]
        # Get the screen width and height
        screen_width = self.waiter_one_tab.winfo_screenwidth()
        screen_height = self.waiter_one_tab.winfo_screenheight()

        # Set the size of each square and the gap between them
        square_size = 150
        gap = 20

        # Calculate the total width and height of all squares and gaps
        total_width = 3 * square_size + 2 * gap
        total_height = 2 * square_size + gap

        # Calculate the starting position to center the squares
        start_x = (screen_width - total_width) // 4
        start_y = (screen_height - total_height) // 2
        for waiter_tab in waiter_tab_list:
            for col in range(6):
                table_obj = Table(f'Table {col+1}')
                table_list.append(table_obj)
                table_label = tk.Label(waiter_tab, padx=35, text=f"Table {col+1}", font=("Helvatica", 15, "bold"), fg="brown")
                table_label.place(x=start_x + col * (square_size + gap), y=180)
                square_frame = tk.Frame(waiter_tab, width=square_size, height=square_size, bd=2, relief="solid")
                square_frame.place(x=start_x + col * (square_size + gap), y=start_y)
                # Display information in the top right of each square
                label_customer = tk.Label(square_frame, text=f"Customer: {table_list[col].get_customer()}", anchor="e", padx=15)
                label_table_state = tk.Label(square_frame, text=f"Table state: {table_list[col].get_state()}", anchor="e", padx=15)
                label_order_state = tk.Label(square_frame, text=f"Order state: {table_list[col].get_order_state()}", anchor="e", padx=15)
                label_meal = tk.Label(square_frame, text=f"Meal: {table_list[col].get_meal()}", anchor="e", padx=15)

                label_customer.pack(side="top", fill="both")
                label_table_state.pack(side="top", fill="both")
                label_order_state.pack(side="top", fill="both")
                label_meal.pack(side="top", fill="both")

    def generate_chef_gui(self):
        self.chef_gui = tk.Toplevel()
        self.chef_gui.state('zoomed')
        self.chef_gui.title("Chef Interface")

        # Create tabs
        tab_control = ttk.Notebook(self.chef_gui)
        
        # Tab 1
        self.chef_one_tab = ttk.Frame(tab_control)
        tab_control.add(self.chef_one_tab, text="Chef 1")
        chef_label = tk.Label(self.chef_one_tab, text="Order Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        chef_label.pack()
        self.generate_chef_gui_content(self.chef_one_tab)

        # Tab 2
        self.chef_two_tab = ttk.Frame(tab_control)
        tab_control.add(self.chef_two_tab, text="Chef 2")
        chef_label = tk.Label(self.chef_two_tab, text="Order Informations", padx=20, pady=20, font=("Helvatica", 15, "bold"), fg="brown")
        chef_label.pack()
        self.generate_chef_gui_content(self.chef_two_tab)

        # Set the default tab to open
        tab_control.select(self.chef_one_tab)

        tab_control.pack(expand=1, fill="both")

        # Start the tkinter main loop
        self.chef_gui.mainloop()

    def generate_chef_gui_content(self, chef_tab):
        # Get the screen width and height
        screen_width = chef_tab.winfo_screenwidth()
        screen_height = chef_tab.winfo_screenheight()

        # Set the size of each square and the gap between them
        square_size = 150
        gap = 50

        # Calculate the total width and height of all squares and gaps
        total_width = 2 * square_size + gap
        total_height = square_size + gap

        # Calculate the starting position to center the squares
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2

        if(chef_tab == self.chef_one_tab):
            a = (0,2)
        elif(chef_tab == self.chef_two_tab):
            a = (2,4)

        for col in range(*a):  
            square_frame = tk.Frame(chef_tab, width=square_size, height=square_size, bd=2, relief="solid")
            if(col<2):
                square_frame.place(x=start_x + col * (square_size + gap), y=start_y)
                meal_label = tk.Label(chef_tab, padx=30, text=f"Meal {col+1}", font=("Helvatica", 15, "bold"), fg="brown")
                meal_label.place(x=start_x + col * (square_size + gap), y=230)
            elif(col==2):
                square_frame.place(x=start_x, y=start_y)
                meal_label = tk.Label(chef_tab, padx=30, text=f"Meal {col-1}", font=("Helvatica", 15, "bold"), fg="brown")
                meal_label.place(x=start_x, y=230)
            elif(col==3):
                square_frame.place(x=start_x + (square_size + gap), y=start_y)
                meal_label = tk.Label(chef_tab, padx=30, text=f"Meal {col-1}", font=("Helvatica", 15, "bold"), fg="brown")
                meal_label.place(x=start_x + (square_size + gap), y=230)

            # Display information in the top right of each square
            label_customer = tk.Label(square_frame, text=f"Customer: {chef_list[col].get_customer()}", anchor="e", padx=5)
            label_order_state = tk.Label(square_frame, text=f"Order state: {chef_list[col].get_order_state()}", anchor="e", padx=5)
            
            label_customer.pack(side="top", fill="both")
            label_order_state.pack(side="top", fill="both")

    def check_empty_chef(self):
        global chef_list, waiter_queue, step_counter
        meal_indexes = []
        counter = 0
        if(waiter_queue.qsize()>0):
            for i,chef in enumerate(chef_list):
                if(chef.get_order_state() == 'empty'):
                    counter += 1
                    chef.set_order_state()
                    meal_indexes.append(i)
                    waiter = waiter_queue.get()
                    chef.set_customer(waiter.get_customer())
                    if(chef.name == "1"):
                        self.write_to_txt_file(f"Step {step_counter}: {waiter.name} passed the order of customer {waiter.get_customer()} to the chef.\n")
                        step_counter += 1
                        self.write_to_txt_file(f"Step {step_counter}: Chef {chef.name} took the order for customer {chef.get_customer()} and started to prepare them.\n")
                        step_counter += 1
                        waiter.reset_customer()
                        waiter.reset_order()
                    elif(chef.name == "2" or chef.name == "3"):
                        self.write_to_txt_file(f"Step {step_counter}: {waiter.name} passed the order of customer {waiter.get_customer()} to the chef.\n")
                        step_counter += 1
                        self.write_to_txt_file(f"Step {step_counter}: Chef {int(chef.name)-1} took the order for customer {chef.get_customer()} and started to prepare them.\n")
                        step_counter += 1
                        waiter.reset_customer()
                        waiter.reset_order()
                    elif(chef.name == "4"):
                        self.write_to_txt_file(f"Step {step_counter}: {waiter.name} passed the order of customer {waiter.get_customer()} to the chef.\n")
                        step_counter += 1
                        self.write_to_txt_file(f"Step {step_counter}: Chef {int(chef.name)-2} took the order for customer {chef.get_customer()} and started to prepare them.\n")
                        step_counter += 1
                        waiter.reset_customer()
                        waiter.reset_order()
                    #waiter_queue.get_nowait()
                    if(waiter_queue.qsize() == 0): break
            if counter>0:
                self.update_chef_gui() 
                check_empty_chef_condition_thread = threading.Timer(3.0, self.check_empty_chef_condition, args=(meal_indexes,)).start()
        
        recursive_thread = threading.Timer(1.0, self.check_empty_chef).start()

    def check_empty_chef_condition(self, meal_indexes):
        self.order_chef_to_table(meal_indexes)
        self.chef_meal_ready(meal_indexes)

    def order_table_to_waiter(self):
        global table_list, waiter_list
        is_waiter_get_order = False
        for waiter in waiter_list:
            for table in table_list:
                if waiter.get_order() == False and table.get_state() == 'full' and table.get_order_state() == 'empty':
                    is_waiter_get_order = True
                    table.set_order_state()           
                    waiter.set_customer(table.get_customer())
                    waiter.set_order()
                    break

        if(is_waiter_get_order):
            self.write_step()
        for waiter in waiter_list:
            if waiter.get_order() == True:
                self.write_to_txt_file(f"{waiter.name} took Customer {waiter.get_customer()}'s order ")
        if(is_waiter_get_order):
            self.write_to_txt_file("\n")

        if(is_waiter_get_order):
            self.write_step()
        chef_index = []
        for j,waiter in enumerate(waiter_list):
            for i,chef in enumerate(chef_list):
                if waiter.get_order() == True and chef.get_order_state() == 'empty':
                    self.write_to_txt_file(f"{waiter.name} passed the order of customer {waiter.get_customer()} ")
                    chef.set_order_state()
                    chef_index.append(i)
                    break

        for index in chef_index:
            chef_list[index].set_order_state()
        
        if(is_waiter_get_order):
            self.write_to_txt_file(".\n")
            self.update_waiter_gui()
            self.order_waiter_to_chef()

    def order_waiter_to_chef(self):
        global waiter_queue, waiter_list, step_counter
        meal_indexes = []
        order_count = 0
        order_give_to_chef_count = 0

        self.write_step()
        for waiter in waiter_list:
            if(waiter.get_order() == True):
                order_count += 1
                for i,chef in enumerate(chef_list):
                    if(chef.get_order_state() == 'empty'):
                        order_give_to_chef_count += 1
                        chef.set_customer(waiter.get_customer())
                        chef.set_order_state()
                        if(i==0):
                            self.write_to_txt_file(f"Chef {chef.name} took the order for customer {chef.get_customer()} ")
                        elif(i==1 or i==2):
                            self.write_to_txt_file(f"Chef {int(chef.name)-1} took the order for customer {chef.get_customer()} ")
                        elif(i==3):
                            self.write_to_txt_file(f"Chef {int(chef.name)-2} took the order for customer {chef.get_customer()} ")
                        waiter.reset_customer()
                        waiter.reset_order()
                        meal_indexes.append(i)
                        break
        self.write_to_txt_file(f"\n")

        if(order_count-order_give_to_chef_count == 2):
            waiter_queue.put(waiter_list[1])
            waiter_queue.put(waiter_list[2])
            self.write_to_txt_file(f"Step {step_counter}: Waiter 2 and waiter 3 are on standby as there are no chef available at the moment.\n")
            step_counter += 1
        elif(order_count-order_give_to_chef_count == 1):
            waiter_queue.put(waiter_list[2])
            self.write_to_txt_file(f"Step {step_counter}: Waiter 3 are on standby as there are no chef available at the moment.\n")
            step_counter += 1

        self.update_chef_gui()
        order_chef_to_table_thread = threading.Timer(3.0, self.order_chef_to_table, args=(meal_indexes,)).start()
        chef_meal_ready_thread = threading.Timer(3.0, self.chef_meal_ready, args=(meal_indexes,)).start()
        
    def order_chef_to_table(self, list):
        global chef_list, table_list
        customer_index = []
        table_index = []
        for i in list:
            for j,table in enumerate(table_list):
                if chef_list[i].get_customer() == table.get_customer():
                    customer_index.append(chef_list[i].get_customer())
                    table_index.append(j)
                    table.set_meal()
                    break
        self.update_waiter_gui()
        
        leave_table_thread = threading.Timer(3.0, self.leave_table, args=(customer_index, table_index))
        leave_table_thread.start()
        
    def chef_meal_ready(self, list):
        global chef_list, step_counter
        for i in list:
            if(i==0):
                self.write_to_txt_file(f"Step {step_counter}: Chef {chef_list[i].name} finished Customer {chef_list[i].get_customer()}'s order. Customer {chef_list[i].get_customer()} start to eating.\n")
                step_counter += 1
            elif(i==1 or i==2):
                self.write_to_txt_file(f"Step {step_counter}: Chef {int(chef_list[i].name)-1} finished Customer {chef_list[i].get_customer()}'s order. Customer {chef_list[i].get_customer()} start to eating.\n")
                step_counter += 1
            elif(i==3):
                self.write_to_txt_file(f"Step {step_counter}: Chef {int(chef_list[i].name)-2} finished Customer {chef_list[i].get_customer()}'s order. Customer {chef_list[i].get_customer()} start to eating.\n")
                step_counter += 1
            chef_list[i].set_order_state()
            chef_list[i].reset_customer()
        self.update_chef_gui()

    def leave_table(self, customer_index, table_index):
        global table_list, customer_counter, step_counter, total_customers
        for table in table_index:
            customer = table_list[table].get_customer()
            table_list[table].reset_customer()
            table_list[table].set_state()
            table_list[table].set_order_state()
            table_list[table].set_meal()
            self.write_to_txt_file(f"Step {step_counter}: Customer {customer} leave from {table_list[table].name} to pay the bill.\n")
            step_counter += 1
            if customer_counter<=total_customers:
                table_list[table].set_customer(customer_counter)
                self.write_to_txt_file(f"Step {step_counter}: Customer {customer_counter} sit at the {table_list[table].name}.\n")
                step_counter += 1
                customer_counter += 1
                table_list[table].set_state()
        self.update_waiter_gui()
        order_table_to_waiter_thread = threading.Timer(2.0, self.order_table_to_waiter)
        order_table_to_waiter_thread.start()
        self.prepare_payment(customer_index)

    def prepare_payment(self, customer_index):
        global step_counter
        for customer in customer_index:
            making_payment_thread = threading.Thread(target=self.making_payment, args=(customer,))
            making_payment_thread.start()
            time.sleep(1)

    def making_payment(self, customer):
        global step_counter, total_payment
        self.write_to_txt_file(f"Step {step_counter}: Customer {customer} paid the bill.\n")
        step_counter += 1
        total_payment += 1
        self.update_payment_gui()

    def update_chef_gui(self):
        # Get the screen width and height
        screen_width = self.chef_one_tab.winfo_screenwidth()
        screen_height = self.chef_one_tab.winfo_screenheight()

        # Set the size of each square and the gap between them
        square_size = 150
        gap = 50

        # Calculate the total width and height of all squares and gaps
        total_width = 2 * square_size + gap
        total_height = square_size + gap

        # Calculate the starting position to center the squares
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2

        for col in range(0,2):  
            meal_label = tk.Label(self.chef_one_tab, padx=30, text=f"Meal {col+1}", font=("Helvatica", 15, "bold"), fg="brown")
            meal_label.place(x=start_x + col * (square_size + gap), y=230)
            square_frame = tk.Frame(self.chef_one_tab, width=square_size, height=square_size, bd=2, relief="solid")
            square_frame.place(x=start_x + col * (square_size + gap), y=start_y)

            # Display information in the top right of each square
            label_customer = tk.Label(square_frame, text=f"Customer: {chef_list[col].get_customer()}", anchor="e", padx=5)
            label_order_state = tk.Label(square_frame, text=f"Order state: {chef_list[col].get_order_state()}", anchor="e", padx=5)
            
            label_customer.pack(side="top", fill="both")
            label_order_state.pack(side="top", fill="both")
        for col in range(2,4):  
            meal_label = tk.Label(self.chef_two_tab, padx=30, text=f"Meal {col-1}", font=("Helvatica", 15, "bold"), fg="brown")
            meal_label.place(x=start_x + (col-2) * (square_size + gap), y=230)
            square_frame = tk.Frame(self.chef_two_tab, width=square_size, height=square_size, bd=2, relief="solid")
            square_frame.place(x=start_x + (col-2) * (square_size + gap), y=start_y)

            # Display information in the top right of each square
            label_customer = tk.Label(square_frame, text=f"Customer: {chef_list[col].get_customer()}", anchor="e", padx=5)
            label_order_state = tk.Label(square_frame, text=f"Order state: {chef_list[col].get_order_state()}", anchor="e", padx=5)
            
            label_customer.pack(side="top", fill="both")
            label_order_state.pack(side="top", fill="both")
        
    def generate_payment_gui(self):
        self.payment_gui = tk.Toplevel()
        self.payment_gui.state('zoomed')
        self.payment_gui.title("Payment Interface")

        # Get the screen width and height
        screen_width = self.payment_gui.winfo_screenwidth()
        screen_height = self.payment_gui.winfo_screenheight()

        # Set the total customer and payment amount
        global total_customers,total_payment
        total_customers = 0
        total_payment = 0

        # Create and display labels in the center of the page
        label_customers = tk.Label(self.payment_gui, text=f"Total Customers: {total_customers}", font=("Helvetica", 14))
        label_payment = tk.Label(self.payment_gui, text=f"Total Payment: ${total_payment:.2f}", font=("Helvetica", 14))

        label_customers.place(x=(screen_width - label_customers.winfo_reqwidth()) // 2, y=screen_height // 2 - 130)
        label_payment.place(x=(screen_width - label_payment.winfo_reqwidth()) // 2, y=screen_height // 2 - 70)

    def update_payment_gui(self):
        # Get the screen width and height
        screen_width = self.payment_gui.winfo_screenwidth()
        screen_height = self.payment_gui.winfo_screenheight()

        # Create and display labels in the center of the page
        label_customers = tk.Label(self.payment_gui, text=f"Total Customers: {total_customers}", font=("Helvetica", 14))
        label_payment = tk.Label(self.payment_gui, text=f"Total Payment: ${total_payment:.2f}", font=("Helvetica", 14))

        label_customers.place(x=(screen_width - label_customers.winfo_reqwidth()) // 2, y=screen_height // 2 - 130)
        label_payment.place(x=(screen_width - label_payment.winfo_reqwidth()) // 2, y=screen_height // 2 - 70)

    def generate_priority_customer(self):
        priority_customer = Customer(f'Customer {customer_counter}',1)

    def generate_non_priority_customer(self):
        non_priority_customer = Customer(f'Customer {customer_counter}')

class Table:
    def __init__(self, name):
        self.name = name
        self.customer = None
        self.state = 'empty'
        self.order_state = 'empty'
        self.meal = 'empty'

    def get_customer(self):
        return self.customer
    
    def set_customer(self, customer_id):
        self.customer = customer_id

    def reset_customer(self):
        self.customer = None

    def get_state(self):
        return self.state
    
    def set_state(self):
        if(self.state == 'empty'):
            self.state = 'full'
        else:
            self.state = 'empty'

    def get_order_state(self):
        return self.order_state
    
    def set_order_state(self):
        if(self.order_state == 'empty'):
            self.order_state = ' taken '
        else:
            self.order_state = 'empty'

    def get_meal(self):
        return self.meal
    
    def set_meal(self):
        if(self.meal == 'empty'):
            self.meal = 'eating'
        else:
            self.meal = 'empty'

class Customer:
    def __init__(self, name, number=None):
        global customer_counter
        self.name = name
        customer_counter += 1

class Waiter:
    def __init__(self, name):
        self.name = name
        self.customer = None
        self.order = False

    def get_customer(self):
        return self.customer
    
    def set_customer(self, customer_id):
        self.customer = customer_id
    
    def reset_customer(self):
        self.customer = None

    def get_order(self):
        return self.order

    def set_order(self):
        if(self.order == False):
            self.order = True
        else:
            self.order = False

    def reset_order(self):
        self.order = False

    #def take_order(self):

class Chef:
    def __init__(self, name):
        self.name = name
        self.customer = None
        self.order_state = 'empty'
        #self.meal_state = 'empty'

    def get_customer(self):
        return self.customer
    
    def set_customer(self, customer_id):
        self.customer = customer_id

    def reset_customer(self):
        self.customer = None

    def get_order_state(self):
        return self.order_state
    
    def set_order_state(self):
        if(self.order_state == 'empty'):
            self.order_state = ' taken '
        else:
            self.order_state = 'empty'

    """ def get_meal_state(self):
        return self.meal_state
    
    def set_meal_state(self):
        if(self.meal_state == 'empty'):
            self.meal_state = 'full'
        else:
            self.meal_state = 'empty' """

class SecondProblem:
    def __init__(self):
        # Create a main window
        self.second_problem_window = tk.Tk()

        # setting attribute
        self.second_problem_window.state('zoomed')

        # Set the title of the window
        self.second_problem_window.title("Second Problem")

    def set_time(self):
        time_label = tk.Label(self.second_problem_window, text="Enter the time : ", font=("Helvetica", 15, "bold"), fg="brown")
        time_label.place(relx=0.41, rely=0.25)

        self.time_field = tk.Entry(self.second_problem_window, width=3, font=('Arial 15'))
        self.time_field.place(relx=0.54, rely=0.25)

        time_type_label = tk.Label(self.second_problem_window, text="min", font=("Helvetica", 15, "bold"))
        time_type_label.place(relx=0.58, rely=0.25)

        self.second_field = tk.Entry(self.second_problem_window, width=3, font=('Arial 15'))
        self.second_field.place(relx=0.25, rely=0.4)

        second_label = tk.Label(self.second_problem_window, text=" seconds", font=("Helvetica", 15, "bold"))
        second_label.place(relx=0.28, rely=0.4)

        self.customer_field = tk.Entry(self.second_problem_window, width=3, font=('Arial 15'))
        self.customer_field.place(relx=0.42, rely=0.4)

        customer_label = tk.Label(self.second_problem_window, text=" Customer", font=("Helvetica", 15, "bold"))
        customer_label.place(relx=0.45, rely=0.4)

        self.priority_field = tk.Entry(self.second_problem_window, width=3, font=('Arial 15'))
        self.priority_field.place(relx=0.58, rely=0.4)

        priority_label = tk.Label(self.second_problem_window, text=" Prioritized", font=("Helvetica", 15, "bold"))
        priority_label.place(relx=0.61, rely=0.4)

        start_btn = tk.Button(self.second_problem_window, text="Start", bg="#99FFFF", fg="#994C00", padx=15, pady=4, font=("Helvetica", 12, "bold"), borderwidth=5, relief="ridge", command=self.display_result)
        start_btn.place(relx=0.47, rely=0.55)

    def calculate_sources(self):
        total_time = int(self.time_field.get())
        total_seconds = total_time*60
        # print(f'seconds: {total_seconds}')
        interval = int(self.second_field.get())
        # print(f'interval: {interval}')
        customer = int(self.customer_field.get())
        # print(f'customer: {customer}')
        priority = int(self.priority_field.get())
        # print(f'priority: {priority}')
        self.total_customer = int((total_seconds/interval)*(customer+priority))
        # print(total_customer)


    def display_result(self):
        self.result_window = tk.Toplevel()
        self.result_window.state('zoomed')
        self.result_window.title("Result of Second Problem")
        title_label = tk.Label(self.result_window, text="Result of Second Problem", font=("Helvetica", 20, "bold"), fg="brown")
        title_label.place(relx=0.35, rely=0.2)

        self.calculate_sources()

        result_label_line_1 = tk.Label(self.result_window, text=f"{self.total_customer} customers come to the restaurant. customers leave from the restaurant.", font=("Helvetica", 15, "bold"))
        result_label_line_1.place(relx=0.1, rely=0.4)

        result_label_line_2 = tk.Label(self.result_window, text=f"For  customers,  tables,  waiters and  chefs, the best earnings are received.", font=("Helvetica", 15, "bold"))
        result_label_line_2.place(relx=0.1, rely=0.5)

        result_label_line_3 = tk.Label(self.result_window, text=f"The gain is ", font=("Helvetica", 15, "bold"))
        result_label_line_3.place(relx=0.1, rely=0.6)


# Creating an instance of the StartApp class and starting the application
app = StartApp()
app.run()
