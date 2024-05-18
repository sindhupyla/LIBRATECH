
import tkinter as tk
from tkinter import messagebox 
from tkinter import simpledialog
import mysql.connector
import re
from PIL import Image, ImageTk

class IntroductionPage:
    def __init__(self, master, db, cursor):
        self.master = master
        self.db = db  
        self.cursor = cursor
        master.title("Welcome to Our Application")
        master.geometry("1300x700+0+0") 
        master.resizable(False, False)
        master.iconbitmap("assets/Iconsmind-Outline-Library-2.ico")
        
    # Background image of our Introduction page
        image1 = Image.open("assets/Libratech_LOGO.png")
        image1 = image1.resize((1300, 700))
        self.background_image1 = ImageTk.PhotoImage(image1)
    # Label for our Introduction page background
        self.background_label1= tk.Label(master, image=self.background_image1)
        self.background_label1.place(x=0, y=0, relwidth=1, relheight=1)
    # Buttons --> login and sign up
        self.signup_button = tk.Button(master, text="Signup", command=self.open_signup_page,font=('Helvetica', 18))
        self.signup_button.place(x=200,y=350)
        self.login_button = tk.Button(master, text="Login", command=self.open_login_page,font=('Helvetica', 18))
        self.login_button.place(x=400,y=350)
    # Invoking signup page 
    def open_signup_page(self):
        self.master.withdraw()  # Hide the introduction page
        signup_window = tk.Toplevel(self.master)
        signup_page = SignUpPage(signup_window, self.master, self.db, self.cursor)
    #Invoking login page 
    def open_login_page(self):
        self.master.withdraw()
        login_window = tk.Toplevel(self.master)
        login_page = LoginPage(login_window)

class SignUpPage:
    def __init__(self, master, login_master, db, cursor):
        self.master = master
        self.login_master = login_master
        self.db = db
        self.cursor = cursor
        master.title("Sign Up")
        master.geometry("1300x650") 
        master.resizable(False, False)
        master.iconbitmap("assets/Iconsmind-Outline-Library-2.ico")    

        self.bg_image = tk.PhotoImage(file="assets/login2.png")
        self.bg_label = tk.Label(master, image=self.bg_image)
        self.bg_label.place(x=50, y=130)

        self.form_frame = tk.Frame(master, bg="pink", width=500, height=350)
        self.form_frame.place(x=720, y=130)

        signup_label = tk.Label(master, text=" Students Sign Up Page ", font=('Helvetica', 20))
        signup_label.place(x=550, y=50)

        self.username_label = tk.Label(self.form_frame, text="Student Name:", bg='white', font=('Helvetica', 14))
        self.username_label.place(x=50, y=50)
        self.username_entry = tk.Entry(self.form_frame, font=('Helvetica', 14))
        self.username_entry.place(x=220, y=50)

        self.reg_label = tk.Label(self.form_frame, text="Registration No:", bg='white', font=('Helvetica', 14))
        self.reg_label.place(x=50, y=100)
        self.reg_entry = tk.Entry(self.form_frame, font=('Helvetica', 14))
        self.reg_entry.place(x=220, y=100)

        self.password_label = tk.Label(self.form_frame, text="Password:", bg='white', font=('Helvetica', 14))
        self.password_label.place(x=50, y=150)
        self.password_entry = tk.Entry(self.form_frame, show="*", font=('Helvetica', 14))
        self.password_entry.place(x=220, y=150)

        self.confirm_password_label = tk.Label(self.form_frame, text="Confirm Password:", bg='white', font=('Helvetica', 14))
        self.confirm_password_label.place(x=50, y=200)
        self.confirm_password_entry = tk.Entry(self.form_frame, show="*", font=('Helvetica', 14))
        self.confirm_password_entry.place(x=225, y=200)

        self.signup_button = tk.Button(self.form_frame, text="Sign Up", command=self.signup, bg='white', font=('Helvetica', 14))
        self.signup_button.place(x=150, y=250)

        self.back_button = tk.Button(master, text="\u2190", command=self.back_to_login, bg='lightblue', font=('Helvetica',20))
        self.back_button.place(x=50, y=550)

    def signup(self):
        username = self.username_entry.get()
        reg_number = self.reg_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()


    #validation of registartion number to specify format 
        if not re.match(r'^[a-zA-Z  ]+$', username):
            messagebox.showerror("Error", "INVALID Name Format")

        elif not re.match(r'^[1-2]{1}[0-9]{1}[Bb]01[Aa][0-9]{2}[A-Za-z0-9]{1}[0-9]{1}$', reg_number):
            messagebox.showerror("Error", "Invalid Registration Number Format")

        # Check if the password meets the minimum length requirement
        elif len(password) < 6:
            messagebox.showerror("Error", "Password should be at least 6 characters long")

        # Check if the password matches the confirm password
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")

        else:
            try:
        # Inserting data into the database
                sql = "INSERT INTO userdetails.users (username, registration_number, password) VALUES (%s, %s, %s)"
                values = (username, reg_number, password)
                self.cursor.execute(sql, values)
                self.db.commit()
                messagebox.showinfo("Sign Up Successful", "User registered successfully!")
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"Failed to register user{error}")

    def back_to_login(self):
        self.master.destroy()  # Close the sign-up window
        self.login_master.deiconify()  # Show the login window


