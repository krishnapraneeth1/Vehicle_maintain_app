import tkinter
#import python ,tkinter, mysql and other libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error, IntegrityError
from PIL import Image, ImageTk
from tkinter import filedialog
import re
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from datetime import datetime, timedelta
from tkinter import ttk
from tkinter import simpledialog
import webbrowser
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from fpdf import FPDF
import os
from tkinter import filedialog
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas
import mysql.connector



db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123"
)
cursor = db_connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Vehicle_Service_DB")
print("Database 'Vehicle_Service_DB' created or already exists.")
cursor.close()
db_connection.close()


db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="Vehicle_Service_DB"
)
cursor = db_connection.cursor()


def table_exists(table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None

tables = {
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
        zipcode VARCHAR(10)
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
        serviceid INT,
        firstname VARCHAR(100) NOT NULL,
        lastname VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        phoneno VARCHAR(15),
        address1 VARCHAR(255),
        city VARCHAR(100),
        state VARCHAR(100),
        zipcode VARCHAR(10),
        FOREIGN KEY (serviceid) REFERENCES Services(serviceid) ON DELETE CASCADE
    )""",
    "Appointments": """
    CREATE TABLE IF NOT EXISTS Appointments (
        appointmentid INT PRIMARY KEY AUTO_INCREMENT,
        userid INT,
        mechid INT,
        appointmentdate DATE NOT NULL,
        appointmenttime TIME NOT NULL,
        status ENUM('Pending', 'In Progress', 'Completed') NOT NULL,
        typeofvehicle VARCHAR(50) NOT NULL,
        FOREIGN KEY (userid) REFERENCES User(userid) ON DELETE CASCADE,
        FOREIGN KEY (mechid) REFERENCES Mechanics(mechid) ON DELETE CASCADE
    )"""
}


for table_name, create_query in tables.items():
    if not table_exists(table_name):
        cursor.execute(create_query)
        print(f"Table '{table_name}' created successfully.")
    else:
        print(f"Table '{table_name}' already exists, skipping creation.")


db_connection.commit()
cursor.close()
db_connection.close()
print("Database setup completed successfully!")


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

        
        # Check if admin
        if email == "admin" and password == "admin":
            self.admin_dashboard()
            return

        # Connect to Database
        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()

        # Check if user exists and fetch role + ID
        query = "SELECT userid, role FROM User WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        if result:
            user_id, role = result
            self.user_id = user_id  # Store user ID globally in the app

            if role == "user":
                self.user_dashboard(email)  # Redirect to User Dashboard
            elif role == "mechanic":
                self.mechanic_dashboard()  # Redirect to Mechanic Dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

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
        self.service_type_dropdown = ctk.CTkComboBox(self.frame, values=["Oil Change", "Tire Replacement", "General Checkup"], width=250)
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
        self.populate_mechanic_details()

    def populate_mechanic_details(self):
        """ Fetch mechanic details from the database and populate fields. """
        if not hasattr(self, 'user_id'):  # Ensure user_id exists
            messagebox.showerror("Error", "Mechanic ID not found. Please log in again.")
            return

        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        # Fetch mechanic details using stored user_id
        query = "SELECT firstname, serviceid, zipcode FROM Mechanics WHERE mechid = %s"
        cursor.execute(query, (self.user_id,))
        result = cursor.fetchone()
        
        cursor.close()
        db_connection.close()

        if result:
            business_name, service_id, zipcode = result
            self.business_name_entry.delete(0, tk.END)
            self.service_id_entry.delete(0, tk.END)
            self.zip_code_entry.delete(0, tk.END)

            self.business_name_entry.insert(0, business_name)
            self.service_id_entry.insert(0, service_id)
            self.zip_code_entry.insert(0, zipcode)


    def submit_business(self):
        business_name = self.business_name_entry.get()
        service_id = self.service_id_entry.get()
        zip_code = self.zip_code_entry.get()

        if not business_name or not service_id or not zip_code:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        if not service_id.isdigit():
            messagebox.showerror("Error", "Service ID must be a number!")
            return

        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO Mechanics (serviceid, firstname, lastname, zipcode, email) VALUES (%s, %s, %s, %s, %s)", (service_id, business_name, "N/A", zip_code, "example@example.com"))
        db_connection.commit()
        cursor.execute("INSERT INTO Mechanics (serviceid, firstname, lastname, zipcode, email, password) VALUES (%s, %s, %s, %s, %s, %s)", (service_id, business_name, "N/A", zip_code, "example@example.com", "default_password"))
        db_connection.close()

        messagebox.showinfo("Success", "Business Registered Successfully!")

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
        email = self.email_entry.get()
        phoneno = self.phone_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        address = self.address_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zipcode = self.zip_entry.get()
        
        # Check if the "Are you a Mechanic?" checkbox is selected
        role = "mechanic" if self.mechanic_check.get() else "user"

        if not firstname or not lastname or not email or not phoneno or not password or not confirm_password:
            messagebox.showerror("Error", "All fields must be filled!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Store user data in the database
        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()

        query = "INSERT INTO User (firstname, lastname, email, phoneno, password, address1, city, state, zipcode, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (firstname, lastname, email, phoneno, password, address, city, state, zipcode, role)

        try:
            cursor.execute(query, values)
            db_connection.commit()
            messagebox.showinfo("Success", "Registration Successful! Please login.")
            self.login_screen()  # Redirect to login screen
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
        self.service_entry = ctk.CTkEntry(self, width=150)
        self.service_entry.place(relx=0.45, rely=0.2)

        self.search_button = ctk.CTkButton(self, text="Search", width=100, command=self.search_mechanics)
        self.search_button.place(relx=0.65, rely=0.2)

        self.book_service_button = ctk.CTkButton(self, text="Book Service", width=150, command=self.book_service)
        self.book_service_button.place(relx=0.8, rely=0.2)

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
        service_type = self.service_entry.get()

        if not zip_code:
            messagebox.showerror("Error", "Please enter a Zip Code!")
            return

        # Fetch only Approved Mechanics
        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()
        query = """
        SELECT firstname, serviceid, zipcode 
        FROM Mechanics 
        WHERE zipcode = %s AND serviceid = %s AND approval_status = 'Approved'
        """
        cursor.execute(query, (zip_code, service_type))
        results = cursor.fetchall()

        if results:
            self.populate_mechanics_table(results)
        else:
            messagebox.showinfo("No Results", "No mechanics found for the given criteria.")

        cursor.close()
        db_connection.close()


    def populate_mechanics_table(self, results):
        for widget in self.mechanics_table.winfo_children():
            widget.destroy()

        headers = ["Business Name", "Service Offered", "Types of Vehicles Serviced", "Rating"]
        for idx, header in enumerate(headers):
            label = ctk.CTkLabel(self.mechanics_table, text=header, font=("Arial", 14, "bold"), fg_color="lightgray")
            label.grid(row=0, column=idx, padx=20, pady=5)

        for row_idx, row in enumerate(results, start=1):
            for col_idx, value in enumerate(row):
                label = ctk.CTkLabel(self.mechanics_table, text=value, font=("Arial", 12))
                label.grid(row=row_idx, column=col_idx, padx=20, pady=5)

    def user_view_bookings(self):
        if not hasattr(self, 'user_id') or not self.user_id:  # ✅ Ensure user_id is set
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

        # Fetch only **approved** appointments
        query = """
        SELECT M.firstname, A.appointmentdate, A.typeofvehicle, S.servicename, A.status
        FROM Appointments A
        JOIN Mechanics M ON A.mechid = M.mechid
        JOIN Services S ON M.serviceid = S.serviceid
        WHERE A.userid = %s AND A.status = 'Approved'
        """
        cursor.execute(query, (self.user_id,))
        bookings = cursor.fetchall()

        cursor.close()
        db_connection.close()

        # If no approved bookings found
        if not bookings:
            messagebox.showinfo("No Bookings", "No approved appointments found.")
            return

        # Create a table frame
        self.bookings_frame = ctk.CTkFrame(self, width=900, height=300, corner_radius=10, fg_color="white")
        self.bookings_frame.place(relx=0.05, rely=0.2)

        # Table Headers
        headers = ["Mechanic", "Date", "Type of Vehicle", "Service", "Status"]
        for col_idx, header in enumerate(headers):
            label = ctk.CTkLabel(self.bookings_frame, text=header, font=("Arial", 14, "bold"))
            label.grid(row=0, column=col_idx, padx=20, pady=5)

        # Populate the table
        for row_idx, row in enumerate(bookings, start=1):
            for col_idx, value in enumerate(row):
                label = ctk.CTkLabel(self.bookings_frame, text=value, font=("Arial", 12))
                label.grid(row=row_idx, column=col_idx, padx=20, pady=5)

        # Back Button
        self.back_button = ctk.CTkButton(self, text="Back", width=100, command=self.user_dashboard)
        self.back_button.place(relx=0.9, rely=0.9)



    def book_service(self):
        selected_mechanic = self.get_selected_mechanic()  # Retrieve selected mechanic from table
        if not selected_mechanic:
            messagebox.showerror("Error", "Please select a mechanic to book a service.")
            return

        # Ask user for appointment details
        appointment_date = simpledialog.askstring("Input", "Enter Appointment Date (YYYY-MM-DD):")
        appointment_time = simpledialog.askstring("Input", "Enter Appointment Time (HH:MM AM/PM):")

        if not appointment_date or not appointment_time:
            messagebox.showerror("Error", "Appointment date and time are required!")
            return

        try:
            # Connect to the database
            db_connection = mysql.connector.connect(
                host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
            )
            cursor = db_connection.cursor()

            # Insert appointment data
            query = """
            INSERT INTO Appointments (userid, mechid, appointmentdate, appointmenttime, status, typeofvehicle) 
            VALUES (%s, %s, %s, %s, 'Pending', %s)
            """
            cursor.execute(query, (self.user_id, selected_mechanic, appointment_date, appointment_time, self.service_entry.get()))
            db_connection.commit()

            messagebox.showinfo("Success", "Service booked successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            db_connection.close()
    
    def get_selected_mechanic(self):
        try:
            selected_item = self.requests_table.focus()
            if not selected_item:
                return None

            mechanic_data = self.requests_table.item(selected_item, "values")
            return mechanic_data[0]
        except AttributeError:
            messagebox.showerror("Error", "Mechanics table not found!")
            return None



    def open_approval_screen(self):
        """ Fetch pending appointment and open approval screen """
        db_connection = mysql.connector.connect(
            host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
        )
        cursor = db_connection.cursor()

        # Fetch pending appointments
        cursor.execute("""
            SELECT appointmentid, userid, typeofvehicle, appointmentdate, appointmenttime
            FROM Appointments WHERE status='Pending' LIMIT 1
        """)
        appointment = cursor.fetchone()

        cursor.close()
        db_connection.close()

        if appointment:
            appointment_id, user_id, vehicle_type, date, time = appointment
            service_type = "Oil Change"  # Replace with actual fetched service type
            issue = "General Maintenance"  # Replace with actual fetched issue

            # Open mechanic approval screen with correct data
            self.mechanic_approval_screen(appointment_id, user_id, service_type, vehicle_type, issue, f"{date} {time}")
        else:
            messagebox.showinfo("No Appointments", "No pending appointments found.")

    def mechanic_approval_screen(self, appointment_id, user_id, service_type, vehicle_type, issue, booking_datetime):
        """ Mechanic approval/rejection screen for appointments """
        for widget in self.winfo_children():
            widget.destroy()

        # Add background image using CTkImage
        self.bg_image = CTkImage(dark_image=Image.open("UI/approval_screen.jpg"), size=(1200, 750))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Accept/Reject Bookings", font=("Arial", 20, "bold"))
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Customer Name
        self.customer_label = ctk.CTkLabel(self, text="Customer Name", font=("Arial", 14))
        self.customer_label.place(relx=0.05, rely=0.2)
        self.customer_entry = ctk.CTkEntry(self, width=250)
        self.customer_entry.place(relx=0.25, rely=0.2)

        # Fetch customer name from DB
        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()
        cursor.execute("SELECT firstname, lastname FROM User WHERE userid = %s", (user_id,))
        customer = cursor.fetchone()
        cursor.close()
        db_connection.close()
        if customer:
            self.customer_entry.insert(0, f"{customer[0]} {customer[1]}")

        # Service Type
        self.service_label = ctk.CTkLabel(self, text="Type of Service Requesting", font=("Arial", 14))
        self.service_label.place(relx=0.05, rely=0.3)
        self.service_entry = ctk.CTkEntry(self, width=250)
        self.service_entry.insert(0, service_type)
        self.service_entry.place(relx=0.25, rely=0.3)

        # Vehicle Type
        self.vehicle_label = ctk.CTkLabel(self, text="Type of Vehicle", font=("Arial", 14))
        self.vehicle_label.place(relx=0.05, rely=0.4)
        self.vehicle_entry = ctk.CTkEntry(self, width=250)
        self.vehicle_entry.insert(0, vehicle_type)
        self.vehicle_entry.place(relx=0.25, rely=0.4)

        # Issue Description
        self.issue_label = ctk.CTkLabel(self, text="Issue", font=("Arial", 14))
        self.issue_label.place(relx=0.05, rely=0.5)
        self.issue_entry = ctk.CTkEntry(self, width=250)
        self.issue_entry.insert(0, issue)
        self.issue_entry.place(relx=0.25, rely=0.5)

        # Booking Date & Time
        self.datetime_label = ctk.CTkLabel(self, text="Booking Date and Time", font=("Arial", 14))
        self.datetime_label.place(relx=0.05, rely=0.6)
        self.datetime_entry = ctk.CTkEntry(self, width=250)
        self.datetime_entry.insert(0, booking_datetime)
        self.datetime_entry.place(relx=0.25, rely=0.6)

        # Accept Button
        self.accept_button = ctk.CTkButton(self, text="Accept", width=150, command=lambda: self.approve_booking(appointment_id, user_id))
        self.accept_button.place(relx=0.4, rely=0.75, anchor="center")

        # Reject Button
        self.reject_button = ctk.CTkButton(self, text="Reject", width=150, fg_color="red", command=lambda: self.reject_booking(appointment_id, user_id))
        self.reject_button.place(relx=0.6, rely=0.75, anchor="center")

        # Back Button
        self.back_button = ctk.CTkButton(self, text="Back", width=100, command=self.mechanic_dashboard)
        self.back_button.place(relx=0.05, rely=0.9)

    def approve_booking(self, appointment_id, user_id):
        """ Approves an appointment and sends confirmation email """
        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()

        # Update appointment status
        cursor.execute("UPDATE Appointments SET status = 'Approved' WHERE appointmentid = %s", (appointment_id,))
        db_connection.commit()

        # Fetch user email
        cursor.execute("SELECT email FROM User WHERE userid = %s", (user_id,))
        user_email = cursor.fetchone()[0]
        cursor.close()
        db_connection.close()

        # Send confirmation email
        self.send_email(user_email, "Your Appointment is Approved", "Your appointment has been successfully approved.")

        messagebox.showinfo("Success", "Appointment Approved! Confirmation email sent.")
        self.mechanic_dashboard()

    def reject_booking(self, appointment_id, user_id):
        """ Rejects an appointment and notifies the user """
        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()

        # Update appointment status
        cursor.execute("UPDATE Appointments SET status = 'Rejected' WHERE appointmentid = %s", (appointment_id,))
        db_connection.commit()

        # Fetch user email
        cursor.execute("SELECT email FROM User WHERE userid = %s", (user_id,))
        user_email = cursor.fetchone()[0]
        cursor.close()
        db_connection.close()

        # Send rejection email
        self.send_email(user_email, "Your Appointment is Rejected", "Unfortunately, your appointment request has been rejected.")

        messagebox.showinfo("Rejected", "Appointment Rejected! User has been notified.")
        self.mechanic_dashboard()

    def send_email(self, recipient, subject, body):
        """ Sends an email notification to the user """
        print(f"Email Sent to {recipient}: {subject}")

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
        """ Shows all pending mechanics waiting for admin approval. """
        for widget in self.winfo_children():
            widget.destroy()

        # Background Image
        self.bg_image = Image.open("UI/admin_request_screen.jpg")
        self.bg_image = self.bg_image.resize((1200, 750), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Pending Mechanic Requests", font=("Arial", 22, "bold"))
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Mechanic Requests Table
        self.requests_table = ttk.Treeview(self, columns=("MechID", "Business Name", "Service Type", "City", "Action"), show="headings")
        self.requests_table.place(relx=0.1, rely=0.15, width=1000, height=400)

        self.requests_table.heading("MechID", text="ID")
        self.requests_table.heading("Business Name", text="Business Name")
        self.requests_table.heading("Service Type", text="Service Type")
        self.requests_table.heading("City", text="City")
        self.requests_table.heading("Action", text="Action")

        self.populate_mechanic_requests()


        #add image as button to approve or reject the mechanic
        approve_icon = Image.open("UI/mark.png").resize((30, 30))
        self.approve_photo = ImageTk.PhotoImage(approve_icon)
        approve_button = ctk.CTkButton(self, image=self.approve_photo, text="", width=60, height=60, fg_color="white",
                hover_color="#D9D9D9", command=lambda: self.approve_mechanic(self.get_selected_mechanic()))
        approve_button.place(x=600, y=600)

        reject_icon = Image.open("UI/decline.png").resize((40, 40))
        self.reject_photo = ImageTk.PhotoImage(reject_icon)
        reject_button = ctk.CTkButton(self, image=self.reject_photo, text="", width=60, height=60, fg_color="white",
                hover_color="#D9D9D9", command=lambda: self.reject_mechanic(self.get_selected_mechanic()))
        reject_button.place(x=700, y=600)


        # Back Button
        self.back_button = ctk.CTkButton(self, text="Back", width=100, command=self.admin_dashboard)
        self.back_button.place(relx=0.05, rely=0.9)

    def populate_mechanic_requests(self):
        """ Fetches pending mechanic requests and populates the table. """
        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()

        cursor.execute("SELECT mechid, firstname, serviceid, city FROM Mechanics WHERE approval_status = 'Pending'")
        requests = cursor.fetchall()

        self.requests_table.delete(*self.requests_table.get_children())

        for request in requests:
            mech_id, business_name, service_type, city = request
            self.requests_table.insert("", "end", values=(mech_id, business_name, service_type, city))

        cursor.close()
        db_connection.close()

        # Add Approve/Reject Buttons
        for child in self.requests_table.get_children():
            self.requests_table.insert(child, "end", values=("Approve", "Reject"))

    def approve_mechanic(self, mechid):
        """ Approves a mechanic's business request. """
        if not mechid:
            messagebox.showerror("Error", "No mechanic selected!")
            return

        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()

        cursor.execute("UPDATE Mechanics SET approval_status = 'Approved' WHERE mechid = %s", (mechid,))
        db_connection.commit()

        cursor.close()
        db_connection.close()

        messagebox.showinfo("Success", "Mechanic Approved!")
        self.view_mechanic_requests()

    def reject_mechanic(self, mechid):
        """ Rejects a mechanic's business request. """
        if not mechid:
            messagebox.showerror("Error", "No mechanic selected!")
            return

        db_connection = mysql.connector.connect(host="localhost", user="root", password="root@123", database="Vehicle_Service_DB")
        cursor = db_connection.cursor()

        cursor.execute("UPDATE Mechanics SET approval_status = 'Rejected' WHERE mechid = %s", (mechid,))
        db_connection.commit()

        cursor.close()
        db_connection.close()

        messagebox.showinfo("Rejected", "Mechanic Rejected!")
        self.view_mechanic_requests()
    
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

