import tkinter
#import python ,tkinter, mysql and other libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error, IntegrityError
from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as ctk
from datetime import datetime, timedelta
from customtkinter import CTkImage
from tkinter import ttk
from tkinter import simpledialog  
from tkcalendar import Calendar 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF
import mysql.connector


# Connect to MySQL Server
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123"
)
cursor = db_connection.cursor()

# Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS Vehicle_Service_DB")
print("Database 'Vehicle_Service_DB' created or already exists.")
cursor.close()
db_connection.close()

# Reconnect to the newly created database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="Vehicle_Service_DB"
)
cursor = db_connection.cursor()

# Function to check if a table exists
def table_exists(table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None

# Dictionary of tables and their respective creation queries
# Dictionary of tables and their respective creation queries
# Dictionary of tables and their respective creation queries
# Dictionary of tables and their respective creation queries
tables = {
    "Roles": """
    CREATE TABLE IF NOT EXISTS Roles (
        roleid INT PRIMARY KEY AUTO_INCREMENT,
        rolename ENUM('user', 'mechanic', 'admin') NOT NULL UNIQUE
    )""",

    "User": """
    CREATE TABLE IF NOT EXISTS User (
        userid INT PRIMARY KEY AUTO_INCREMENT,
        firstname VARCHAR(100) NOT NULL,
        lastname VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        phoneno VARCHAR(15),
        address1 VARCHAR(255),
        city VARCHAR(100),
        state VARCHAR(100),
        zipcode VARCHAR(10),
        roleid INT NOT NULL,
        FOREIGN KEY (roleid) REFERENCES Roles(roleid) ON DELETE CASCADE ON UPDATE CASCADE
    )""",

    "Services": """
    CREATE TABLE IF NOT EXISTS Services (
        serviceid INT PRIMARY KEY AUTO_INCREMENT,
        servicename VARCHAR(255) NOT NULL,
        typeofvehicle VARCHAR(50) NOT NULL
    )""",

    "Mechanics": """
    CREATE TABLE IF NOT EXISTS Mechanics (
        mechid INT PRIMARY KEY AUTO_INCREMENT,
        serviceid INT NOT NULL,
        userid INT NOT NULL,  -- Linking mechanics to the user table
        FOREIGN KEY (userid) REFERENCES User(userid) ON DELETE CASCADE,
        firstname VARCHAR(100) NOT NULL,
        lastname VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        phoneno VARCHAR(15),
        address1 VARCHAR(255),
        city VARCHAR(100),
        state VARCHAR(100),
        zipcode VARCHAR(10),
        approval_status ENUM('Pending', 'Approved', 'Rejected') NOT NULL DEFAULT 'Pending',
        FOREIGN KEY (serviceid) REFERENCES Services(serviceid) ON DELETE CASCADE
    )""",

    "Mechanic_Businesses": """
    CREATE TABLE IF NOT EXISTS Mechanic_Businesses (
        business_id INT PRIMARY KEY AUTO_INCREMENT,
        mechid INT NOT NULL,
        business_name VARCHAR(255) NOT NULL,
        service_id INT NOT NULL,
        zip_code VARCHAR(10) NOT NULL,
        service_type VARCHAR(255) NOT NULL,
        vehicle_type VARCHAR(255) NOT NULL,
        approval_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
        FOREIGN KEY (mechid) REFERENCES Mechanics(mechid) ON DELETE CASCADE,
        FOREIGN KEY (service_id) REFERENCES Services(serviceid) ON DELETE CASCADE
    )""",

    "Appointments": """
    CREATE TABLE IF NOT EXISTS Appointments (
        appointmentid INT PRIMARY KEY AUTO_INCREMENT,
        userid INT NOT NULL,
        mechid INT NOT NULL,
        appointmentdate DATE NOT NULL,
        appointmenttime TIME NOT NULL,
        status ENUM('Pending', 'In Progress', 'Completed') NOT NULL,
        typeofvehicle VARCHAR(50) NOT NULL,
        FOREIGN KEY (userid) REFERENCES User(userid) ON DELETE CASCADE,
        FOREIGN KEY (mechid) REFERENCES Mechanics(mechid) ON DELETE CASCADE
    )""",
}



# Create tables if they do not exist
for table_name, create_query in tables.items():
    if not table_exists(table_name):
        cursor.execute(create_query)
        print(f"Table '{table_name}' created successfully.")
    else:
        print(f"Table '{table_name}' already exists, skipping creation.")

# Commit and close connection
db_connection.commit()
cursor.close()
db_connection.close()

print("Database setup completed successfully!")

# Insert predefined roles if they don't exist
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="Vehicle_Service_DB"
)
cursor = db_connection.cursor()

