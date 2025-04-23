import tkinter as tk
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from tkcalendar import Calendar
from models.user import User
from models.mechanic import Mechanic
from models.appointment import Appointment
from database.config import get_db_connection
from mysql.connector import Error
from datetime import datetime

class UserDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller, email):
        super().__init__(parent)
        self.controller = controller
        self.email = email
        self.setup_ui()

    def get_services_from_db(self):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT servicename FROM Services")
            services = [service[0] for service in cursor.fetchall()]
            cursor.close()
            connection.close()
            return services
        except Exception as e:
            print(f"Error fetching services: {str(e)}")
            return []

    def setup_ui(self):
        # Configure the main frame with light background
        self.configure(width=1200, height=750, fg_color="#F0F2F5")

        # Add main dashboard heading
        self.main_heading = ctk.CTkLabel(
            self,
            text="User Dashboard",
            font=("Poppins", 32, "bold"),
            text_color="#1A237E"
        )
        self.main_heading.place(relx=0.5, rely=0.05, anchor="center")

        # Create left frame for search and results
        self.left_frame = ctk.CTkFrame(
            self,
            width=550,
            height=600,
            corner_radius=15,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E0E0E0"
        )
        self.left_frame.place(x=20, y=80)

        # Search section header
        self.search_header = ctk.CTkLabel(
            self.left_frame,
            text="Search Mechanics",
            font=("Poppins", 28, "bold"),
            text_color="#1A237E"
        )
        self.search_header.place(x=20, y=20)

        # Search form
        # ZIP Code
        self.zip_label = ctk.CTkLabel(
            self.left_frame,
            text="ZIP Code",
            font=("Poppins", 12),
            text_color="#1A237E"
        )
        self.zip_label.place(x=20, y=80)

        self.zip_entry = ctk.CTkEntry(
            self.left_frame,
            width=180,
            height=40,
            corner_radius=8,
            placeholder_text="Enter ZIP code"
        )
        self.zip_entry.place(x=20, y=110)

        # Service Type
        self.service_label = ctk.CTkLabel(
            self.left_frame,
            text="Service Type",
            font=("Poppins", 12),
            text_color="#1A237E"
        )
        self.service_label.place(x=220, y=80)

        services = self.get_services_from_db()
        self.service_dropdown = ctk.CTkComboBox(
            self.left_frame,
            width=180,
            height=40,
            values=services,
            corner_radius=8
        )
        if services:
            self.service_dropdown.set(services[0])
        self.service_dropdown.place(x=220, y=110)

        # Search Button
        self.search_button = ctk.CTkButton(
            self.left_frame,
            text="Search",
            width=110,
            height=40,
            corner_radius=8,
            font=("Poppins", 12),
            fg_color="#1A237E",
            hover_color="#303F9F",
            command=self.search_mechanics
        )
        self.search_button.place(x=420, y=110)

        # Results section
        self.results_label = ctk.CTkLabel(
            self.left_frame,
            text="Available Mechanics",
            font=("Poppins", 16, "bold"),
            text_color="#1A237E"
        )
        self.results_label.place(x=20, y=170)

        # Results container (scrollable)
        self.results_frame = ctk.CTkScrollableFrame(
            self.left_frame,
            width=510,  # Slightly wider
            height=380,
            fg_color="transparent"
        )
        self.results_frame.place(x=10, y=200)  # Moved slightly left

        # Create right frame for bookings
        self.right_frame = ctk.CTkFrame(
            self,
            width=550,
            height=600,
            corner_radius=15,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E0E0E0"
        )
        self.right_frame.place(x=590, y=80)

        # Bookings header
        self.bookings_header = ctk.CTkLabel(
            self.right_frame,
            text="Your Bookings",
            font=("Poppins", 28, "bold"),
            text_color="#1A237E"
        )
        self.bookings_header.place(x=20, y=20)

        # Refresh button
        self.refresh_button = ctk.CTkButton(
            self.right_frame,
            text="Refresh",
            width=100,
            height=32,
            corner_radius=8,
            font=("Poppins", 12),
            fg_color="#1A237E",
            hover_color="#303F9F",
            command=self.load_bookings
        )
        self.refresh_button.place(x=420, y=20)

        # Bookings container (scrollable)
        self.bookings_frame = ctk.CTkScrollableFrame(
            self.right_frame,
            width=510,
            height=520,
            fg_color="transparent"
        )
        self.bookings_frame.place(x=20, y=60)

        # Logout Button
        self.logout_button = ctk.CTkButton(
            self,
            text="Logout",
            width=120,
            height=35,
            corner_radius=8,
            font=("Poppins", 12, "bold"),
            fg_color="#FFFFFF",
            text_color="#1A237E",
            border_color="#1A237E",
            border_width=1,
            hover_color="#E8EAF6",
            command=self.controller.show_login
        )
        self.logout_button.place(x=1020, y=690)

        # Load initial bookings
        self.load_bookings()

    def search_mechanics(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        zip_code = self.zip_entry.get()
        service_type = self.service_dropdown.get()

        if not zip_code:
            tk.messagebox.showerror("Error", "Please enter a ZIP Code!")
            return

        results = Mechanic.search_mechanics(zip_code, service_type)
        if not results:
            no_results = ctk.CTkLabel(
                self.results_frame,
                text="No mechanics found for the given criteria",
                font=("Poppins", 14),
                text_color="#666666"
            )
            no_results.pack(pady=20)
            return

        for mechanic in results:
            self.create_mechanic_card(mechanic)

    def create_mechanic_card(self, mechanic):
        business_name, service_offered, zip_code, vehicle_type = mechanic
        
        # Create card frame with reduced height and better organization
        card = ctk.CTkFrame(
            self.results_frame,
            height=120,  # Reduced from 140 to 120
            corner_radius=10,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E0E0E0"
        )
        card.pack(fill="x", padx=5, pady=5)
        card.pack_propagate(False)

        # Business name - make it shorter if too long
        if len(business_name) > 25:
            display_name = business_name[:22] + "..."
        else:
            display_name = business_name
        
        ctk.CTkLabel(
            card,
            text=display_name,
            font=("Poppins", 14, "bold"),
            text_color="#1A237E",
            anchor="w",
            width=380  # Control the width to prevent overflow
        ).place(x=15, y=15)

        # Left column - service and zip code
        service_label = ctk.CTkLabel(
            card,
            text=f"Service:",
            font=("Poppins", 12, "bold"),
            text_color="#666666",
            anchor="w",
            width=60
        )
        service_label.place(x=15, y=45)
        
        # Truncate service name if too long
        if len(service_offered) > 15:
            display_service = service_offered[:12] + "..."
        else:
            display_service = service_offered
        
        service_value = ctk.CTkLabel(
            card,
            text=display_service,
            font=("Poppins", 12),
            text_color="#666666",
            anchor="w",
            width=120
        )
        service_value.place(x=80, y=45)

        # ZIP Code in left column
        zip_label = ctk.CTkLabel(
            card,
            text=f"ZIP:",
            font=("Poppins", 12, "bold"),
            text_color="#666666",
            anchor="w",
            width=40
        )
        zip_label.place(x=15, y=75)
        
        zip_value = ctk.CTkLabel(
            card,
            text=zip_code,
            font=("Poppins", 12),
            text_color="#666666",
            anchor="w",
            width=80
        )
        zip_value.place(x=60, y=75)

        # Vehicle type in middle column
        vehicle_label = ctk.CTkLabel(
            card,
            text=f"Vehicle:",
            font=("Poppins", 12, "bold"),
            text_color="#666666",
            anchor="w",
            width=60
        )
        vehicle_label.place(x=220, y=45)
        
        # Truncate vehicle type if too long
        if len(vehicle_type) > 10:
            display_vehicle = vehicle_type[:7] + "..."
        else:
            display_vehicle = vehicle_type
        
        vehicle_value = ctk.CTkLabel(
            card,
            text=display_vehicle,
            font=("Poppins", 12),
            text_color="#666666",
            anchor="w",
            width=80
        )
        vehicle_value.place(x=285, y=45)

        # Book button - moved slightly up and right-aligned
        book_button = ctk.CTkButton(
            card,
            text="Book",  # Shortened text
            width=80,     # Smaller width
            height=32,    # Smaller height
            corner_radius=8,
            font=("Poppins", 12),
            fg_color="#1A237E",
            hover_color="#303F9F",
            command=lambda m=mechanic: self.show_booking_section(m)
        )
        book_button.place(x=390, y=45)  # Positioned more carefully

    def show_booking_section(self, mechanic):
        booking_window = ctk.CTkToplevel(self)
        booking_window.title("Book Appointment")
        booking_window.geometry("400x500")
        booking_window.transient(self)
        booking_window.grab_set()

        business_name, service_offered, _, vehicle_type = mechanic

        # Title
        ctk.CTkLabel(
            booking_window,
            text="Book Appointment",
            font=("Poppins", 20, "bold"),
            text_color="#1A237E"
        ).pack(pady=(20, 10))

        # Mechanic details
        ctk.CTkLabel(
            booking_window,
            text=f"Mechanic: {business_name}",
            font=("Poppins", 14)
        ).pack(pady=5)
        ctk.CTkLabel(
            booking_window,
            text=f"Service: {service_offered}",
            font=("Poppins", 14)
        ).pack(pady=5)

        # Calendar
        calendar_label = ctk.CTkLabel(
            booking_window,
            text="Select Date:",
            font=("Poppins", 14)
        )
        calendar_label.pack(pady=(20, 5))
        
        calendar_frame = tk.Frame(booking_window)
        calendar_frame.pack(pady=5)
        
        calendar = Calendar(
            calendar_frame,
            selectmode="day",
            year=2025,
            month=3,
            day=1,
            mindate=datetime.now()
        )
        calendar.pack()

        # Time selection
        time_label = ctk.CTkLabel(
            booking_window,
            text="Select Time:",
            font=("Poppins", 14)
        )
        time_label.pack(pady=(20, 5))

        time_var = tk.StringVar(value="09:00 AM")
        time_slots = ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"]
        
        time_dropdown = ctk.CTkComboBox(
            booking_window,
            values=time_slots,
            variable=time_var,
            width=200,
            height=35
        )
        time_dropdown.pack(pady=5)

        # Confirm button
        confirm_button = ctk.CTkButton(
            booking_window,
            text="Confirm Booking",
            width=200,
            height=40,
            corner_radius=8,
            font=("Poppins", 14),
            fg_color="#1A237E",
            hover_color="#303F9F",
            command=lambda: self.confirm_booking(
                booking_window,
                business_name,
                service_offered,
                calendar.get_date(),
                time_var.get()
            )
        )
        confirm_button.pack(pady=20)

    def confirm_booking(self, window, business_name, service_type, date, time):
        db_connection = None
        cursor = None
        try:
            # Get mechid from business name
            db_connection = get_db_connection()
            cursor = db_connection.cursor()
            
            # Get mechid in a separate query
            cursor.execute("""
                SELECT mechid FROM Mechanic_Businesses 
                WHERE business_name = %s AND approval_status = 'Approved'
            """, (business_name,))
            result = cursor.fetchone()
            cursor.fetchall()  # Clear any unread results
            
            if not result:
                tk.messagebox.showerror("Error", "Could not find approved mechanic business.")
                return
            
            mechid = result[0]
            
            # Close current cursor and connection before creating appointment
            cursor.close()
            db_connection.close()
            
            # Try to create the appointment with a new connection
            success, message = Appointment.create_appointment(
                self.controller.user_id,
                mechid,
                date,
                time,
                service_type
            )
            
            if success:
                tk.messagebox.showinfo("Success", message)
                window.destroy()
                self.load_bookings()  # Refresh bookings list
            else:
                tk.messagebox.showerror("Error", message)
                
        except Error as e:
            tk.messagebox.showerror("Error", f"Failed to book appointment: {str(e)}")
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if db_connection:
                try:
                    db_connection.close()
                except:
                    pass

    def load_bookings(self):
        # Clear existing bookings
        for widget in self.bookings_frame.winfo_children():
            widget.destroy()

        bookings = Appointment.get_user_appointments(self.controller.user_id)
        
        if not bookings:
            no_bookings_label = ctk.CTkLabel(
                self.bookings_frame,
                text="No appointments found",
                font=("Poppins", 14),
                text_color="#666666"
            )
            no_bookings_label.pack(pady=20)
            return

        for booking in bookings:
            mechanic_name, date, service_type, time, status = booking
            
            # Create booking card
            card = ctk.CTkFrame(
                self.bookings_frame,
                height=140,
                corner_radius=10,
                fg_color="#FFFFFF",
                border_width=1,
                border_color="#E0E0E0"
            )
            card.pack(fill="x", padx=5, pady=5)
            card.pack_propagate(False)

            # Mechanic name
            ctk.CTkLabel(
                card,
                text=f"Mechanic: {mechanic_name}",
                font=("Poppins", 14, "bold"),
                text_color="#1A237E"
            ).place(x=15, y=15)

            # Service details
            ctk.CTkLabel(
                card,
                text=f"Service: {service_type}",
                font=("Poppins", 12),
                text_color="#666666"
            ).place(x=15, y=45)

            # Date and Time
            formatted_date = date.strftime('%Y-%m-%d') if isinstance(date, datetime) else date
            formatted_time = time.strftime('%I:%M %p') if isinstance(time, datetime) else time
            
            ctk.CTkLabel(
                card,
                text=f"Date: {formatted_date}",
                font=("Poppins", 12),
                text_color="#666666"
            ).place(x=15, y=75)

            ctk.CTkLabel(
                card,
                text=f"Time: {formatted_time}",
                font=("Poppins", 12),
                text_color="#666666"
            ).place(x=250, y=45)

            # Status with color coding
            status_colors = {
                "Pending": {"fg": "#F57C00", "bg": "#FFF3E0"},
                "In Progress": {"fg": "#1976D2", "bg": "#E3F2FD"},
                "Completed": {"fg": "#388E3C", "bg": "#E8F5E9"},
                "Rejected": {"fg": "#D32F2F", "bg": "#FFEBEE"} 
            }
            
            status_frame = ctk.CTkFrame(
                card,
                width=100,
                height=28,
                corner_radius=14,
                fg_color=status_colors[status]["bg"]
            )
            status_frame.place(x=250, y=75)
            status_frame.pack_propagate(False)

            ctk.CTkLabel(
                status_frame,
                text=status,
                font=("Poppins", 12),
                text_color=status_colors[status]["fg"]
            ).place(relx=0.5, rely=0.5, anchor="center")