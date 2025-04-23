import tkinter as tk
import customtkinter as ctk
from database.config import init_db
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.forgot_password import forgotpassword
from pages.user_dashboard import UserDashboard
from pages.mechanic_dashboard import MechanicDashboard
from pages.admin_dashboard import AdminDashboard

class VehicleServiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize database
        init_db()
        
        # Configure window
        self.geometry("1200x750")
        self.resizable(False, False)
        self.title("Vehicle Service & Maintenance Management System")
        
        # Configure appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Initialize user_id
        self.user_id = None
        
        # Show login screen
        self.show_login()

    def clear_frame(self):
        for widget in self.winfo_children():
            try:
                widget.destroy()
            except Exception as e:
                print(f"Skipping widget destruction due to: {e}")



    def show_login(self):
        """
        Shows the login page after clearing the current UI
        """
        print("Navigating to login page...")  # Debug output
        self.clear_frame()  # Use consistent clearing method
        from pages.login_page import LoginPage
        LoginPage(self, self).pack(fill="both", expand=True)


    def show_forgot_password(self):
        self.clear_frame()
        self.title("Forgot Password")  # This is correct here, since `self` is the main window
        forgotpassword(self, self).pack(fill="both", expand=True)


  # or whatever your register screen class is

    def show_registration(self):
        self.clear_frame()
        RegistrationPage(self, self).pack(fill="both", expand=True)


    def show_user_dashboard(self, email):
        self.clear_window()
        UserDashboard(self, self, email).pack(fill="both", expand=True)

    def show_mechanic_dashboard(self):
        self.clear_window()
        MechanicDashboard(self, self).pack(fill="both", expand=True)

    def show_admin_dashboard(self):
        self.clear_window()
        AdminDashboard(self, self).pack(fill="both", expand=True)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = VehicleServiceApp()
    app.mainloop()