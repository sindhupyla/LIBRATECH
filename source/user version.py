
import tkinter as tk
from tkinter import messagebox

import mysql.connector
import re
from PIL import Image, ImageTk

class LoginPage:
    def __init__(self, master):
        self.master = master
        master.title("Login")
        master.geometry("1300x650")  # Initial size of the window
        master.resizable(False, False)
        master.iconbitmap("assets/Iconsmind-Outline-Library-2.ico")

        # Background Image
        self.bg_image = tk.PhotoImage(file="assets/Screenshot 2024-02-26 203510.png")
        self.canvas = tk.Canvas(master, width=1300, height=650)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        self.canvas.place(x=50, y=50)

        # Database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Libratech@24",
            database="userdetails"
        )
        self.cursor = self.db.cursor()

        # Frame for labels, textboxes, and buttons
        self.form_frame = tk.Frame(master, bg="pink", width=500, height=300)
        self.form_frame.place(x=700, y=150)
        # Username/Registration Number
        self.username_label = tk.Label(self.form_frame, text="Registration No:", bg='white', font=('Helvetica', 14))
        self.username_label.place(x=50, y=50)
        self.username_entry = tk.Entry(self.form_frame, font=('Helvetica', 14))
        self.username_entry.place(x=200, y=50)

        # Password
        self.password_label = tk.Label(self.form_frame, text="Password:", bg='white', font=('Helvetica', 14))
        self.password_label.place(x=50, y=100)
        self.password_entry = tk.Entry(self.form_frame, show="*", font=('Helvetica', 14))
        self.password_entry.place(x=200, y=100)

        # Login Button
        self.login_button = tk.Button(self.form_frame, text="Login", command=self.login, bg='white', font=('Helvetica', 14))
        self.login_button.place(x=150, y=150)

        # Sign Up Button
        self.signup_button = tk.Button(self.form_frame, text="Sign Up", command=self.open_signup_page, bg='white', font=('Helvetica', 14))
        self.signup_button.place(x=250, y=150)

    def login(self):
        registration_number = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the user exists in the database
        sql = "SELECT * FROM users WHERE registration_number = %s AND password = %s"
        values = (registration_number, password)
        self.cursor.execute(sql, values)
        user = self.cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome!")
            self.username = user[1]  # Save the username for later use
            self.open_library_page()
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials of user")

    def open_signup_page(self):
        self.master.withdraw()  
        signup_window = tk.Toplevel(self.master)
        signup_page = SignUpPage(signup_window, self.master, self.db, self.cursor)

    
    def open_library_page(self):
        registration_number = self.username_entry.get()  # Retrieve registration number from the login page
        self.master.withdraw()  # Hide the login window
        library_window = tk.Toplevel(self.master)
        library_page = LibraryPage(library_window, self.master, self.db, self.cursor, registration_number)  

class SignUpPage:
    def __init__(self, master, login_master, db, cursor):
        self.master = master
        self.login_master = login_master
        self.db = db
        self.cursor = cursor
        master.title("Sign Up")
        master.geometry("1300x650")  # Initial size of the window
        master.resizable(False, False)
        master.iconbitmap("assets/Iconsmind-Outline-Library-2.ico")

        # Background Image
        self.bg_image = tk.PhotoImage(file="assets/Screenshot 2024-02-26 203510.png")
        self.canvas = tk.Canvas(master, width=1300, height=650)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        self.canvas.place(x=50, y=50)

        # Frame for labels, textboxes, and buttons
        self.form_frame = tk.Frame(master, bg="pink", width=500, height=300)
        self.form_frame.place(x=700, y=150)

        # Username
        self.username_label = tk.Label(self.form_frame, text="Username:", bg='white', font=('Helvetica', 14))
        self.username_label.place(x=50, y=50)
        self.username_entry = tk.Entry(self.form_frame, font=('Helvetica', 14))
        self.username_entry.place(x=200, y=50)

        # Registration Number
        self.reg_label = tk.Label(self.form_frame, text="Registration No", bg='white', font=('Helvetica', 14))
        self.reg_label.place(x=50, y=100)
        self.reg_entry = tk.Entry(self.form_frame, font=('Helvetica', 14))
        self.reg_entry.place(x=200, y=100)

        # Password
        self.password_label = tk.Label(self.form_frame, text="Password:", bg='white', font=('Helvetica', 14))
        self.password_label.place(x=50, y=150)
        self.password_entry = tk.Entry(self.form_frame, show="*", font=('Helvetica', 14))
        self.password_entry.place(x=200, y=150)

        # Sign Up Button
        self.signup_button = tk.Button(self.form_frame, text="Sign Up", command=self.signup, bg='white', font=('Helvetica', 14))
        self.signup_button.place(x=150, y=200)

        # Back to Login Button
        self.back_button = tk.Button(self.form_frame, text="Back to Login", command=self.back_to_login, bg='white', font=('Helvetica', 14))
        self.back_button.place(x=250, y=200)

    def signup(self):
        username = self.username_entry.get()
        reg_number = self.reg_entry.get()
        password = self.password_entry.get()

        # Check if the registration number matches the format
        if not re.match(r'^[1-2]{1}[0-9]{1}[Bb]01[Aa][0-9]{2}[A-Za-z0-9]{1}[0-9]{1}$', reg_number):
            messagebox.showerror("Error", "INVALID FORMAT")

        # Check if the password meets minimum length requirement
        elif len(password) < 6:
            messagebox.showerror("Error", "Password should be minimum of 6 digits")

        else:
            try:
                # Inserting data into the database
                sql = "INSERT INTO users (username, registration_number, password) VALUES (%s, %s, %s)"
                values = (username, reg_number, password)
                self.cursor.execute(sql, values)
                self.db.commit()
                messagebox.showinfo("Sign Up Successful", "User registered successfully!")
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"Failed to register user")

    def back_to_login(self):
        self.master.destroy()  # Close the sign-up window
        self.login_master.deiconify()  # Show the login window

