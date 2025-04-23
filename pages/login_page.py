import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from customtkinter import CTkImage
from models.user import User

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
    

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")  # Show password
        else:
            self.password_entry.configure(show="*")  # Hide password


    def setup_ui(self):
        # Configure the main frame with a light background
        self.configure(width=1200, height=750, fg_color="#F0F2F5")
        
        # Create left side for branding and illustration
        self.left_frame = ctk.CTkFrame(self, width=700, height=750, fg_color="#FFFFFF")
        self.left_frame.place(x=0, y=0)
        
        # Add the main heading
        self.main_heading = ctk.CTkLabel(
            self.left_frame,
            text="Vehicle Service & Maintenance\nManagement System",
            font=("Poppins", 32, "bold"),
            text_color="#1A237E",
            justify="center"
        )
        self.main_heading.place(relx=0.5, rely=0.15, anchor="center")
        
        # Add background image - tow truck illustration
        self.bg_image = Image.open("UI/login_screen.png")
        self.bg_image = self.bg_image.resize((500, 400), Image.LANCZOS)
        self.bg_image = CTkImage(light_image=self.bg_image, dark_image=self.bg_image, size=(500, 400))
        self.bg_label = ctk.CTkLabel(self.left_frame, image=self.bg_image, text="")
        self.bg_label.place(relx=0.5, rely=0.55, anchor="center")

        # Right side container with gradient effect
        self.right_frame = ctk.CTkFrame(
            self,
            width=500,
            height=750,
            corner_radius=0,
            fg_color="#E8EAF6"  # Light indigo background
        )
        self.right_frame.place(x=700, y=0)

        # Add decorative top accent
        self.top_accent = ctk.CTkFrame(
            self.right_frame,
            width=500,
            height=8,
            corner_radius=0,
            fg_color="#1A237E"  # Dark indigo accent
        )
        self.top_accent.place(x=0, y=0)

        # Add decorative circles for visual interest
        circle_colors = ["#3949AB", "#303F9F", "#283593"]
        circle_positions = [(50, 680), (80, 700), (110, 670)]
        circle_sizes = [30, 40, 25]
        
        for pos, color, size in zip(circle_positions, circle_colors, circle_sizes):
            circle = ctk.CTkFrame(
                self.right_frame,
                width=size,
                height=size,
                corner_radius=size//2,
                fg_color=color
            )
            circle.place(x=pos[0], y=pos[1])

        # Login form container with semi-transparent background
        self.login_container = ctk.CTkFrame(
            self.right_frame,
            width=400,
            height=500,
            corner_radius=15,
            fg_color="#FFFFFF",
            border_width=0
        )
        self.login_container.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome text
        self.welcome_text = ctk.CTkLabel(
            self.login_container,
            text="Welcome Back!",
            font=("Poppins", 28, "bold"),
            text_color="#1A237E"
        )
        self.welcome_text.place(relx=0.5, rely=0.05, anchor="center")

        self.subtitle_text = ctk.CTkLabel(
            self.login_container,
            text="Please sign in to continue",
            font=("Poppins", 14),
            text_color="#666666"
        )
        self.subtitle_text.place(relx=0.5, rely=0.12, anchor="center")

        # Username/Email field
        self.username_label = ctk.CTkLabel(
            self.login_container,
            text="Username / Business ID",
            font=("Poppins", 12),
            text_color="#1A237E"
        )
        self.username_label.place(relx=0.1, rely=0.25)
        
        self.username_entry = ctk.CTkEntry(
            self.login_container,
            width=360,
            height=45,
            corner_radius=8,
            border_width=1,
            fg_color="#F8F9FA",
            border_color="#E0E0E0",
            placeholder_text="Enter your username or business ID",
            font=("Poppins", 12)
        )
        self.username_entry.place(relx=0.5, rely=0.35, anchor="center")

        # Password field
        self.password_label = ctk.CTkLabel(
            self.login_container,
            text="Password",
            font=("Poppins", 12),
            text_color="#1A237E"
        )
        self.password_label.place(relx=0.1, rely=0.45)
        
        self.password_entry = ctk.CTkEntry(
            self.login_container,
            width=360,
            height=45,
            corner_radius=8,
            border_width=1,
            fg_color="#F8F9FA",
            border_color="#E0E0E0",
            show="*",
            placeholder_text="Enter your password",
            font=("Poppins", 12)
        )
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")

        # Show Password Checkbox
        self.show_password_var = ctk.BooleanVar()
        self.show_password_checkbox = ctk.CTkCheckBox(
            self.login_container,
            text="Show Password",
            variable=self.show_password_var,
            command=lambda: self.toggle_password_visibility(),
            font=("Poppins", 11),
            text_color="#666666",
            fg_color="#1A237E",
            hover_color="#303F9F"
        )
        self.show_password_checkbox.place(relx=0.1, rely=0.65)

        # Forgot Password
        self.forgot_password_label = ctk.CTkButton(
            self.login_container,
            text="Forgot Password?",
            font=("Poppins", 11),
            cursor="hand2",
            command=lambda: self.controller.show_forgot_password(),
            fg_color="transparent",
            text_color="#1A237E",
            hover_color="#F0F2F5"
        )
        self.forgot_password_label.place(relx=0.65, rely=0.65)

        # Login Button
        self.login_button = ctk.CTkButton(
            self.login_container,
            text="Sign In",
            width=360,
            height=45,
            font=("Poppins", 14, "bold"),
            command=self.login_authenticate,
            fg_color="#1A237E",
            hover_color="#303F9F",
            corner_radius=8
        )
        self.login_button.place(relx=0.5, rely=0.8, anchor="center")

        # Register Button
        self.register_button = ctk.CTkButton(
            self.login_container,
            text="Create New Account",
            width=360,
            height=45,
            font=("Poppins", 14, "bold"),
            fg_color="#FFFFFF",
            text_color="#1A237E",
            border_color="#1A237E",
            border_width=1,
            hover_color="#F0F2F5",
            command=lambda: self.controller.show_registration(),
            corner_radius=8
        )
        self.register_button.place(relx=0.5, rely=0.9, anchor="center")

    def login_authenticate(self):
        email = self.username_entry.get()
        password = self.password_entry.get()

        result = User.authenticate(email, password)
        if result:
            userid, roleid = result
            self.controller.user_id = userid  # Store user_id in controller
            
            if roleid == 1:
                self.controller.show_user_dashboard(email)
            elif roleid == 2:
                self.controller.show_mechanic_dashboard()
            elif roleid == 3:
                self.controller.show_admin_dashboard()
        else:
            tk.messagebox.showerror("Login Failed", "Invalid email or password.") 