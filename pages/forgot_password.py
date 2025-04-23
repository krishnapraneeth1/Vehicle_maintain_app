import tkinter as tk
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from models.user import User
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import re


class forgotpassword(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.forgot_password_screen()

    def forgot_password_screen(self):
            for widget in self.winfo_children():
                widget.destroy()

            #self.title("Forgot Password")
            self.configure(width=1200, height=750)

            # Background
            self.bg_image = Image.open("UI/forgotpassword.jpg")
            self.bg_image = self.bg_image.resize((1200, 750), Image.LANCZOS)
            self.bg_image = CTkImage(light_image=self.bg_image, dark_image=self.bg_image, size=(1200, 750))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            # Frame
            self.frame = ctk.CTkFrame(self, width=400, height=480, corner_radius=10)
            self.frame.place(relx=0.8, rely=0.5, anchor="center")

            ctk.CTkLabel(self.frame, text="Reset Password", font=("Arial", 20, "bold")).place(relx=0.5, rely=0.05, anchor="center")

            # Email
            ctk.CTkLabel(self.frame, text="Registered Email", font=("Arial", 14)).place(relx=0.1, rely=0.18)
            self.email_entry = ctk.CTkEntry(self.frame, width=300)
            self.email_entry.place(relx=0.5, rely=0.27, anchor="center")

            # New Password
            ctk.CTkLabel(self.frame, text="New Password", font=("Arial", 14)).place(relx=0.1, rely=0.36)
            self.new_pass_entry = ctk.CTkEntry(self.frame, width=300, show="*")
            self.new_pass_entry.place(relx=0.5, rely=0.45, anchor="center")

            # Confirm Password
            ctk.CTkLabel(self.frame, text="Confirm Password", font=("Arial", 14)).place(relx=0.1, rely=0.53)
            self.confirm_pass_entry = ctk.CTkEntry(self.frame, width=300, show="*")
            self.confirm_pass_entry.place(relx=0.5, rely=0.62, anchor="center")

            # Show password checkbox
            self.show_pass_var = tk.IntVar()
            def toggle_password_visibility():
                show = "" if self.show_pass_var.get() else "*"
                self.new_pass_entry.configure(show=show)
                self.confirm_pass_entry.configure(show=show)

            self.show_password_check = ctk.CTkCheckBox(
                self.frame,
                text="Show Password",
                variable=self.show_pass_var,
                command=toggle_password_visibility
            )
            self.show_password_check.place(relx=0.5, rely=0.72, anchor="center")

            # Reset button
            reset_btn = ctk.CTkButton(self.frame, text="Reset Password", width=200, command=self.reset_password)
            reset_btn.place(relx=0.5, rely=0.83, anchor="center")

            # Back button
            back_btn = ctk.CTkButton(self.frame, text="Back to Login", width=150, command=lambda: self.controller.show_login())
            back_btn.place(relx=0.5, rely=0.92, anchor="center")

            
    def reset_password(self):

        email = self.email_entry.get()
        new_pass = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()

        if not email or not new_pass or not confirm_pass:
            messagebox.showerror("Error", "All fields are required!")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Password validation
        if len(new_pass) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long!")
            return
        if not any(char.isupper() for char in new_pass):
            messagebox.showerror("Error", "Password must contain at least one uppercase letter!")
            return
        if not any(char.islower() for char in new_pass):
            messagebox.showerror("Error", "Password must contain at least one lowercase letter!")
            return
        if not any(char.isdigit() for char in new_pass):
            messagebox.showerror("Error", "Password must contain at least one digit!")
            return
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_pass):
            messagebox.showerror("Error", "Password must contain at least one special character!")
            return

        try:
            db_connection = mysql.connector.connect(
                host="localhost", user="root", password="root@123", database="Vehicle_Service_DB"
            )
            cursor = db_connection.cursor()
            cursor.execute("SELECT userid FROM User WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user:
                messagebox.showerror("Error", "Email not found. Please enter a valid registered email.")
                return

            cursor.execute("UPDATE User SET password = %s WHERE email = %s", (new_pass, email))
            db_connection.commit()
            messagebox.showinfo("Success", "Password has been reset successfully!")
            self.controller.show_login()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

        finally:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()