class LoginPage:
    def __init__(self, master):
        self.master = master
        master.title("Login")
        master.geometry("1300x700") 
        master.resizable(False, False)
        master.iconbitmap("assets/Iconsmind-Outline-Library-2.ico")
        image2 = Image.open("assets/loginbg.png")
        image2 = image2.resize((1300, 700))
        
        self.background_image2 = ImageTk.PhotoImage(image2)
        admin_image = Image.open("assets/admin logo.png")
        
        self.background_label2= tk.Label(master, image=self.background_image2)
        self.background_label2.place(x=0, y=0, relwidth=1, relheight=1)

        admin_login_label = tk.Label(master, text="Admin Login", font=('Helvetica', 20))
        admin_login_label.place(x=310, y=85)
        resized_admin_image = admin_image.resize((70, 60), Image.BILINEAR)
        admin_image_tk = ImageTk.PhotoImage(resized_admin_image)
        admin_image_label = tk.Label(master, image=admin_image_tk)
        admin_image_label.image = admin_image_tk
        admin_image_label.place(x=350, y=135)

        # Frame for admin login
        self.admin_frame = tk.Frame(master, bg="lightblue", width=500, height=300)
        self.admin_frame.place(x=170, y=210)

        # Admin ID
        self.admin_id_label = tk.Label(self.admin_frame, text="Admin ID:", bg='white', font=('Helvetica', 14))
        self.admin_id_label.place(x=50, y=50)
        self.admin_id_entry = tk.Entry(self.admin_frame, font=('Helvetica', 14))
        self.admin_id_entry.place(x=200, y=50)

        # Admin Password
        self.admin_password_label = tk.Label(self.admin_frame, text="Password:", bg='white', font=('Helvetica', 14))
        self.admin_password_label.place(x=50, y=100)
        self.admin_password_entry = tk.Entry(self.admin_frame, show="*", font=('Helvetica', 14))
        self.admin_password_entry.place(x=210, y=100)

        # Admin Login Button
        self.admin_login_button = tk.Button(self.admin_frame, text="Login", command=self.admin_login, bg='white', font=('Helvetica', 14))
        self.admin_login_button.place(x=150, y=150)

        
        # Database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Libratech@24",
            database="userdetails"
        )
        #Data base access
        self.cursor = self.db.cursor()

      
        student_login_label = tk.Label(master, text="Student Login", font=('Helvetica', 20))
        student_login_label.place(x=850,y=80)

        student_image = Image.open("assets/student logo.png")
        resized_student_image = student_image.resize((70,60 ), Image.BILINEAR)
        student_image_tk = ImageTk.PhotoImage(resized_student_image)
        student_image_label = tk.Label(master, image=student_image_tk)
        student_image_label.image = student_image_tk
        student_image_label.place(x=900, y=135)

        self.form_frame = tk.Frame(master, bg="pink", width=500, height=300)
        self.form_frame.place(x=700, y=210)

        self.username_label = tk.Label(self.form_frame, text="Registration No:", bg='white', font=('Helvetica', 14))
        self.username_label.place(x=50, y=50)
        self.username_entry = tk.Entry(self.form_frame, font=('Helvetica', 14))
        self.username_entry.place(x=200, y=50)

        self.password_label = tk.Label(self.form_frame, text="Password:", bg='white', font=('Helvetica', 14))
        self.password_label.place(x=50, y=100)
        self.password_entry = tk.Entry(self.form_frame, show="*", font=('Helvetica', 14))
        self.password_entry.place(x=200, y=100)

        self.login_button = tk.Button(self.form_frame, text="Login", command=self.login, bg='white', font=('Helvetica', 14))
        self.login_button.place(x=150, y=150)

        self.signup_button = tk.Button(self.form_frame, text="Sign Up", command=self.open_signup_page, bg='white', font=('Helvetica', 14))
        self.signup_button.place(x=250, y=150)

        self.back_button = tk.Button(master, text="\u2190 ", command=self.go_to_intro_page, bg='lightblue',font=('Helvetica', 20))
        self.back_button.place(x=50, y=550)
    
    def login(self):
        registration_number = self.username_entry.get()
        password = self.password_entry.get()

        # login validation
        sql = "SELECT * FROM users WHERE registration_number = %s AND password = %s"
        values = (registration_number, password)
        self.cursor.execute(sql, values)
        user = self.cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome!")
            self.username = user[1]  # Save the username for later use
            self.username_entry.delete(0, 'end') 
            self.password_entry.delete(0, 'end') 
            self.open_library_page(registration_number)  
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials of user")

    def admin_login(self):
        admin_id = self.admin_id_entry.get().lower()
        admin_password = self.admin_password_entry.get()

        # Check if the admin credentials are correct(static)
        if admin_id == "librarian" and admin_password == "svecw":
            messagebox.showinfo("Admin Login Successful", "Welcome Admin!")
            self.admin_id_entry.delete(0, 'end')  # Clear admin ID entry
            self.admin_password_entry.delete(0, 'end') 
            self.open_admin_page()
        else:
            messagebox.showerror("Admin Login Failed", "Invalid Admin Credentials")
    def open_signup_page(self):
        self.master.withdraw()  
        signup_window = tk.Toplevel(self.master)
        signup_page = SignUpPage(signup_window, self.master, self.db, self.cursor)

    def open_library_page(self, registration_number):
        self.master.withdraw() 
        library_window = tk.Toplevel(self.master)
        library_page = LibraryPage(library_window, self.master, self.db, self.cursor, registration_number)
         
    def open_admin_page(self):
        self.master.withdraw()  
        admin_window = tk.Toplevel(self.master)
        admin_page = AdminPage(admin_window,self.master, self.db, self.cursor)
          
        self.db.reconnect()
        self.cursor = self.db.cursor()
        self.cursor_reserved_books = self.db.cursor()

    def go_to_intro_page(self):
        self.master.withdraw() 
        intro_window = tk.Toplevel(self.master)
        intro_page = IntroductionPage(intro_window,self.db,self.cursor) 

