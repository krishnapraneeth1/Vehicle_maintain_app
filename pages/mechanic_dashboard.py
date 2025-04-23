import tkinter as tk
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from models.mechanic import Mechanic
from models.appointment import Appointment
from database.config import get_db_connection
from datetime import datetime

class MechanicDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.mechanic_details = self.get_mechanic_details()
        self.setup_ui()

    def get_mechanic_details(self):
        try:
            db_connection = get_db_connection()
            cursor = db_connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT business_name, zipcode 
                FROM mechanics 
                WHERE userid = %s
            """, (self.controller.user_id,))
            details = cursor.fetchone()
            cursor.close()
            db_connection.close()
            return details
        except Exception as e:
            print(f"Error fetching mechanic details: {str(e)}")
            return None

    def setup_ui(self):
        # Configure the main frame with light background
        self.configure(width=1200, height=700, fg_color="#F0F2F5")

        # Add main dashboard heading (centered)
        self.main_heading = ctk.CTkLabel(
            self,
            text="Mechanic's Dashboard",
            font=("Poppins", 32, "bold"),
            text_color="#1A237E"
        )
        self.main_heading.place(relx=0.5, rely=0.05, anchor="center")

        # Create left side for bookings with adjusted position
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

        # Bookings header
        self.bookings_header = ctk.CTkLabel(
            self.left_frame,
            text="Current Bookings",
            font=("Poppins", 28, "bold"),
            text_color="#1A237E"
        )
        self.bookings_header.place(x=20, y=20)

        self.bookings_subtitle = ctk.CTkLabel(
            self.left_frame,
            text="View and manage your service appointments",
            font=("Poppins", 14),
            text_color="#666666"
        )
        self.bookings_subtitle.place(x=20, y=60)

        # Add a refresh button with modern styling
        self.refresh_button = ctk.CTkButton(
            self.left_frame,
            text="Refresh",
            width=100,
            height=32,
            corner_radius=8,
            font=("Poppins", 12),
            fg_color="#1A237E",
            hover_color="#303F9F",
            command=self.show_appointments
        )
        self.refresh_button.place(x=420, y=20)

        # Create bookings container frame (scrollable)
        self.bookings_frame = ctk.CTkScrollableFrame(
            self.left_frame,
            width=510,
            height=500,
            fg_color="transparent"
        )
        self.bookings_frame.place(x=20, y=100)

        # Create right side for registration form with improved styling
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

        # Add decorative top accent
        self.top_accent = ctk.CTkFrame(
            self.right_frame,
            width=550,
            height=8,
            corner_radius=0,
            fg_color="#1A237E"
        )
        self.top_accent.place(x=0, y=0)

        # Registration header with improved styling
        self.register_header = ctk.CTkLabel(
            self.right_frame,
            text="Business Registration",
            font=("Poppins", 28, "bold"),
            text_color="#1A237E"
        )
        self.register_header.place(relx=0.5, rely=0.1, anchor="center")

        self.register_subtitle = ctk.CTkLabel(
            self.right_frame,
            text="Complete your business profile",
            font=("Poppins", 14),
            text_color="#666666"
        )
        self.register_subtitle.place(relx=0.5, rely=0.15, anchor="center")

        # Registration form fields with improved spacing and styling
        y_offset = 0.25  # Starting y position (relative)
        field_height = 0.11  # Increased height between fields (relative)

        # Business Name
        self.business_name_label = ctk.CTkLabel(
            self.right_frame,
            text="Business Name",
            font=("Poppins", 12),
            text_color="#1A237E"
        )
        self.business_name_label.place(relx=0.1, rely=y_offset)
        
        self.business_name_entry = ctk.CTkEntry(
            self.right_frame,
            width=450,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter your business name",
            font=("Poppins", 12)
        )
        self.business_name_entry.place(relx=0.1, rely=y_offset + 0.04)  # Increased gap between label and entry
        
        # Set business name if available
        if self.mechanic_details and self.mechanic_details['business_name']:
            self.business_name_entry.insert(0, self.mechanic_details['business_name'])
            self.business_name_entry.configure(state="disabled")

        # Zip Code
        y_offset += field_height
        self.zip_code_label = ctk.CTkLabel(
            self.right_frame,
            text="ZIP Code",
            font=("Poppins", 12),
            text_color="#1A237E"
        )
        self.zip_code_label.place(relx=0.1, rely=y_offset)
        
        self.zip_code_entry = ctk.CTkEntry(
            self.right_frame,
            width=450,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            fg_color="#FFFFFF",
            placeholder_text="Enter ZIP code",
            font=("Poppins", 12)
        )
        self.zip_code_entry.place(relx=0.1, rely=y_offset + 0.04)
        
        # Set zip code if available
        if self.mechanic_details and self.mechanic_details['zipcode']:
            self.zip_code_entry.insert(0, self.mechanic_details['zipcode'])
            self.zip_code_entry.configure(state="disabled")

        # Service Type
        y_offset += field_height
        self.service_type_label = ctk.CTkLabel(
            self.right_frame,
            text="Service Type Offered",
            font=("Poppins", 12),
            text_color="#1A237E"
        )
        self.service_type_label.place(relx=0.1, rely=y_offset)
        
        # Get available services from database
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        cursor.execute("SELECT serviceid, servicename, typeofvehicle FROM Services")
        services = cursor.fetchall()
        cursor.close()
        db_connection.close()

        # Create dictionary of service names to IDs
        self.service_to_id = {service[1]: service[0] for service in services}
        service_names = list(self.service_to_id.keys())

        # Create a frame for the listbox and scrollbar with a light blue background
        self.service_frame = ctk.CTkFrame(
            self.right_frame,
            width=450,
            height=120,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E0E0E0",
            corner_radius=8
        )
        self.service_frame.place(relx=0.1, rely=y_offset + 0.04)
        self.service_frame.pack_propagate(False)

        # Get already registered services
        registered_services = Mechanic.get_registered_services(self.controller.user_id)

        # Create multi-select listbox
        self.service_listbox = tk.Listbox(
            self.service_frame,
            selectmode=tk.MULTIPLE,
            font=("Poppins", 11),
            relief="flat",
            bg="#FFFFFF",
            fg="#1A237E",
            selectbackground="#E8EAF6",
            selectforeground="#1A237E",
            activestyle="none",
            height=6
        )
        self.service_listbox.pack(side="left", fill="both", expand=True)

        # Add scrollbar
        scrollbar = tk.Scrollbar(self.service_frame, orient="vertical", command=self.service_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.service_listbox.config(yscrollcommand=scrollbar.set)

        # Insert services into listbox
        for service in service_names:
            self.service_listbox.insert(tk.END, service)
            if service in registered_services:
                last_idx = self.service_listbox.size() - 1
                self.service_listbox.itemconfig(last_idx, {'bg': '#F0F2F5', 'fg': '#888888'})
                self.service_listbox.selection_set(last_idx)
                self.service_listbox.activate(last_idx)

        # Vehicle Type - Adjusted position
        y_offset += field_height + 0.15  # Added extra space to prevent overlap
        self.vehicle_type_label = ctk.CTkLabel(
            self.right_frame,
            text="Type of Vehicles Serviced",
            font=("Poppins", 12),
            text_color="#1A237E"
        )
        self.vehicle_type_label.place(relx=0.1, rely=y_offset)
        
        self.vehicle_type_dropdown = ctk.CTkComboBox(
            self.right_frame,
            width=450,
            height=40,
            values=["Cars", "Bikes", "Trucks"],
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            button_color="#1A237E",
            button_hover_color="#303F9F",
            dropdown_hover_color="#E8EAF6",
            font=("Poppins", 12)
        )
        self.vehicle_type_dropdown.place(relx=0.1, rely=y_offset + 0.04)

        # Submit Button with improved styling
        self.submit_button = ctk.CTkButton(
            self.right_frame,
            text="Submit Registration",
            width=400,
            height=40,
            corner_radius=8,
            font=("Poppins", 14, "bold"),
            fg_color="#1A237E",
            hover_color="#303F9F",
            command=self.submit_business
        )
        self.submit_button.place(relx=0.15, rely=0.85)

        # Logout Button with adjusted position
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
        self.logout_button.place(x=1020, y=680)  # Moved further down

        # Load initial appointments
        self.show_appointments()

    def submit_business(self):
        business_name = self.business_name_entry.get()
        selected_indices = self.service_listbox.curselection()
        vehicle_type = self.vehicle_type_dropdown.get()
        zip_code = self.zip_code_entry.get()

        if not business_name or not selected_indices or not vehicle_type or not zip_code:
            tk.messagebox.showerror("Error", "All fields must be filled!")
            return

        # Get selected services
        selected_services = [self.service_listbox.get(i) for i in selected_indices]
        
        # Get already registered services
        registered_services = Mechanic.get_registered_services(self.controller.user_id)
        
        # Filter out already registered services
        new_services = [service for service in selected_services if service not in registered_services]
        
        if not new_services:
            tk.messagebox.showinfo("Info", "All selected services are already registered!")
            return

        # Get mechanic details first
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        success = True
        
        try:
            # Check if mechanic exists
            cursor.execute("SELECT mechid FROM mechanics WHERE userid = %s", (self.controller.user_id,))
            mechanic = cursor.fetchone()
            
            if not mechanic:
                # Get user details to register mechanic
                cursor.execute("SELECT firstname, lastname, email, password, phoneno, address1, city, state, zipcode FROM User WHERE userid = %s", 
                             (self.controller.user_id,))
                user = cursor.fetchone()
                
                if not user:
                    tk.messagebox.showerror("Error", "User details not found!")
                    return
                    
                # Register mechanic first with the first new service
                if not Mechanic.register_mechanic(
                    firstname=user[0],
                    lastname=user[1],
                    email=user[2],
                    password=user[3],
                    phoneno=user[4],
                    address1=user[5],
                    city=user[6],
                    state=user[7],
                    zipcode=user[8],
                    business_name=business_name,
                    service_id=self.service_to_id[new_services[0]]
                ):
                    tk.messagebox.showerror("Error", "Failed to register mechanic. Please try again.")
                    return

            # Register each new service
            for service in new_services:
                service_id = self.service_to_id.get(service)
                if not Mechanic.register_business(
                    self.controller.user_id,
                    business_name,
                    service_id,
                    zip_code,
                    service,
                    vehicle_type
                ):
                    success = False
                    break

            if success:
                tk.messagebox.showinfo("Success", "Services Submitted! Waiting for Admin Approval.")
                
                # Mark newly submitted services as selected and disabled in the listbox
                for service in new_services:
                    idx = list(self.service_to_id.keys()).index(service)
                    self.service_listbox.itemconfig(idx, {'bg': '#F0F2F5', 'fg': '#888888'})
                    self.service_listbox.selection_set(idx)
                    
                # Disable other form fields
                self.business_name_entry.configure(state="disabled")
                self.zip_code_entry.configure(state="disabled")
                self.vehicle_type_dropdown.configure(state="disabled")
            else:
                tk.messagebox.showerror("Error", "Registration failed. Please try again.")
                
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            cursor.close()
            db_connection.close()

    def show_appointments(self):
        # Clear existing appointments
        for widget in self.bookings_frame.winfo_children():
            widget.destroy()

        appointments = Appointment.get_mechanic_appointments(self.controller.user_id)
        
        if not appointments:
            no_bookings_label = ctk.CTkLabel(
                self.bookings_frame,
                text="No appointments found",
                font=("Poppins", 14),
                text_color="#666666"
            )
            no_bookings_label.pack(pady=20)
            return

        for appointment in appointments:
            time, customer, service_type, date, status, appointment_id = appointment
            
            # Create appointment card with increased height for two buttons
            card = ctk.CTkFrame(
                self.bookings_frame,
                height=160,  # Increased height from 140 to 160
                corner_radius=10,
                fg_color="#FFFFFF",
                border_width=1,
                border_color="#E0E0E0"
            )
            card.pack(fill="x", padx=5, pady=5)
            card.pack_propagate(False)

            # Customer info
            ctk.CTkLabel(
                card,
                text=f"Customer: {customer}",
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
            ctk.CTkLabel(
                card,
                text=f"Date: {date.strftime('%Y-%m-%d') if isinstance(date, datetime) else date}",
                font=("Poppins", 12),
                text_color="#666666"
            ).place(x=15, y=75)

            ctk.CTkLabel(
                card,
                text=f"Time: {time}",
                font=("Poppins", 12),
                text_color="#666666"
            ).place(x=250, y=45)

            # Status with color coding - add "Rejected" status
            status_colors = {
                "Pending": {"fg": "#F57C00", "bg": "#FFF3E0"},
                "In Progress": {"fg": "#1976D2", "bg": "#E3F2FD"},
                "Completed": {"fg": "#388E3C", "bg": "#E8F5E9"},
                "Rejected": {"fg": "#D32F2F", "bg": "#FFEBEE"}  # Added Rejected status
            }
            
            # Use get() with default to handle any unknown status
            status_color = status_colors.get(status, {"fg": "#757575", "bg": "#F5F5F5"})
            
            status_frame = ctk.CTkFrame(
                card,
                width=100,
                height=28,
                corner_radius=14,
                fg_color=status_color["bg"]
            )
            status_frame.place(x=250, y=75)
            status_frame.pack_propagate(False)

            ctk.CTkLabel(
                status_frame,
                text=status,
                font=("Poppins", 12),
                text_color=status_color["fg"]
            ).place(relx=0.5, rely=0.5, anchor="center")

            # Action buttons based on status
            if status == "Pending":
                # Show both Accept and Reject buttons for pending appointments
                # Accept button - positioned on the right
                ctk.CTkButton(
                    card,
                    text="Accept",
                    width=90,
                    height=35,
                    corner_radius=8,
                    font=("Poppins", 12),
                    fg_color="#1A237E",  # Blue
                    hover_color="#303F9F",
                    command=lambda aid=appointment_id: self.update_appointment_status(aid, "In Progress")
                ).place(x=400, y=45)
                
                # Add Reject button - positioned below the Accept button
                ctk.CTkButton(
                    card,
                    text="Reject",
                    width=90,
                    height=35,
                    corner_radius=8,
                    font=("Poppins", 12),
                    fg_color="#D32F2F",  # Red color for reject
                    hover_color="#B71C1C",
                    command=lambda aid=appointment_id: self.update_appointment_status(aid, "Rejected")
                ).place(x=400, y=90)
                
            elif status == "In Progress":
                # Show only Complete button for in-progress appointments
                ctk.CTkButton(
                    card,
                    text="Complete",
                    width=90,
                    height=35,
                    corner_radius=8,
                    font=("Poppins", 12),
                    fg_color="#1A237E",
                    hover_color="#303F9F",
                    command=lambda aid=appointment_id: self.update_appointment_status(aid, "Completed")
                ).place(x=400, y=60)

    def update_appointment_status(self, appointment_id, status):
        if Appointment.update_appointment_status(appointment_id, status):
            tk.messagebox.showinfo("Success", f"Appointment {status} successfully!")
            self.show_appointments()
        else:
            tk.messagebox.showerror("Error", "Failed to update appointment status.")

class AppointmentsWindow(tk.Toplevel):
    def __init__(self, parent, appointments, mechid):
        super().__init__(parent)
        self.title("View & Approve Appointments")
        self.geometry("800x600")
        self.mechid = mechid
        self.setup_ui(appointments)

    def setup_ui(self, appointments):
        # Create Treeview
        self.tree = tk.ttk.Treeview(
            self, 
            columns=("Time", "Customer", "Vehicle", "Service", "Status", "AppointmentID"),
            show="headings"
        )

        # Configure columns
        self.tree.heading("Time", text="Time")
        self.tree.heading("Customer", text="Customer")
        self.tree.heading("Vehicle", text="Vehicle Type")
        self.tree.heading("Service", text="Service")
        self.tree.heading("Status", text="Status")
        self.tree.heading("AppointmentID", text="Appointment ID")

        self.tree.column("Time", width=100)
        self.tree.column("Customer", width=150)
        self.tree.column("Vehicle", width=100)
        self.tree.column("Service", width=100)
        self.tree.column("Status", width=100)
        self.tree.column("AppointmentID", width=0, stretch=tk.NO)  # Hidden column

        # Add scrollbar
        scrollbar = tk.ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Pack widgets
        self.tree.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate data
        for appointment in appointments:
            self.tree.insert("", "end", values=appointment)

        # Action buttons frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # Approve and Reject buttons
        self.approve_btn = tk.Button(button_frame, text="Approve", command=lambda: self.handle_appointment("In Progress"))
        self.approve_btn.pack(side="left", padx=5)

        self.reject_btn = tk.Button(button_frame, text="Reject", command=lambda: self.handle_appointment("Rejected"))
        self.reject_btn.pack(side="left", padx=5)

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_appointment_select)

    def on_appointment_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            self.approve_btn.config(state="disabled")
            self.reject_btn.config(state="disabled")
            return

        item = self.tree.item(selected_item[0])
        appointment_data = item['values']
        
        if not appointment_data:
            return

        status = appointment_data[4]  # Status is the 5th column

        if status == 'Pending':
            self.approve_btn.config(state="normal")
            self.reject_btn.config(state="normal")
        else:
            self.approve_btn.config(state="disabled")
            self.reject_btn.config(state="disabled")

    def handle_appointment(self, status):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        appointment_data = item['values']
        appointment_id = appointment_data[5]  # AppointmentID is the 6th column

        if Appointment.update_appointment_status(appointment_id, status):
            tk.messagebox.showinfo("Success", f"Appointment {status} successfully!")
            # Refresh the appointments list
            appointments = Appointment.get_mechanic_appointments(self.mechid)
            for item in self.tree.get_children():
                self.tree.delete(item)
            for appointment in appointments:
                self.tree.insert("", "end", values=appointment)
        else:
            tk.messagebox.showerror("Error", "Failed to update appointment status.")