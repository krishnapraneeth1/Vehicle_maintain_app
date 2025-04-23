import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageEnhance
from customtkinter import CTkImage
from models.user import User
import re
from tkinter import messagebox
from models.mechanic import Mechanic
from tkinter import ttk

class RegistrationPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.service_options = self.fetch_services()  # Fetch available services
        self.setup_ui()

    def fetch_services(self):
        try:
            from database.config import get_db_connection
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT serviceid, servicename, typeofvehicle FROM services")
            services = cursor.fetchall()
            cursor.close()
            connection.close()
            return services
        except Exception as e:
            print(f"Error fetching services: {str(e)}")
            return []

    def setup_ui(self):
        # Configure the main frame
        self.configure(width=1200, height=750, fg_color="#F0F2F5")

        # Create header frame
        self.header_frame = ctk.CTkFrame(self, width=1200, height=250, fg_color="transparent")
        self.header_frame.place(x=0, y=0)
        
        # Add header image with proper sizing and darkening effect
        self.bg_image = Image.open("UI/RegisterationFrame.jpg")
        # Resize to maintain aspect ratio and cover the header area
        self.bg_image = self.bg_image.resize((1200, 250), Image.LANCZOS)
        # Darken the image slightly for better text visibility
        enhancer = ImageEnhance.Brightness(self.bg_image)
        self.bg_image = enhancer.enhance(0.7)  # Reduce brightness to 70%
        self.bg_image = CTkImage(light_image=self.bg_image, dark_image=self.bg_image, size=(1200, 250))
        
        # Place header image
        self.bg_label = ctk.CTkLabel(self.header_frame, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0)

        # Create a semi-transparent frame for text background
        self.text_bg_frame = ctk.CTkFrame(
            self.header_frame,
            width=600,
            height=120,
            fg_color="#000000",
            corner_radius=10
        )
        self.text_bg_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create a canvas for the semi-transparent effect
        self.canvas = tk.Canvas(
            self.text_bg_frame,
            width=600,
            height=120,
            highlightthickness=0,
            bg="#000000"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0, 0, 600, 120, fill="#000000", stipple="gray50")

        # Header Title with shadow effect
        self.header_title = ctk.CTkLabel(
            self.text_bg_frame,
            text="Create Your Account",
            font=("Poppins", 36, "bold"),
            text_color="#FFFFFF"
        )
        self.header_title.place(relx=0.5, rely=0.4, anchor="center")

        # Add a subtitle
        self.header_subtitle = ctk.CTkLabel(
            self.text_bg_frame,
            text="Join our vehicle service management system",
            font=("Poppins", 14),
            text_color="#E0E0E0"
        )
        self.header_subtitle.place(relx=0.5, rely=0.7, anchor="center")

        # Main Registration Container
        self.main_frame = ctk.CTkFrame(
            self,
            width=1000,
            height=450,
            corner_radius=15,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E0E0E0"
        )
        self.main_frame.place(relx=0.5, rely=0.6, anchor="center")

        # Left Column
        # Personal Information Section Title
        self.personal_info_title = ctk.CTkLabel(
            self.main_frame,
            text="Personal Information",
            font=("Poppins", 16, "bold"),
            text_color="#1B2559"
        )
        self.personal_info_title.place(relx=0.05, rely=0.05)

        # User Details with modern styling
        self.fname_label = ctk.CTkLabel(self.main_frame, text="First Name", font=("Poppins", 12), text_color="#1B2559")
        self.fname_label.place(relx=0.05, rely=0.15)
        self.fname_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter your first name"
        )
        self.fname_entry.place(relx=0.05, rely=0.22)

        self.lname_label = ctk.CTkLabel(self.main_frame, text="Last Name", font=("Poppins", 12), text_color="#1B2559")
        self.lname_label.place(relx=0.05, rely=0.32)
        self.lname_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter your last name"
        )
        self.lname_entry.place(relx=0.05, rely=0.39)

        self.email_label = ctk.CTkLabel(self.main_frame, text="Email", font=("Poppins", 12), text_color="#1B2559")
        self.email_label.place(relx=0.05, rely=0.49)
        self.email_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter your email"
        )
        self.email_entry.place(relx=0.05, rely=0.56)

        self.phone_label = ctk.CTkLabel(self.main_frame, text="Phone Number", font=("Poppins", 12), text_color="#1B2559")
        self.phone_label.place(relx=0.05, rely=0.66)
        self.phone_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter your phone number"
        )
        self.phone_entry.place(relx=0.05, rely=0.73)

        # Center Column
        # Address Information Section Title
        self.address_info_title = ctk.CTkLabel(
            self.main_frame,
            text="Address Information",
            font=("Poppins", 16, "bold"),
            text_color="#1B2559"
        )
        self.address_info_title.place(relx=0.38, rely=0.05)

        self.address_label = ctk.CTkLabel(self.main_frame, text="Address", font=("Poppins", 12), text_color="#1B2559")
        self.address_label.place(relx=0.38, rely=0.15)
        self.address_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter your address"
        )
        self.address_entry.place(relx=0.38, rely=0.22)

        self.city_label = ctk.CTkLabel(self.main_frame, text="City", font=("Poppins", 12), text_color="#1B2559")
        self.city_label.place(relx=0.38, rely=0.32)
        self.city_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter your city"
        )
        self.city_entry.place(relx=0.38, rely=0.39)

        self.state_label = ctk.CTkLabel(self.main_frame, text="State", font=("Poppins", 12), text_color="#1B2559")
        self.state_label.place(relx=0.38, rely=0.49)
        self.state_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter your state"
        )
        self.state_entry.place(relx=0.38, rely=0.56)

        self.zip_label = ctk.CTkLabel(self.main_frame, text="ZIP Code", font=("Poppins", 12), text_color="#1B2559")
        self.zip_label.place(relx=0.38, rely=0.66)
        self.zip_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter ZIP code"
        )
        self.zip_entry.place(relx=0.38, rely=0.73)

        # Right Column
        # Account Information Section Title
        self.account_info_title = ctk.CTkLabel(
            self.main_frame,
            text="Account Information",
            font=("Poppins", 16, "bold"),
            text_color="#1B2559"
        )
        self.account_info_title.place(relx=0.71, rely=0.05)

        self.password_label = ctk.CTkLabel(self.main_frame, text="Password", font=("Poppins", 12), text_color="#1B2559")
        self.password_label.place(relx=0.71, rely=0.15)

        # Password field with eye icon
        self.show_password = False
        self.password_frame = ctk.CTkFrame(
            self.main_frame,
            width=250,
            height=40,
            fg_color="transparent"
        )
        self.password_frame.place(relx=0.71, rely=0.22)
        
        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            width=220,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            show="*",
            placeholder_text="Enter your password"
        )
        self.password_entry.place(x=0, y=0)

        self.eye_icon = CTkImage(light_image=Image.open("UI/hidden.png"), dark_image=Image.open("UI/hidden.png"), size=(20, 20))
        self.toggle_password_btn = ctk.CTkButton(
            self.password_frame,
            width=30,
            height=40,
            image=self.eye_icon,
            command=self.toggle_password_visibility,  # This should call toggle_password_visibility, not toggle_confirm_password_visibility
            fg_color="transparent",
            hover_color="#F0F2F5"
        )
        self.toggle_password_btn.place(x=220, y=0)

        self.confirm_password_label = ctk.CTkLabel(self.main_frame, text="Confirm Password", font=("Poppins", 12), text_color="#1B2559")
        self.confirm_password_label.place(relx=0.71, rely=0.32)

        # Confirm Password field with eye icon
        self.show_confirm_password = False
        self.confirm_password_frame = ctk.CTkFrame(
            self.main_frame,
            width=250,
            height=40,
            fg_color="transparent"
        )
        self.confirm_password_frame.place(relx=0.71, rely=0.39)
        
        self.confirm_password_entry = ctk.CTkEntry(
            self.confirm_password_frame,
            width=220,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            show="*",
            placeholder_text="Confirm your password"
        )
        self.confirm_password_entry.place(x=0, y=0)

        # Replace text with an image for the toggle button
        self.eye_icon = CTkImage(light_image=Image.open("UI/hidden.png"), dark_image=Image.open("UI/hidden.png"), size=(20, 20))
        self.toggle_confirm_password_btn = ctk.CTkButton(
            self.confirm_password_frame,
            width=30,
            height=40,
            image=self.eye_icon,
            command=self.toggle_confirm_password_visibility,
            fg_color="transparent",
            hover_color="#F0F2F5"
        )
        self.toggle_confirm_password_btn.place(x=220, y=0)

        # Mechanic Selection with modern styling
        self.mechanic_label = ctk.CTkLabel(
            self.main_frame,
            text="Account Type",
            font=("Poppins", 12),
            text_color="#1B2559"
        )
        self.mechanic_label.place(relx=0.71, rely=0.49)
        
        self.mechanic_check = ctk.CTkCheckBox(
            self.main_frame,
            text="Register as Mechanic",
            font=("Poppins", 12),
            command=self.toggle_mechanic_fields,
            fg_color="#1B2559",
            hover_color="#2D3867",
            text_color="#1B2559"
        )
        self.mechanic_check.place(relx=0.71, rely=0.56)

        # Mechanic Fields (Initially Hidden)
        self.business_label = ctk.CTkLabel(
            self.main_frame,
            text="Business Name",
            font=("Poppins", 12),
            text_color="#1B2559"
        )
        self.business_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter business name"
        )

        self.business_id_label = ctk.CTkLabel(
            self.main_frame,
            text="Business ID",
            font=("Poppins", 12),
            text_color="#1B2559"
        )
        self.business_id_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter business ID"
        )

        # Register button
        self.register_button = ctk.CTkButton(
            self,
            text="Register",
            width=200,
            height=45,
            corner_radius=8,
            font=("Poppins", 14, "bold"),
            fg_color="#1B2559",
            hover_color="#2D3867",
            command=self.register_user  # This is using register_user, not register_mechanic
        )
        self.register_button.place(relx=0.65, rely=0.94, anchor="center")

        self.login_button = ctk.CTkButton(
            self,
            text="Back to Login",
            width=200,
            height=45,
            corner_radius=8,
            font=("Poppins", 14, "bold"),
            fg_color="transparent",
            text_color="#1B2559",
            border_color="#1B2559",
            border_width=1,
            hover_color="#F0F2F5",
            command=self.controller.show_login
        )
        self.login_button.place(relx=0.35, rely=0.94, anchor="center")

    def toggle_mechanic_fields(self):
        if self.mechanic_check.get():
            self.business_label.place(relx=0.71, rely=0.66)
            self.business_entry.place(relx=0.71, rely=0.73)
            self.business_id_label.place(relx=0.71, rely=0.79)
            self.business_id_entry.place(relx=0.71, rely=0.86)
        else:
            self.business_label.place_forget()
            self.business_entry.place_forget()
            self.business_id_label.place_forget()
            self.business_id_entry.place_forget()
            self.business_entry.delete(0, 'end')
            self.business_id_entry.delete(0, 'end')

    def toggle_password_visibility(self):
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "*")
        # Update the icon based on visibility state
        self.toggle_password_btn.configure(
            image=CTkImage(light_image=Image.open("UI/visible.png" if self.show_password else "UI/hidden.png"), 
                           dark_image=Image.open("UI/visible.png" if self.show_password else "UI/hidden.png"), 
                           size=(20, 20))
        )

    def toggle_confirm_password_visibility(self):
        self.show_confirm_password = not self.show_confirm_password
        self.confirm_password_entry.configure(show="" if self.show_confirm_password else "*")
        # Update the icon based on visibility state
        self.toggle_confirm_password_btn.configure(
            image=CTkImage(light_image=Image.open("UI/visible.png" if self.show_confirm_password else "UI/hidden.png"), 
                           dark_image=Image.open("UI/visible.png" if self.show_confirm_password else "UI/hidden.png"), 
                           size=(20, 20))
        )

    def register_user(self):
        try:
            firstname = self.fname_entry.get()
            lastname = self.lname_entry.get()
            email = self.email_entry.get().lower()
            phoneno = self.phone_entry.get()
            password = self.password_entry.get()
            confirm_password = self.confirm_password_entry.get()
            address = self.address_entry.get()
            city = self.city_entry.get()
            state = self.state_entry.get()
            zipcode = self.zip_entry.get()
            is_mechanic = self.mechanic_check.get()

            # Check for empty fields
            if not firstname or not lastname or not email or not phoneno or not password or not confirm_password or not address or not city or not state or not zipcode:
                tk.messagebox.showerror("Error", "All fields must be filled!")
                return

            # Validate email format
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                tk.messagebox.showerror("Error", "Invalid email format!")
                return

            # Validate phone number (10 digits)
            if not phoneno.isdigit() or len(phoneno) != 10:
                tk.messagebox.showerror("Error", "Phone number must be 10 digits!")
                return

            # Validate password (minimum 8 characters, at least one uppercase, one lowercase, one digit, and one special character)
            password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
            if not re.match(password_regex, password):
                tk.messagebox.showerror(
                    "Error",
                    "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a digit, and a special character!"
                )
                return

            # Check if passwords match
            if password != confirm_password:
                tk.messagebox.showerror("Error", "Passwords do not match!")
                return

            # Validate zip code (5 digits)
            if not zipcode.isdigit() or len(zipcode) != 5:
                tk.messagebox.showerror("Error", "Zip code must be 5 digits!")
                return

            # Validate city and state (only alphabetic characters)
            if not city.replace(" ", "").isalpha():
                tk.messagebox.showerror("Error", "City must contain only alphabetic characters!")
                return

            if not state.replace(" ", "").isalpha():
                tk.messagebox.showerror("Error", "State must contain only alphabetic characters!")
                return

            # If registering as mechanic, check for business name
            if is_mechanic:
                business_name = self.business_entry.get()
                business_id = self.business_id_entry.get()
                if not business_name or not business_id:
                    tk.messagebox.showerror("Error", "Business name and Business ID are required for mechanic registration!")
                    return
                try:
                    from models.mechanic import Mechanic
                    if Mechanic.register_mechanic(
                        firstname=firstname,
                        lastname=lastname,
                        email=email,
                        password=password,
                        phoneno=phoneno,
                        address1=address,
                        city=city,
                        state=state,
                        zipcode=zipcode,
                        business_name=business_name,
                        serviceid=business_id
                    ):
                        tk.messagebox.showinfo("Success", "Your mechanic account has been created successfully. An admin will review your application.")
                        # Ensure this line executes after the message box is closed
                        self.controller.show_login()
                    else:
                        tk.messagebox.showerror("Error", "Mechanic registration failed. Please try again.")
                except Exception as e:
                    tk.messagebox.showerror("Error", f"Mechanic registration failed: {str(e)}")
            else:
                # Determine role ID based on email and mechanic status
                if "admin" in email:
                    roleid = 3  # Admin role
                else:
                    roleid = 2 if is_mechanic else 1  # 2 for mechanic, 1 for regular user
                
                # Print for debugging
                print(f"Attempting to register user with email: {email}, role: {roleid}")
                
                from database.config import get_db_connection
                connection = get_db_connection()
                if connection is None:
                    tk.messagebox.showerror("Error", "Could not connect to database")
                    return
                    
                user_id = User.register(firstname, lastname, email, password, phoneno, address, city, state, zipcode, roleid)
                
                if user_id:
                    success_message = "Registration Successful! "
                    if roleid == 3:
                        success_message += "Your admin account is ready to use."
                    else:
                        success_message += "Please log in."
                    tk.messagebox.showinfo("Success", success_message)
                    self.controller.show_login()
                else:
                    tk.messagebox.showerror("Error", "Registration failed. Please try again.")
                    
        except AttributeError as e:
            tk.messagebox.showerror("Error", f"Attribute error: {str(e)}")
        except Exception as e:
            if "Duplicate entry" in str(e) and "user.email" in str(e):
                tk.messagebox.showerror("Error", "This email is already registered. Please use a different email or log in.")
            else:
                tk.messagebox.showerror("Error", f"Registration failed: {str(e)}")
                print(f"Registration error: {str(e)}")

    def register_mechanic(self):
        # Get input values
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zipcode = self.zipcode_entry.get()
        business_name = self.business_name_entry.get()
        service_id = self.selected_service_id
        
        # Validate inputs
        if not all([firstname, lastname, email, password, confirm_password, 
                    phone, address, city, state, zipcode, business_name, service_id]):
            messagebox.showerror("Registration Error", "All fields are required")
            return
            
        if password != confirm_password:
            messagebox.showerror("Registration Error", "Passwords do not match")
            return
        
        # Call the registration method from Mechanic model
        success = Mechanic.register_mechanic(
            firstname, lastname, email, password, phone, 
            address, city, state, zipcode, business_name, service_id
        )
        
        if success:
            messagebox.showinfo("Registration Successful", 
                "Your mechanic account has been created successfully.")
            # Navigate back to login page after successful registration
            self.controller.show_login()
        else:
            messagebox.showerror("Registration Error", 
                "Failed to register. Please try again or contact support.")

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_frame = None
        self.show_login()

    def clear_frame(self):
        """Clears the current frame from the window."""
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def show_login(self):
        """Displays the login page."""
        self.clear_frame()
        from pages.login_page import LoginPage
        self.current_frame = LoginPage(self, self)
        self.current_frame.pack(fill="both", expand=True)

    def show_registration(self):
        """Displays the registration page."""
        self.clear_frame()
        from pages.registration_page import RegistrationPage
        self.current_frame = RegistrationPage(self, self)
        self.current_frame.pack(fill="both", expand=True)