class LibraryPage:
    def __init__(self, master, login_master, db, cursor, registration_number):
        self.master = master
        self.login_master = login_master
        self.db = db
        self.cursor = cursor
        self.regdno = registration_number
        self.profile_visible = False
        master.iconbitmap("assets/Iconsmind-Outline-Library-2.ico")
        master.geometry("1300x700+0+0")
        master.resizable(False, False)

        master.title("Library")
        image = Image.open("assets/bookbg.png")
        image = image.resize((1300, 700))
        self.background_image = ImageTk.PhotoImage(image)
        
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.profile_image = Image.open("assets/Userlogo.png")
        self.profile_image = self.profile_image.resize((50, 50))  # Resize the image
        self.profile_image = ImageTk.PhotoImage(self.profile_image)
        self.profile_button = tk.Button(master, image=self.profile_image, command=self.show_profile_frame)
        self.profile_button.place(x=1200, y=30)

        self.label_book_name = tk.Label(master, text="Enter Book Name:", font=("Helvetica", 15), bg="gold")
        self.label_book_name.place(x=450, y=150)
        self.entry_book_name = tk.Entry(master, font=("Helvetica", 15))
        self.entry_book_name.place(x=650, y=150)

        self.check_button = tk.Button(master, text="Check Availability", command=self.check_availability, font=("Helvetica", 15))
        self.check_button.place(x=550, y=220)

        
        # database connections
        self.db_availablebooks = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="Libratech@24",  
            database="availablebooks"
        )
        self.cursor_availablebooks = self.db_availablebooks.cursor()

        self.db_books_dataset = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="Libratech@24",  
            database="books_dataset"
        )
        self.cursor_books_dataset = self.db_books_dataset.cursor()

        # Initialize database connection for requested_books
        self.db_reserved_books = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="Libratech@24",  
            database="reserved_books"
        )
        self.cursor_reserved_books = self.db_reserved_books.cursor()

        # Destroy reserved_books database connection when the window is closed as that database being updated
        master.protocol("DELETE WINDOW", self.close_connection)
        

    def check_availability(self):
        book = self.entry_book_name.get().lower()

        # Check if the book exists in availablebooks
        sql_availablebooks = "SELECT * FROM availablebooks WHERE LOWER(book) = %s"
        self.cursor_availablebooks.execute(sql_availablebooks, (book,))
        result_availablebooks = self.cursor_availablebooks.fetchone()

        # Check if the result_availablebooks is None
        if result_availablebooks is not None:
            messagebox.showinfo("Book Availability", "Book is available.")
        else:
            # Check if the book exists in books_dataset
            sql_books_dataset = "SELECT * FROM books_dataset WHERE LOWER(book) = %s"
            self.cursor_books_dataset.execute(sql_books_dataset, (book,))
            result_books_dataset = self.cursor_books_dataset.fetchone()

            if result_books_dataset:
                choice = messagebox.askyesno("Book Availability", "Book not currently available. Would you like to request it?")
                if choice:
                    self.request_book(book)  # Call request_book if user chooses to request the book
                else:
                    messagebox.showinfo("Request Status", "BOOK not requested.")
            else:
                messagebox.showinfo("Book Availability", "Book does not exist.")
    def view_requests(self):
        try:
            # Fetch requests made by the user with the given registration number
            sql = "SELECT * FROM reserved_books.reserved_books WHERE regdno = %s"
            self.cursor_reserved_books.execute(sql, (self.regdno,))
            requests = self.cursor_reserved_books.fetchall()

            # Display requests in a message box
            if requests:
                request_details = "\n".join([f"Book: {row[1]}, Author: {row[2]}" for row in requests])
                messagebox.showinfo("My Requests", f"Your requests:\n{request_details}")
            else:
                messagebox.showinfo("My Requests", "You have not made any requests yet.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to fetch requests: {error}")



    def request_book(self, book):
        db_reserved_books = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Libratech@24",
            database="reserved_books"
        )
        cursor_reserved_books = db_reserved_books.cursor()

        # Retrieve author name from the books_dataset
        sql_get_author = "SELECT author FROM books_dataset WHERE LOWER(book) = %s"
        self.cursor_books_dataset.execute(sql_get_author, (book,))
        author_result = self.cursor_books_dataset.fetchone()

        if author_result:
            author = author_result[0]
            try:
                # Ensure that the 'regd_no' column exists in the 'reserved_books' table
                cursor_reserved_books.execute("DESCRIBE reserved_books")
                columns = cursor_reserved_books.fetchall()
                column_names = [column[0] for column in columns]

                # Insert the user's registration number along with the book details into the reserved_books table
                sql_insert_reserved = "INSERT INTO reserved_books (regdno, book, author) VALUES (%s, %s, %s)"
                values = (self.regdno, book, author)
                cursor_reserved_books.execute(sql_insert_reserved, values)
                db_reserved_books.commit()
                messagebox.showinfo("Request Status", f"Your request for '{book}' has been sent. Please login back within two days to check for its availability")
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"Failed to request book: {error}")
        else:
            messagebox.showerror("Error", f"Author information not found for '{book}'. Cannot request the book.")
        if not self.regdno:
            messagebox.showerror("Error", "Registration number not available. Please login.")
            return
        # Close the connection to the reserved_books database
        cursor_reserved_books.close()
        db_reserved_books.close()

    # Show profile frame and fetch user details
    def show_profile_frame(self):
        # Destroy existing profile frame if any
        if hasattr(self, 'profile_frame'):
            self.profile_frame.destroy()

        # Create a new profile frame
        self.profile_frame = tk.Frame(self.master, bg="white", width=300, height=300)
        self.profile_frame.place(x=1000, y=100)

        # Fetch user details using registration_number
        sql = "SELECT username, registration_number FROM users WHERE registration_number = %s"
        self.cursor.execute(sql, (self.regdno,))
        user_details = self.cursor.fetchone()

        if user_details:
            username, registration_number = user_details
            details_text = f"Username: {username}\nRegistration Number: {registration_number}"

            # Display user details
            self.user_details_label = tk.Label(self.profile_frame, text=details_text, font=('Helvetica', 12), bg='white')
            self.user_details_label.pack()
            
            self.my_requests_button = tk.Button(self.profile_frame, text="My Requests", command=self.view_requests, font=('Helvetica', 12))
            self.my_requests_button.pack()
            # Show the logout button
            self.logout_button = tk.Button(self.profile_frame, text="Logout", command=self.go_back_to_login, font=("Helvetica", 12))
            self.logout_button.pack()

        else:
            messagebox.showinfo("User Details", "User details not found.")
        if self.profile_visible:
            # If profile frame is visible, hide it
            self.profile_frame.place_forget()
            self.profile_visible = False
        else:
            # If profile frame is not visible, show it and fetch user details
            self.profile_frame.place(x=1000, y=100)
            self.fetch_user_details()
            self.profile_visible = True
    
    def fetch_user_details(self):
        # Fetch user details using registration number
        sql = "SELECT username, registration_number FROM users WHERE registration_number = %s"
        self.cursor.execute(sql, (self.regdno,))
        user_details = self.cursor.fetchone()

        if user_details:
            username, registration_number = user_details
            details_text = f"Username: {username}\nRegistration Number: {registration_number}"
            self.user_details_label.config(text=details_text)
        else:
            messagebox.showinfo("User Details", "User details not found.")
    def close_connection(self):
        # Close the connection to the reserved_books database
        self.cursor_reserved_books.close()
        self.db_reserved_books.close()
        self.master.destroy()
    def go_back_to_login(self):
    # Close the library window
        self.master.destroy()  
        # Show the login window
        self.login_master.deiconify() 
    