class LibraryPage:
    def __init__(self, master, login_master, db, cursor, registration_number):
        self.master = master
        self.login_master = login_master
        self.db = db
        self.cursor = cursor
        self.regdno = registration_number
        master.title("Library")
        master.geometry("1300x650")
        master.iconbitmap("assets/Iconsmind-Outline-Library-2.ico")

        

        # Open and resize the image
        image = Image.open("assets/book1.png")
        image = image.resize((1300,650))
        self.background_image = ImageTk.PhotoImage(image)
    
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.profile_image = Image.open("assets/Userlogo.png")
        self.profile_image = self.profile_image.resize((50, 50), Image.BILINEAR)  # Resize the image
        self.profile_image = ImageTk.PhotoImage(self.profile_image)
        self.profile_label = tk.Label(master, image=self.profile_image)
        self.profile_label.place(x=1200, y=30)
        self.profile_label.bind("<Button-1>", self.display_user_details)  # Bind click event


        # Label and Entry for Book Name
        self.label_book_name = tk.Label(master, text="Enter Book Name:", font=("Helvetica", 15), bg="gold")
        self.label_book_name.place(x=450, y=150)
        self.entry_book_name = tk.Entry(master, font=("Helvetica", 15))
        self.entry_book_name.place(x=650, y=150)

        # Check Availability Button
        self.check_button = tk.Button(master, text="Check Availability", command=self.check_availability, font=("Helvetica", 15))
        self.check_button.place(x=550, y=220)

        
        # Initialize database connections for availablebooks and books_dataset
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

        # Initialize database connection for reserved_books
        self.db_reserved_books = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="Libratech@24",  
            database="reserved_books"
        )
        self.cursor_reserved_books = self.db_reserved_books.cursor()

        # Destroy reserved_books database connection when the window is closed
        master.protocol("WM_DELETE_WINDOW", self.close_connection)

    def display_user_details(self):
    # Fetch user details using registration_number
        sql = "SELECT username, registration_number FROM users WHERE registration_number = %s"
        self.cursor.execute(sql, (self.regdno,))
        user_details = self.cursor.fetchone()

        if user_details:
            username, registration_number = user_details
            details_text = f"Username: {username}\nRegistration Number: {registration_number}"

            # Calculate the width of the text to adjust the x-coordinate
            text_width = len(max(details_text.split('\n'), key=len)) * 7  # Adjust the factor as needed

            # Place the label in the top right corner
            user_details_label = tk.Label(self.master, text=details_text, font=('Helvetica', 12), bg='white')
            user_details_label.place(x=self.master.winfo_width() - text_width - 20, y=10)  # Adjust the padding as needed
        else:
            messagebox.showinfo("User Details", "User details not found.")

    def view_history(self):
        # Add your view history functionality here
        pass

    def close_connection(self):
        # Close the connection to the reserved_books database
        self.cursor_reserved_books.close()
        self.db_reserved_books.close()
        self.master.destroy()


    def check_availability(self):
        book = self.entry_book_name.get().lower()  

        # Check if the book exists in availablebooks
        sql_availablebooks = "SELECT * FROM availablebooks WHERE LOWER(book) = %s"
        self.cursor_availablebooks.execute(sql_availablebooks, (book,))
        result_availablebooks = self.cursor_availablebooks.fetchone()

        # Check if the book exists in books_dataset
        sql_books_dataset = "SELECT * FROM books_dataset WHERE LOWER(book) = %s"
        self.cursor_books_dataset.execute(sql_books_dataset, (book,))
        result_books_dataset = self.cursor_books_dataset.fetchone()

        if result_availablebooks:
            messagebox.showinfo("Book Availability", "Book is available.")
        elif result_books_dataset:
            choice = messagebox.askyesno("Book Availability", "Book not currently available. Would you like to request it?")
            if choice:
                self.request_book(book)  # Call request_book if user chooses to request the book
            else:
                messagebox.showinfo("Request Status", "BOOK not requested.")
        else:
            messagebox.showinfo("Book Availability", "Book does not exist.")

    def request_book(self, book):
    # Initialize database connection for reserved_books
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
                messagebox.showinfo("Request Status", f"Your request for '{book}' has been sent. Book registered successfully!")
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
    
    # Fetch user details using registration_number
    def display_user_details(self,_=None):
    # Fetch user details using registration_number
        sql = "SELECT username, registration_number FROM users WHERE registration_number = %s"
        self.cursor.execute(sql, (self.regdno,))
        user_details = self.cursor.fetchone()

        if user_details:
            username, registration_number = user_details
            details_text = f"Username: {username}\nRegistration Number: {registration_number}"

            # Calculate the width of the text to adjust the x-coordinate
            text_width = len(max(details_text.split('\n'), key=len)) * 8  # Adjust the factor as needed

            # Place the label in the top right corner
            user_details_label = tk.Label(self.master, text=details_text, font=('Helvetica', 12), bg='white')
            user_details_label.place(x=1000, y=100)  # Adjust the padding as needed
        else:
            messagebox.showinfo("User Details", "User details not found.")
    



def main():
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