cursor.execute("INSERT IGNORE INTO Roles (roleid, rolename) VALUES (1, 'user'), (2, 'mechanic'), (3, 'admin')")
db_connection.commit()
cursor.close()
db_connection.close()



ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class VehicleServiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Vehicle Service & Maintenance Management System")
        self.geometry("1200x750")
        self.resizable(False, False)
        self.login_screen()

    def login_screen(self):

        for widget in self.winfo_children():
            widget.destroy()
        
        # Add image to the login screen
        self.bg_image = Image.open("UI/login_screen.png")
        self.bg_image = self.bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # UI Container (Login Box)
        self.frame = ctk.CTkFrame(self, width=350, height=450, corner_radius=10, fg_color="#D3D3D3")
        self.frame.place(relx=0.8, rely=0.5, anchor="center")  # Moved to the right

        # Login/Register Label
        self.title_label = ctk.CTkLabel(self.frame, text="Login", font=("Arial", 18, "bold"))
        self.title_label.place(relx=0.5, rely=0.1, anchor="center")

        # Username/Email Label
        self.username_label = ctk.CTkLabel(self.frame, text="Username/Business ID", font=("Arial", 14, "bold"))
        self.username_label.place(relx=0.15, rely=0.2)  # Adjusted to the left
        # Username/Email Entry
        self.username_entry = ctk.CTkEntry(self.frame, width=250, height=35)
        self.username_entry.place(relx=0.5, rely=0.3, anchor="center")  # Adjusted to the left

        # Password Label
        self.password_label = ctk.CTkLabel(self.frame, text="Password", font=("Arial", 14, "bold"))
        self.password_label.place(relx=0.15, rely=0.4)  # Adjusted to the left
        # Password Entry
        self.password_entry = ctk.CTkEntry(self.frame, width=250, height=35, show="*")
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")  # Adjusted to the left

        # Forgot Password Link
        self.forgot_password_label = ctk.CTkLabel(self.frame, text="Forgot Password?", font=("Arial", 12), cursor="hand2")
        self.forgot_password_label.place(relx=0.5, rely=0.6, anchor="center")  # Adjusted to the left

        # Login Button
        self.login_button = ctk.CTkButton(self.frame, text="Login", width=200, height=40, font=("Arial", 14, "bold"), command=self.login_authenticate)
        self.login_button.place(relx=0.55, rely=0.75, anchor="center")  # Adjusted to the right

        # Register Button
        self.register_button = ctk.CTkButton(self.frame, text="Register", width=200, height=40, font=("Arial", 14, "bold"), fg_color="#FFFFFF", text_color="#000000", command=self.registration_screen)
        self.register_button.place(relx=0.55, rely=0.9, anchor="center")  # Adjusted to the right

    def login_authenticate(self):
        email = self.username_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter email and password!")
            return

        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        cursor.execute("SELECT userid, roleid FROM User WHERE email = %s AND password = %s", (email, password))
        result = cursor.fetchone()

        if result:
            self.user_id = result[0]
            roleid = result[1]

            if roleid == 1:
                self.user_dashboard(email)
            elif roleid == 2:
                self.mechanic_dashboard()
            elif roleid == 3:
                self.admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

        cursor.close()
        db_connection.close()



    def admin_dashboard(self):
        # Destroy previous UI components
        for widget in self.winfo_children():
            widget.destroy()

        # UI Container (Admin Dashboard Box)
        self.frame = ctk.CTkFrame(self, width=900, height=450, corner_radius=10, fg_color="#D3D3D3")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Dashboard Title
        self.title_label = ctk.CTkLabel(self.frame, text="Welcome Admin", font=("Arial", 20, "bold"))
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Add more admin functionalities here

        # Logout Button
        self.logout_button = ctk.CTkButton(self, text="Logout", width=100, command=self.logout)
        self.logout_button.place(relx=0.9, rely=0.95, anchor="center")

    def registration_screen(self):
        # Destroy old frame if it exists
        for widget in self.winfo_children():
            widget.destroy()

        #add image to the registration screen
        self.bg_image = Image.open("UI/RegisterationFrame.jpg")
        self.bg_image = self.bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # UI Container (Registration Box)
        self.frame = ctk.CTkFrame(self, width=1100, height=450, corner_radius=10, fg_color="#D3D3D3")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Registration Label
        self.title_label = ctk.CTkLabel(self.frame, text="Registration", font=("Arial", 20, "bold"))
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # User Details
        self.fname_label = ctk.CTkLabel(self.frame, text="First Name", font=("Arial", 14))
        self.fname_label.place(relx=0.05, rely=0.15)
        self.fname_entry = ctk.CTkEntry(self.frame, width=250)
        self.fname_entry.place(relx=0.2, rely=0.15)

        self.lname_label = ctk.CTkLabel(self.frame, text="Last Name", font=("Arial", 14))
        self.lname_label.place(relx=0.05, rely=0.25)
        self.lname_entry = ctk.CTkEntry(self.frame, width=250)
        self.lname_entry.place(relx=0.2, rely=0.25)

        self.email_label = ctk.CTkLabel(self.frame, text="Email", font=("Arial", 14))
        self.email_label.place(relx=0.05, rely=0.35)
        self.email_entry = ctk.CTkEntry(self.frame, width=250)
        self.email_entry.place(relx=0.2, rely=0.35)

        self.phone_label = ctk.CTkLabel(self.frame, text="Phone No.", font=("Arial", 14))
        self.phone_label.place(relx=0.05, rely=0.45)
        self.phone_entry = ctk.CTkEntry(self.frame, width=250)
        self.phone_entry.place(relx=0.2, rely=0.45)

        self.password_label = ctk.CTkLabel(self.frame, text="Password", font=("Arial", 14))
        self.password_label.place(relx=0.05, rely=0.55)
        self.password_entry = ctk.CTkEntry(self.frame, width=250, show="*")
        self.password_entry.place(relx=0.2, rely=0.55)

        self.confirm_password_label = ctk.CTkLabel(self.frame, text="Confirm Password", font=("Arial", 14))
        self.confirm_password_label.place(relx=0.05, rely=0.65)
        self.confirm_password_entry = ctk.CTkEntry(self.frame, width=250, show="*")
        self.confirm_password_entry.place(relx=0.2, rely=0.65)

        # Mechanic Selection
        self.mechanic_label = ctk.CTkLabel(self.frame, text="Are you a Mechanic?", font=("Arial", 14))
        self.mechanic_label.place(relx=0.55, rely=0.15)
        self.mechanic_check = ctk.CTkCheckBox(self.frame, text="Yes", command=self.toggle_mechanic_fields)
        self.mechanic_check.place(relx=0.75, rely=0.15)

        # Address Fields
        self.address_label = ctk.CTkLabel(self.frame, text="User/Business Address", font=("Arial", 14))
        self.address_label.place(relx=0.55, rely=0.25)
        self.address_entry = ctk.CTkEntry(self.frame, width=250)
        self.address_entry.place(relx=0.75, rely=0.25)

        self.city_label = ctk.CTkLabel(self.frame, text="City", font=("Arial", 14))
        self.city_label.place(relx=0.55, rely=0.35)
        self.city_entry = ctk.CTkEntry(self.frame, width=250)
        self.city_entry.place(relx=0.75, rely=0.35)

        self.state_label = ctk.CTkLabel(self.frame, text="State", font=("Arial", 14))
        self.state_label.place(relx=0.55, rely=0.45)
        self.state_entry = ctk.CTkEntry(self.frame, width=250)
        self.state_entry.place(relx=0.75, rely=0.45)

        self.zip_label = ctk.CTkLabel(self.frame, text="Zip Code", font=("Arial", 14))
        self.zip_label.place(relx=0.55, rely=0.55)
        self.zip_entry = ctk.CTkEntry(self.frame, width=250)
        self.zip_entry.place(relx=0.75, rely=0.55)

        # Mechanic Fields (Initially Hidden)
        self.business_label = ctk.CTkLabel(self.frame, text="Business Name", font=("Arial", 14))
        self.service_label = ctk.CTkLabel(self.frame, text="Service ID", font=("Arial", 14))
        self.business_entry = ctk.CTkEntry(self.frame, width=250)
        self.service_entry = ctk.CTkEntry(self.frame, width=250)

        # Login & Register Buttons
        self.login_button = ctk.CTkButton(self, text="Back to Login", width=150, command=self.login_screen)
        self.login_button.place(relx=0.4, rely=0.85, anchor="center")

        self.register_button = ctk.CTkButton(self, text="Register", width=150, command=self.register_user)
        self.register_button.place(relx=0.6, rely=0.85, anchor="center")

        # # Back Button to Login Screen
        # back_icon = Image.open("UI/back.png").resize((30, 30))
        # self.back_photo = ImageTk.PhotoImage(back_icon)
        # back_button = ctk.CTkButton(self, image=self.back_photo, text="", width=60, height=60, fg_color="white",
        #         hover_color="#D9D9D9", command=self.login_screen)
        # back_button.place(x=920, y=600)

    def mechanic_dashboard(self):
        # Destroy previous UI components
        for widget in self.winfo_children():
            widget.destroy()

        # Add image to the mechanic dashboard
        self.bg_image = Image.open("UI/mechanic_screen.jpg")
        self.bg_image = self.bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Add label to the mechanic dashboard
        self.title_label = ctk.CTkLabel(self, text="You are Viewing Mechanic Dashboard", font=("Arial", 20, "bold"), bg_color="white")
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # UI Container (Dashboard Box)
        self.frame = ctk.CTkFrame(self, width=600, height=450, corner_radius=10, fg_color="#D3D3D3")
        self.frame.place(relx=0.05, rely=0.15, anchor="nw")  # Moved a bit down

        # Dashboard Title
        self.title_label = ctk.CTkLabel(self.frame, text="Welcome Mechanic", font=("Arial", 20, "bold"))
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Business Registration Section
        self.business_label = ctk.CTkLabel(self.frame, text="Business Registration", font=("Arial", 16, "bold"))
        self.business_label.place(relx=0.05, rely=0.15)

        self.business_name_label = ctk.CTkLabel(self.frame, text="Business Name", font=("Arial", 14))
        self.business_name_label.place(relx=0.05, rely=0.25)
        self.business_name_entry = ctk.CTkEntry(self.frame, width=250)
        self.business_name_entry.place(relx=0.35, rely=0.25)

        self.service_id_label = ctk.CTkLabel(self.frame, text="Service ID", font=("Arial", 14))
        self.service_id_label.place(relx=0.05, rely=0.35)
        self.service_id_entry = ctk.CTkEntry(self.frame, width=250)
        self.service_id_entry.place(relx=0.35, rely=0.35)

        self.zip_code_label = ctk.CTkLabel(self.frame, text="Zip Code", font=("Arial", 14))
        self.zip_code_label.place(relx=0.05, rely=0.45)
        self.zip_code_entry = ctk.CTkEntry(self.frame, width=250)
        self.zip_code_entry.place(relx=0.35, rely=0.45)

        self.service_type_label = ctk.CTkLabel(self.frame, text="Service Type Offered", font=("Arial", 14))
        self.service_type_label.place(relx=0.05, rely=0.55)
        self.service_type_dropdown = ctk.CTkComboBox(self.frame, values=[
            "Oil Change", 
            "Tire Replacement", 
            "General Checkup",
            "Brake Service",
            "Engine Tune-up",
            "Wheel Alignment"
        ], width=250)
        self.service_type_dropdown.place(relx=0.35, rely=0.55)

        self.vehicle_type_label = ctk.CTkLabel(self.frame, text="Type of Vehicles Serviced", font=("Arial", 14))
        self.vehicle_type_label.place(relx=0.05, rely=0.65)
        self.vehicle_type_dropdown = ctk.CTkComboBox(self.frame, values=["Cars", "Bikes", "Trucks"], width=250)
        self.vehicle_type_dropdown.place(relx=0.35, rely=0.65)

        # View/Accept Current Bookings Section
        self.bookings_button = ctk.CTkButton(self, text="View/Accept Current Bookings", width=250, command=self.open_approval_screen)
        self.bookings_button.place(relx=0.75, rely=0.05)

        # Submit Button
        self.submit_button = ctk.CTkButton(self.frame, text="Submit", width=150, command=self.submit_business)
        self.submit_button.place(relx=0.5, rely=0.85, anchor="center")

        # Logout Button
        self.logout_button = ctk.CTkButton(self, text="Logout", width=100, command=self.login_screen)
        self.logout_button.place(relx=0.9, rely=0.95, anchor="center")

        # Populate business name and service ID
        # self.populate_mechanic_details()

    # def populate_mechanic_details(self):
    #     if not hasattr(self, 'user_id') or not self.user_id:
    #         messagebox.showerror("Error", "Mechanic ID not found. Please log in again.")
    #         return

    #     db_connection = mysql.connector.connect(
    #         host="localhost", user="root", password="admin", database="Vehicle_Service_DB"
    #     )
    #     cursor = db_connection.cursor()
    #     query = "SELECT firstname, serviceid, zipcode FROM Mechanics WHERE mechid = %s AND approval_status = 'Approved'"
    #     cursor.execute(query, (self.user_id,))
    #     result = cursor.fetchone()
        
    #     cursor.close()
    #     db_connection.close()

    #     if result:
    #         business_name, service_id, zipcode = result
    #         self.business_name_entry.delete(0, tk.END)
    #         self.service_id_entry.delete(0, tk.END)
    #         self.zip_code_entry.delete(0, tk.END)

    #         self.business_name_entry.insert(0, business_name)
    #         self.service_id_entry.insert(0, service_id)
    #         self.zip_code_entry.insert(0, zipcode)
    #     else:
    #         messagebox.showinfo("Pending Approval", "Your mechanic registration is still pending admin approval.")



    def submit_business(self):
        if not hasattr(self, 'user_id') or not self.user_id:
            messagebox.showerror("Error", "Mechanic ID not found. Please log in again.")
            return

        business_name = self.business_name_entry.get()
        service_type = self.service_type_dropdown.get()
        vehicle_type = self.vehicle_type_dropdown.get()
        zip_code = self.zip_code_entry.get()

        if not business_name or not service_type or not vehicle_type or not zip_code:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        try:
            # First check if a service with this name exists
            cursor.execute("SELECT serviceid FROM Services WHERE servicename = %s", (service_type,))
            service_result = cursor.fetchone()

            if not service_result:
                # If service doesn't exist, create it
                cursor.execute("INSERT INTO Services (servicename, typeofvehicle) VALUES (%s, %s)", 
                            (service_type, vehicle_type))
                db_connection.commit()
                service_id = cursor.lastrowid
            else:
                service_id = service_result[0]

            # Insert the business registration
            cursor.execute(
                """
                INSERT INTO Mechanic_Businesses (mechid, business_name, service_id, zip_code, service_type, vehicle_type, approval_status) 
                VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
                """,
                (self.user_id, business_name, service_id, zip_code, service_type, vehicle_type)
            )

            # Update the mechanic's service ID
            cursor.execute("UPDATE Mechanics SET serviceid = %s WHERE mechid = %s", (service_id, self.user_id))

            db_connection.commit()
            messagebox.showinfo("Success", "Business Registration Submitted! Waiting for Admin Approval.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")
            print(f"Detailed error: {err}")  # For debugging
        finally:
            cursor.close()
            db_connection.close()


    def toggle_mechanic_fields(self):
        if self.mechanic_check.get():
            self.business_label.place(relx=0.55, rely=0.65)
            self.business_entry.place(relx=0.75, rely=0.65)
            self.service_label.place(relx=0.55, rely=0.75)
            self.service_entry.place(relx=0.75, rely=0.75)
        else:
            self.business_label.place_forget()
            self.business_entry.place_forget()
            self.service_label.place_forget()
            self.service_entry.place_forget()
        

    def toggle_mechanic_fields(self):
        if self.mechanic_check.get():
            self.business_label.place(relx=0.55, rely=0.65)
            self.business_entry.place(relx=0.75, rely=0.65)
            self.service_label.place(relx=0.55, rely=0.75)
            self.service_entry.place(relx=0.75, rely=0.75)
        else:
            self.business_label.place_forget()
            self.business_entry.place_forget()
            self.service_label.place_forget()
            self.service_entry.place_forget()
    
    def register_user(self):
        firstname = self.fname_entry.get()
        lastname = self.lname_entry.get()
        email = self.email_entry.get().lower()  # Convert email to lowercase for consistency
        phoneno = self.phone_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        address = self.address_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zipcode = self.zip_entry.get()
        is_mechanic = self.mechanic_check.get()

        if not firstname or not lastname or not email or not phoneno or not password or not confirm_password:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        try:
            # 🔥 Assign roleid correctly
            if "admin" in email:  # ✅ If email contains 'admin', assign roleid = 3
                roleid = 3
            elif is_mechanic:  # ✅ Mechanic role
                roleid = 2
            else:  # ✅ Default to normal user
                roleid = 1  

            # ✅ Insert user with the correct roleid
            cursor.execute(
                "INSERT INTO User (firstname, lastname, email, phoneno, password, address1, city, state, zipcode, roleid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (firstname, lastname, email, phoneno, password, address, city, state, zipcode, roleid),
            )
            db_connection.commit()

            messagebox.showinfo("Success", f"Registration Successful! You are registered as {['User', 'Mechanic', 'Admin'][roleid-1]}. Please log in.")
            self.login_screen()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

        cursor.close()
        db_connection.close()







    def user_dashboard(self, email):
        # Destroy previous UI components
        for widget in self.winfo_children():
            widget.destroy()

        # Add background image
        self.bg_image = Image.open("UI/user_dashboard.jpg")
        self.bg_image = self.bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # welcome user message from database
        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()
        query = "SELECT firstname FROM User WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        db_connection.close()
        if result:
            firstname = result[0]
            self.welcome_label = ctk.CTkLabel(self, text=f"Welcome {firstname}", font=("Arial", 25, "bold"), bg_color="#D1D1D1")
            self.welcome_label.place(relx=0.5, rely=0.1, anchor="center")


        # Search for Mechanics Section
        self.search_label = ctk.CTkLabel(self, text="Search for Mechanics", font=("Arial", 16, "bold"), bg_color="#D1D1D1")
        self.search_label.place(relx=0.05, rely=0.15)

        self.zip_label = ctk.CTkLabel(self, text="Zip Code", font=("Arial", 14), bg_color="#D1D1D1")
        self.zip_label.place(relx=0.05, rely=0.2)
        self.zip_entry = ctk.CTkEntry(self, width=150)
        self.zip_entry.place(relx=0.15, rely=0.2)

        self.service_label = ctk.CTkLabel(self, text="Service Type", font=("Arial", 14), bg_color="#D1D1D1")
        self.service_label.place(relx=0.35, rely=0.2)
        
        # Create dropdown for service type
        services = [
            "Oil Change",
            "Tire Replacement",
            "General Checkup",
            "Brake Service",
            "Engine Tune-up",
            "Wheel Alignment"
        ]
        self.service_dropdown = ctk.CTkComboBox(self, values=services, width=150)
        self.service_dropdown.place(relx=0.45, rely=0.2)
        self.service_dropdown.set(services[0])

        self.search_button = ctk.CTkButton(self, text="Search", width=100, command=self.search_mechanics)
        self.search_button.place(relx=0.65, rely=0.2)

        # self.book_service_button = ctk.CTkButton(self, text="Book Service", width=150, command=self.book_service)
        # self.book_service_button.place(relx=0.8, rely=0.2)

        # View Current Bookings Section
        self.view_bookings_label = ctk.CTkLabel(self, text="View Current Bookings", font=("Arial", 16, "bold"), bg_color="#D1D1D1")
        self.view_bookings_label.place(relx=0.05, rely=0.3)

        self.view_bookings_button = ctk.CTkButton(self, text="View Bookings", width=150, command=self.user_view_bookings)
        self.view_bookings_button.place(relx=0.05, rely=0.35)

        # Available Mechanics Section
        self.available_mechanics_label = ctk.CTkLabel(self, text="Available Mechanics", font=("Arial", 16, "bold"), bg_color="#D1D1D1")
        self.available_mechanics_label.place(relx=0.05, rely=0.45)

        self.mechanics_table = ctk.CTkFrame(self, width=900, height=250, corner_radius=10, fg_color="white")
        self.mechanics_table.place(relx=0.05, rely=0.5)

        # Logout Button
        self.logout_button = ctk.CTkButton(self, text="Logout", width=100, command=self.login_screen)
        self.logout_button.place(relx=0.9, rely=0.95, anchor="center")

    def search_mechanics(self):
        zip_code = self.zip_entry.get()
        service_type = self.service_dropdown.get()  # Changed from service_entry to service_dropdown

        if not zip_code:
            messagebox.showerror("Error", "Please enter a Zip Code!")
            return

        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        try:
            
            query = """
            SELECT B.business_name, S.servicename, B.zip_code, B.vehicle_type
            FROM mechanic_businesses B
            JOIN services S ON B.service_id = S.serviceid
            WHERE B.zip_code = %s AND S.servicename = %s AND B.approval_status = 'Approved'
            """
            cursor.execute(query, (zip_code, service_type))
            results = cursor.fetchall()

            if results:
                self.populate_mechanics_table(results)
            else:
                messagebox.showinfo("No Results", "No approved mechanics found for the given criteria.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

        finally:
            cursor.close()
            db_connection.close()

    def populate_mechanics_table(self, results):
        """ Populate the UI Table with Mechanics List """
        
        
        for widget in self.mechanics_table.winfo_children():
            widget.destroy()

        
        self.mechanics_tree = ttk.Treeview(
            self.mechanics_table, 
            columns=("Business Name", "Service Offered", "Zip Code", "Vehicle Type"), 
            show="headings", height=5
        )
        self.mechanics_tree.pack(side="left", fill="both", expand=True)

        
        scrollbar = ttk.Scrollbar(self.mechanics_table, orient="vertical", command=self.mechanics_tree.yview)
        self.mechanics_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        
        self.mechanics_tree.heading("Business Name", text="Business Name")
        self.mechanics_tree.heading("Service Offered", text="Service Offered")
        self.mechanics_tree.heading("Zip Code", text="Zip Code")
        self.mechanics_tree.heading("Vehicle Type", text="Vehicle Type")

       
        self.mechanics_tree.column("Business Name", width=150)
        self.mechanics_tree.column("Service Offered", width=150)
        self.mechanics_tree.column("Zip Code", width=100)
        self.mechanics_tree.column("Vehicle Type", width=150)

        
        for row in results:
            self.mechanics_tree.insert("", "end", values=row)

        
        self.mechanics_tree.unbind("<ButtonRelease-1>")
        self.mechanics_tree.bind("<ButtonRelease-1>", self.get_selected_mechanic)


        
        self.book_service_button = ctk.CTkButton(self, text="Book Service", width=150, command=self.book_service)
        self.book_service_button.place(relx=0.8, rely=0.2)


    def get_selected_mechanic(self, event=None):
        """ Retrieves the selected mechanic from the table when a user selects one. """
        
        if not hasattr(self, 'mechanics_tree'):
            messagebox.showerror("Error", "Mechanics table not found!")
            return None

        selected_item = self.mechanics_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a mechanic to book a service.")
            return None

        mechanic_data = self.mechanics_tree.item(selected_item, "values")

        if not mechanic_data:
            messagebox.showerror("Error", "No mechanic details found in the selection.")
            return None

        self.selected_mechanic = mechanic_data  # Store the selected mechanic globally
        return mechanic_data  # Return Selected Mechanic Data

    def get_booked_slots(self, date, mechid):
        """ Retrieve all booked time slots for a given date and mechanic. """
        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        try:
            cursor.execute("""
                SELECT appointmenttime FROM Appointments 
                WHERE appointmentdate = %s AND mechid = %s
            """, (date, mechid))

            booked_slots = [row[0] for row in cursor.fetchall()]
            return booked_slots

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")
            return []

        finally:
            cursor.close()
            db_connection.close()


    def update_available_times(self, event=None):
        """ Update the available time slots based on existing bookings. """
        
        # Get the selected date
        selected_date = self.calendar.get_date()

        try:
            # Convert date to correct format
            date_obj = datetime.strptime(selected_date, '%m/%d/%y')
            formatted_date = date_obj.strftime('%Y-%m-%d')

            # Fetch booked slots using `mechid`
            booked_slots = self.get_booked_slots(formatted_date, self.mechid)

            # Define all possible time slots
            all_time_slots = ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"]

            # Remove booked slots
            available_slots = [slot for slot in all_time_slots if slot not in booked_slots]

            if not available_slots:
                available_slots = ["No slots available"]

            # Update the dropdown options
            self.time_dropdown.configure(values=available_slots)
            self.time_dropdown.set(available_slots[0])

        except ValueError:
            messagebox.showerror("Error", "Invalid date selection!")

    def book_service(self):
        """ Opens the booking screen with selected mechanic details. """
        
        # Get the selected mechanic data
        if not hasattr(self, 'mechanics_tree'):
            messagebox.showerror("Error", "Please search for mechanics first!")
            return

        selected_item = self.mechanics_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a mechanic to book a service.")
            return  

        mechanic_data = self.mechanics_tree.item(selected_item, "values")
        if not mechanic_data:
            messagebox.showerror("Error", "No mechanic details found in the selection.")
            return

        self.selected_mechanic = mechanic_data

        business_name, service_offered, _, vehicle_type = self.selected_mechanic

        # Retrieve mechid from the database
        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        try:
            cursor.execute("SELECT mechid FROM Mechanic_Businesses WHERE business_name = %s", (business_name,))
            mechanic_result = cursor.fetchone()

            if not mechanic_result:
                messagebox.showerror("Error", "Could not find the selected mechanic!")
                return

            self.mechid = mechanic_result[0]  # Store mechid globally

        finally:
            cursor.close()
            db_connection.close()

        for widget in self.winfo_children():
            widget.destroy()

        self.title_label = ctk.CTkLabel(self, text="Book Appointment", font=("Arial", 22, "bold"))
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        self.mechanic_label = ctk.CTkLabel(self, text=f"Mechanic: {business_name}", font=("Arial", 16))
        self.mechanic_label.place(relx=0.05, rely=0.15)

        self.service_label = ctk.CTkLabel(self, text=f"Service: {service_offered}", font=("Arial", 16))
        self.service_label.place(relx=0.05, rely=0.2)

        self.vehicle_label = ctk.CTkLabel(self, text=f"Vehicle Type: {vehicle_type}", font=("Arial", 16))
        self.vehicle_label.place(relx=0.05, rely=0.25)

        self.calendar_label = ctk.CTkLabel(self, text="Select Appointment Date:", font=("Arial", 14))
        self.calendar_label.place(relx=0.05, rely=0.35)

        self.calendar = Calendar(self, selectmode="day", year=2025, month=3, day=1)
        self.calendar.place(relx=0.05, rely=0.4)
        self.calendar.bind("<<CalendarSelected>>", self.update_available_times)

        self.time_label = ctk.CTkLabel(self, text="Select Time Slot:", font=("Arial", 14))
        self.time_label.place(relx=0.05, rely=0.65)

        self.time_dropdown = ctk.CTkComboBox(self, values=["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"], width=150)
        self.time_dropdown.place(relx=0.05, rely=0.7)

        # Initialize available time slots
        self.update_available_times()

        self.confirm_button = ctk.CTkButton(self, text="Confirm Appointment", width=200, 
                                            command=lambda: self.confirm_booking(business_name, vehicle_type))
        self.confirm_button.place(relx=0.5, rely=0.85, anchor="center")

        # Store email in instance variable for back button
        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()
        
        try:
            cursor.execute("SELECT email FROM User WHERE userid = %s", (self.user_id,))
            result = cursor.fetchone()
            self.user_email = result[0] if result else "unknown@email.com"
        finally:
            cursor.close()
            db_connection.close()

        self.back_button = ctk.CTkButton(self, text="Back", width=100, 
                                        command=lambda: self.user_dashboard(self.user_email))
        self.back_button.place(relx=0.05, rely=0.9)


    def confirm_booking(self, business_name, vehicle_type):
        """ Stores the appointment in the database after user confirmation. """
        selected_date = self.calendar.get_date()
        selected_time = self.time_dropdown.get()

        if not selected_date or not selected_time or selected_time == "No slots available":
            messagebox.showerror("Error", "Please select a valid date and time slot!")
            return

        try:
            # Convert date from MM/DD/YY to YYYY-MM-DD
            date_obj = datetime.strptime(selected_date, '%m/%d/%y')
            formatted_date = date_obj.strftime('%Y-%m-%d')

            # Convert time from 12-hour to 24-hour format
            time_obj = datetime.strptime(selected_time, '%I:%M %p')
            formatted_time = time_obj.strftime('%H:%M:00')

            db_connection = mysql.connector.connect(
                host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
            )
            cursor = db_connection.cursor()

            try:
                # Insert the appointment with the correct `mechid`
                cursor.execute(
                    """
                    INSERT INTO Appointments (userid, mechid, appointmentdate, appointmenttime, status, typeofvehicle) 
                    VALUES (%s, %s, %s, %s, 'Pending', %s)
                    """,
                    (self.user_id, self.mechid, formatted_date, formatted_time, vehicle_type)
                )

                db_connection.commit()
                messagebox.showinfo("Success", "Appointment booked successfully!")
                self.user_dashboard(self.user_email)  # Redirect back to dashboard

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database Error: {err}")
                print(f"Database error: {err}")
            finally:
                cursor.close()
                db_connection.close()

        except ValueError as e:
            messagebox.showerror("Error", "Invalid date or time format!")
            print(f"Date/Time formatting error: {e}")



    def user_view_bookings(self):
        if not hasattr(self, 'user_id') or not self.user_id: 
            messagebox.showerror("Error", "User not logged in!")
            return

        # Destroy previous UI components
        for widget in self.winfo_children():
            widget.destroy()

        # Add background image
        self.bg_image = ctk.CTkImage(Image.open("UI/user_view_bookings.jpg"), size=(1200, 750))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Viewing Bookings", font=("Arial", 22, "bold"))
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Subtitle Label
        self.list_label = ctk.CTkLabel(self, text="List of Appointments", font=("Arial", 16, "bold"))
        self.list_label.place(relx=0.05, rely=0.15)

        # Connect to DB
        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        # Fetch appointments with mechanic details from User table
        query = """
        SELECT U.firstname, A.appointmentdate, A.typeofvehicle, MB.service_type, A.status
        FROM Appointments A
        JOIN User U ON A.mechid = U.userid
        JOIN Mechanic_Businesses MB ON A.mechid = MB.mechid
        WHERE A.userid = %s
        """
        cursor.execute(query, (self.user_id,))
        bookings = cursor.fetchall()

        cursor.close()
        db_connection.close()

        # If no bookings found
        if not bookings:
            messagebox.showinfo("No Bookings", "No appointments found.")
            return

        # Create a table frame
        self.bookings_frame = ctk.CTkFrame(self, width=900, height=300, corner_radius=10, fg_color="white")
        self.bookings_frame.place(relx=0.05, rely=0.2)

        # Table Headers
        headers = ["Mechanic", "Date", "Vehicle Type", "Service", "Status"]
        for col_idx, header in enumerate(headers):
            label = ctk.CTkLabel(self.bookings_frame, text=header, font=("Arial", 14, "bold"))
            label.grid(row=0, column=col_idx, padx=20, pady=5)

        # Populate the table
        for row_idx, row in enumerate(bookings, start=1):
            for col_idx, value in enumerate(row):
                label = ctk.CTkLabel(self.bookings_frame, text=value, font=("Arial", 12))
                label.grid(row=row_idx, column=col_idx, padx=20, pady=5)

        # Back Button
        self.back_button = ctk.CTkButton(self, text="Back", width=100, command=lambda: self.user_dashboard(None))
        self.back_button.place(relx=0.9, rely=0.9)

    def open_approval_screen(self):
        """ Opens the appointment approval screen (removes calendar). """
        
        # Clear previous UI components
        for widget in self.winfo_children():
            widget.destroy()

        # Title
        self.title_label = ctk.CTkLabel(self, text="View & Approve Appointments", font=("Arial", 22, "bold"))
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Appointments List Frame
        self.appointments_frame = ctk.CTkFrame(self, width=900, height=500)
        self.appointments_frame.place(relx=0.05, rely=0.15)

        # Create Treeview for appointments
        self.appointments_tree = ttk.Treeview(
            self.appointments_frame,
            columns=("Time", "Customer", "Vehicle", "Service", "Status", "AppointmentID"),
            show="headings",
            height=10
        )

        # Configure columns
        self.appointments_tree.heading("Time", text="Time")
        self.appointments_tree.heading("Customer", text="Customer")
        self.appointments_tree.heading("Vehicle", text="Vehicle Type")
        self.appointments_tree.heading("Service", text="Service")
        self.appointments_tree.heading("Status", text="Status")
        self.appointments_tree.heading("AppointmentID", text="Appointment ID")

        self.appointments_tree.column("Time", width=100)
        self.appointments_tree.column("Customer", width=150)
        self.appointments_tree.column("Vehicle", width=100)
        self.appointments_tree.column("Service", width=100)
        self.appointments_tree.column("Status", width=100)
        self.appointments_tree.column("AppointmentID", width=0, stretch=NO)  # Hidden column

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.appointments_frame, orient="vertical", command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscroll=scrollbar.set)

        # Pack the Treeview and scrollbar
        self.appointments_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create frame for action buttons
        self.action_frame = ctk.CTkFrame(self.appointments_frame, height=50)
        self.action_frame.pack(side="bottom", fill="x", pady=10)

        # Approve Button
        self.approve_btn = ctk.CTkButton(
            self.action_frame,
            text="Approve",
            width=100,
            state="disabled"
        )
        self.approve_btn.pack(side="left", padx=10)

        # Reject Button
        self.reject_btn = ctk.CTkButton(
            self.action_frame,
            text="Reject",
            width=100,
            fg_color="red",
            state="disabled"
        )
        self.reject_btn.pack(side="left", padx=10)

        # Bind selection event
        self.appointments_tree.bind('<<TreeviewSelect>>', self.on_appointment_select)

        # Back Button
        self.back_button = ctk.CTkButton(self, text="Back", width=100, command=self.mechanic_dashboard)
        self.back_button.place(relx=0.05, rely=0.9)

        # ✅ Call `show_appointments()` correctly
        self.show_appointments()




    def on_appointment_select(self, event):
        """ Enable action buttons when an appointment is selected. """

        selected_item = self.appointments_tree.selection()
        if not selected_item:
            return

        # Get the selected appointment data
        item = self.appointments_tree.item(selected_item[0])  # Get first selected item
        appointment_data = item['values']
        
        if not appointment_data:
            return

        status = appointment_data[4]  # Status (5th column)
        appt_id = appointment_data[5]  # Appointment ID (6th hidden column)

        # Enable buttons only for pending appointments
        if status == 'Pending':
            self.approve_btn.configure(state="normal", command=lambda: self.handle_appointment(appt_id, "Approved"))
            self.reject_btn.configure(state="normal", command=lambda: self.handle_appointment(appt_id, "Rejected"))
        else:
            self.approve_btn.configure(state="disabled")
            self.reject_btn.configure(state="disabled")



    def show_appointments(self, event=None):
        """ Fetch and display appointments in the table. """

        # Clear existing rows in the Treeview
        for row in self.appointments_tree.get_children():
            self.appointments_tree.delete(row)

        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        # ✅ Fetch appointments for the current mechanic
        query = """
            SELECT A.appointmenttime, U.firstname, A.typeofvehicle, S.servicename, A.status, A.appointmentid
            FROM Appointments A
            JOIN User U ON A.userid = U.userid
            JOIN Mechanics M ON A.mechid = M.mechid
            JOIN Services S ON M.serviceid = S.serviceid
            WHERE M.mechid = %s
        """
        cursor.execute(query, (self.user_id,))
        appointments = cursor.fetchall()

        # Populate the table
        for row in appointments:
            self.appointments_tree.insert("", "end", values=row)

        cursor.close()
        db_connection.close()



    def handle_appointment(self, appt_id, status):
        """ Approves or Rejects an appointment and updates the database. """

        # ✅ Fix the status mapping
        if status == "Approved":  
            status = "In Progress"  # 🔹 Convert "Approved" to a valid ENUM value

        # ✅ Ensure status is valid
        valid_statuses = ["Pending", "In Progress", "Completed"]
        if status not in valid_statuses:
            messagebox.showerror("Error", f"Invalid status '{status}'! Allowed: {valid_statuses}")
            return

        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        try:
            # ✅ Update appointment status in the database
            cursor.execute("UPDATE Appointments SET status = %s WHERE appointmentid = %s", (status, appt_id))
            db_connection.commit()

            # Notify user
            messagebox.showinfo("Success", f"Appointment {status} successfully!")

            # Refresh appointments list
            self.show_appointments()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

        finally:
            cursor.close()
            db_connection.close()

    def admin_dashboard(self):
        """ Displays the Admin Dashboard UI. """
        for widget in self.winfo_children():
            widget.destroy()

        # Background Image
        self.bg_image = Image.open("UI/admin_dashboard.jpg")
        self.bg_image = self.bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Welcome Admin", font=("Arial", 24, "bold"))
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # View Requests Button
        self.view_requests_button = ctk.CTkButton(self, text="View Requests", width=200, command=self.view_mechanic_requests)
        self.view_requests_button.place(relx=0.2, rely=0.3)

        # Generate Report Button
        self.report_button = ctk.CTkButton(self, text="Report", width=200, command=self.generate_admin_report)
        self.report_button.place(relx=0.2, rely=0.45)

        # Logout Button
        self.logout_button = ctk.CTkButton(self, text="Logout", width=100, command=self.login_screen)
        self.logout_button.place(relx=0.9, rely=0.95, anchor="center")
    


    def view_mechanic_requests(self):
        # Clear existing UI
        for widget in self.winfo_children():
            widget.destroy()

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Pending Mechanic Requests", font=("Arial", 20, "bold"))
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Table Frame
        self.request_table_frame = ctk.CTkFrame(self, width=900, height=300, corner_radius=10, fg_color="white")
        self.request_table_frame.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.6)

        # Table with Scrollbar
        self.request_table = ttk.Treeview(self.request_table_frame, columns=("Mech ID", "Business Name", "Service ID", "Zip Code"), show="headings")
        self.request_table.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.request_table_frame, orient="vertical", command=self.request_table.yview)
        self.request_table.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.request_table.heading("Mech ID", text="Mech ID")
        self.request_table.heading("Business Name", text="Business Name")
        self.request_table.heading("Service ID", text="Service ID")
        self.request_table.heading("Zip Code", text="Zip Code")

        # Populate Mechanic Requests
        self.populate_mechanic_requests()

        # Approve Button
        approve_icon = Image.open("UI/mark.png").resize((30, 30))
        self.approve_photo = ImageTk.PhotoImage(approve_icon)
        approve_button = ctk.CTkButton(self, image=self.approve_photo, text="", width=60, height=60, fg_color="white",
                                    hover_color="#D9D9D9", command=self.approve_selected_mechanic)
        approve_button.place(x=600, y=600)

        # Reject Button
        reject_icon = Image.open("UI/decline.png").resize((40, 40))
        self.reject_photo = ImageTk.PhotoImage(reject_icon)
        reject_button = ctk.CTkButton(self, image=self.reject_photo, text="", width=60, height=60, fg_color="white",
                                    hover_color="#D9D9D9", command=self.reject_selected_mechanic)
        reject_button.place(x=700, y=600)

        # Back Button
        self.back_button = ctk.CTkButton(self, text="Back", width=100, command=self.admin_dashboard)
        self.back_button.place(relx=0.05, rely=0.9)

    def populate_mechanic_requests(self):
        """ Fetches pending mechanic requests and populates the table. """
        
        # Clear existing rows in the table
        for row in self.request_table.get_children():
            self.request_table.delete(row)

        # Connect to the database
        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()

        cursor.execute("SELECT business_id, business_name, service_id, zip_code, service_type, vehicle_type FROM Mechanic_Businesses WHERE approval_status = 'Pending'")
        requests = cursor.fetchall()

        # Populate the table with fetched requests
        for request in requests:
            self.request_table.insert("", "end", values=request)

        cursor.close()
        db_connection.close()

    def approve_selected_mechanic(self):
        selected_item = self.request_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No mechanic selected!")
            return

        business_id = self.request_table.item(selected_item, "values")[0]

        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        cursor.execute("UPDATE Mechanic_Businesses SET approval_status = 'Approved' WHERE business_id = %s", (business_id,))
        db_connection.commit()
        
        cursor.close()
        db_connection.close()

        messagebox.showinfo("Success", "Mechanic Business Approved!")
        self.view_mechanic_requests()  # Refresh request list

    def reject_selected_mechanic(self):
        selected_item = self.request_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No mechanic selected!")
            return

        business_id = self.request_table.item(selected_item, "values")[0]

        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        cursor.execute("UPDATE Mechanic_Businesses SET approval_status = 'Rejected' WHERE business_id = %s", (business_id,))
        db_connection.commit()
        
        cursor.close()
        db_connection.close()

        messagebox.showinfo("Rejected", "Mechanic Business Rejected!")
        self.view_mechanic_requests()  # Refresh request list

    def generate_admin_report(self):
        """ Generates a report of registered mechanics and appointments. """
        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()

        # Fetch Mechanic Report
        cursor.execute("SELECT firstname, serviceid, city FROM Mechanics WHERE approval_status = 'Approved'")
        mechanics = cursor.fetchall()

        # Fetch Appointments Report
        cursor.execute("SELECT appointmentdate, appointmenttime, status FROM Appointments")
        appointments = cursor.fetchall()

        cursor.close()
        db_connection.close()

        report_text = "Mechanics Report:\n" + "\n".join([f"{m[0]}, Service: {m[1]}, City: {m[2]}" for m in mechanics])
        report_text += "\n\nAppointments Report:\n" + "\n".join([f"Date: {a[0]}, Time: {a[1]}, Status: {a[2]}" for a in appointments])

        # Save to File
        with open("admin_report.txt", "w") as file:
            file.write(report_text)

        messagebox.showinfo("Report Generated", "Report saved as 'admin_report.txt'!")





if __name__ == "__main__":
    app = VehicleServiceApp()
    app.mainloop()