class AdminPage:
    def __init__(self, master, login_master,db, cursor):
        self.master = master
        self.db = db
        self.cursor = cursor
        self.login_master=login_master
        self.db_reserved_books = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="Libratech@24",  
            database="reserved_books"
        )
        self.cursor_reserved_books = self.db_reserved_books.cursor()

        master.title("Admin Page")
        master.geometry("1300x650")
        master.iconbitmap("assets/Iconsmind-Outline-Library-2.ico")
        master.resizable(False, False)

        image = Image.open("assets/admin3.png")
        image = image.resize((1350,650))
        
        self.background_image = ImageTk.PhotoImage(image)
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Define button styles
        button_style = {
            "font": ("Helvetica", 12),
            "bg": "lightblue",
            "fg": "black",
            "width": 20,
            "height": 2,
            "bd": 0,
        }

        # Button to update available books
        self.update_books_button = tk.Button(master, text="Update Available Books", command=self.update_available_books, **button_style)
        self.update_books_button.place(x=300, y=120)

        self.update_dataset_button = tk.Button(master, text="Update Dataset Books", command=self.update_books_dataset, **button_style)
        self.update_dataset_button.place(x=300, y=180)

        self.show_requests_button = tk.Button(master, text="Show Requests", command=self.show_requests, **button_style)
        self.show_requests_button.place(x=300, y=240)

        self.back_button = tk.Button(master, text="\u2190", command=self.back_to_login, bg='lightblue', font=('Helvetica',20))
        self.back_button.place(x=50, y=550)

    def update_available_books(self):
        book_info = self.prompt_input("Enter Book and Author Name (separated by comma):")
        if book_info:
            book_name, author_name = book_info.split(',')
            self.insert_into_available_books(book_name.strip(), author_name.strip())

    def insert_into_available_books(self, book_name, author_name):
        try:
            sql = "INSERT INTO availablebooks.availablebooks (book, author) VALUES (%s, %s)"
            values = (book_name, author_name)
            self.cursor.execute(sql, values)
            self.db.commit()
            
        except mysql.connector.Error as err:
            print("Error:", err)

    def update_books_dataset(self):
        book_info = self.prompt_input("Enter Book Details (Book, Author):")
        if book_info:
            book, author = book_info.split(',')
            self.insert_into_books_dataset(book.strip(), author.strip())

    def insert_into_books_dataset(self, book_name, author_name):
        try:
            sql = "INSERT INTO books_dataset.books_dataset (book, author) VALUES (%s, %s)"
            values = (book_name, author_name)
            self.cursor.execute(sql, values)
            self.db.commit()
          
        except mysql.connector.Error as err:
            print("Error:", err)

    def prompt_input(self, prompt):
        book_info = simpledialog.askstring("Input", prompt)
        return book_info

    def show_requests(self):

        try:
            # Fetch reserved books data
            reserved_books_data = self.refresh_reserved_books()
            self.cursor_reserved_books.execute("SELECT * FROM reserved_books.reserved_books")
            reserved_books_data = self.cursor_reserved_books.fetchall()
            # Create a new tkinter window to display requests
            requests_window = tk.Toplevel(self.master)
            requests_page = RequestsPage(requests_window, reserved_books_data)
                
        except mysql.connector.Error as err:
            # Handle any errors that occur during database query
            messagebox.showerror("Error", f"An error occurred: {err}")

    def refresh_reserved_books(self):
        try:
            # Execute a query to fetch all records from the reserved books table
            self.cursor.execute("SELECT * FROM reserved_books.reserved_books")
            
            # Fetch all rows from the result set
            reserved_books_data = self.cursor.fetchall()
            
            return reserved_books_data

        except mysql.connector.Error as error:
            print("Error refreshing reserved books:", error)

    def back_to_login(self):
        # Close the current admin page window
        self.master.destroy()
        self.login_master.deiconify() 

class RequestsPage:
    def __init__(self, master, reserved_books_data):
        self.master = master
        self.reserved_books_data = reserved_books_data

        master.title("Requests")
        master.geometry("1300x700")  # Initial size of the window
        master.resizable(False, False)
        master.iconbitmap("assets/Iconsmind-Outline-Library-2.ico")
        
        self.back_button = tk.Button(master, text="\u2190", command=self.go_back, bg='lightblue', font=('Helvetica',20))
        self.back_button.place(x=50, y=550)

        # Create a frame to contain the requests
        self.frame = tk.Frame(master)
        self.frame.pack()
        image = Image.open("assets/admin3.png")
        image = image.resize((1350,650))
        
       
        # Display requests
        self.display_requests()


    def display_requests(self):
        # Display each request in a single line with a "Done" button
        for request in self.reserved_books_data:
            request_frame = tk.Frame(self.frame)
            request_frame.pack(pady=7, fill="x")
           
            # Display request information (registration number, book, author) in a single line
            request_info = f"Registration Number: {request[0]}, Book: {request[1]}, Author: {request[2]}"
            request_label = tk.Label(request_frame, text=request_info)
            request_label.pack(side="left")
            # Create "Done" button for each request
            done_button = tk.Button(request_frame, text="Available", command=lambda req=request: self.mark_as_done(req))
            done_button.pack(side="right")

    def mark_as_done(self, request):
        try:
            # Connect to the database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Libratech@24",
                database="reserved_books")
            cursor = db.cursor()

            # Delete the row from the database
            sql = "DELETE FROM reserved_books.reserved_books WHERE regdno = %s AND book = %s AND author = %s"
            values = (request[0], request[1], request[2])
            cursor.execute(sql, values)
            db.commit()
            
            # Update available_books database
            self.update_available_books(request[1], request[2])

            # Close the database connection
            cursor.close()
            db.close()

            # Remove the request from GUI
            self.remove_request_from_gui(request)

            library_page = self.master.library_page
            library_page.notify_user(request[0], request[1])


        except mysql.connector.Error as error:
            print("Error:", error)

    def update_available_books(self, book, author):
        try:
            # Connect to the database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Libratech@24",
                database="availablebooks")
            cursor = db.cursor()

            # Insert the book and author into available_books
            sql = "INSERT INTO availablebooks.availablebooks (book, author) VALUES (%s, %s)"
            values = (book, author)
            cursor.execute(sql, values)
            db.commit()

            # Close the database connection
            cursor.close()
            db.close()

        except mysql.connector.Error as error:
            print("Error:", error)

    def remove_request_from_gui(self, request):
        # Remove the request from GUI
        for widget in self.frame.winfo_children():
            request_info = f"Registration Number: {request[0]}, Book: {request[1]}, Author: {request[2]}"
            if widget.winfo_class() == "Frame" and widget.winfo_children()[0]["text"] == request_info:
                widget.destroy()
                break
    def go_back(self):
        # Destroy the current requests page window and deiconify the admin page window
        self.master.destroy()
        self.admin_page.master.deiconify()

def main():
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Libratech@24",
    )
    root = tk.Tk() 
    
    root.geometry("1300x700")
    root.resizable(False, False)
    cursor = db.cursor()
    app = IntroductionPage(root, db, cursor) 
    root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    main()

