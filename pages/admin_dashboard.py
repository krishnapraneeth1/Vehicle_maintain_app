import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from models.mechanic import Mechanic

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=("#ffffff", "#2b2b2b"))  # Set frame background color
        self.setup_ui()

    def setup_ui(self):
        # Configure the main frame to fill the window
        self.pack(fill="both", expand=True)

        # Title Label with background
        title_frame = ctk.CTkFrame(self, fg_color=("#2980b9", "#2475a8"))
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="Admin Dashboard", 
            font=("Arial", 28, "bold"),
            text_color=("white", "white")
        )
        title_label.pack(pady=15)

        # Create left sidebar for buttons
        sidebar = ctk.CTkFrame(self, fg_color="transparent")
        sidebar.pack(side="left", fill="y", padx=20)
        
        # Add some space at the top of the sidebar
        spacing_frame = ctk.CTkFrame(sidebar, height=60, fg_color="transparent")
        spacing_frame.pack(pady=(40, 20))
        
        # Add Approve and Reject buttons to the sidebar - with colored borders
        self.approve_btn = ctk.CTkButton(
            sidebar,
            text="Approve",
            width=200,
            height=40,
            font=("Poppins", 12, "bold"),
            fg_color="#FFFFFF",  # White background
            text_color="#27ae60",  # Green text
            border_color="#27ae60",  # Green border
            border_width=1,
            hover_color="#E8EAF6",
            command=lambda: self.handle_request("Approved"),
            state="disabled"  # Initially disabled
        )
        self.approve_btn.pack(pady=10)

        self.reject_btn = ctk.CTkButton(
            sidebar,
            text="Reject",
            width=200,
            height=40,
            font=("Poppins", 12, "bold"),
            fg_color="#FFFFFF",  # White background
            text_color="#e74c3c",  # Red text
            border_color="#e74c3c",  # Red border
            border_width=1,
            hover_color="#E8EAF6",
            command=lambda: self.handle_request("Rejected"),
            state="disabled"  # Initially disabled
        )
        self.reject_btn.pack(pady=10)
        
        # View Requests Button - with blue border to match logout style
        self.refresh_button = ctk.CTkButton(
            sidebar, 
            text="Refresh Requests", 
            width=200,
            height=40,
            font=("Poppins", 12, "bold"),
            fg_color="#FFFFFF",  # White background
            text_color="#1A237E",  # Blue text
            border_color="#1A237E",  # Blue border
            border_width=1,
            hover_color="#E8EAF6",
            command=self.load_requests  # Changed from toggle_requests_view to load_requests
        )
        self.refresh_button.pack(pady=10)

        # Generate Report Button - same blue border style
        self.report_button = ctk.CTkButton(
            sidebar, 
            text="Generate Report", 
            width=200,
            height=40,
            font=("Poppins", 12, "bold"),
            fg_color="#FFFFFF",  # White background
            text_color="#1A237E",  # Blue text
            border_color="#1A237E",  # Blue border
            border_width=1,
            hover_color="#E8EAF6",
            command=self.generate_admin_report
        )
        self.report_button.pack(pady=10)

        # Logout Button - same style
        self.logout_button = ctk.CTkButton(
            sidebar, 
            text="Logout",
            width=200,
            height=40,
            font=("Poppins", 12, "bold"),
            fg_color="#FFFFFF",  # White background
            text_color="#1A237E",  # Blue text
            border_color="#1A237E",  # Blue border
            border_width=1,
            hover_color="#E8EAF6",
            command=self.controller.show_login
        )
        self.logout_button.pack(side="bottom", pady=20)

        # Create main content area for requests view
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Initialize requests view
        self.setup_requests_view()

    def setup_requests_view(self):
        # Create and configure the Treeview with a modern style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", rowheight=22)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#393e46", foreground="white")
        style.map('Treeview', background=[('selected', '#2c3e50')])

        # Create Treeview with height parameter to control its size
        columns = ["Business ID", "Business Name", "Service ID", "Zip Code", "Service Type", "Vehicle Type", "Status"]
        self.tree = ttk.Treeview(
            self.content_frame,
            columns=columns,
            show="headings",
            style="Treeview",
            height=12
        )

        # Configure columns with smaller width
        column_widths = {
            "Business ID": 80,
            "Business Name": 150,
            "Service ID": 80,
            "Zip Code": 80,
            "Service Type": 150,
            "Vehicle Type": 100,
            "Status": 120
        }

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 110), anchor="center")

        # Create scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Pack widgets with adjusted padding
        self.tree.pack(side="top", fill="both", expand=True, pady=(0, 15))
        scrollbar.pack(side="right", fill="y")

        # Configure tag for already registered services
        self.tree.tag_configure("registered", foreground="#888888")

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_request_select)

    def toggle_requests_view(self):
        if not hasattr(self, '_requests_visible'):
            self._requests_visible = False
        
        self._requests_visible = not self._requests_visible
        
        if self._requests_visible:
            self.load_requests()
            self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
            # Updated active state styling
            self.view_requests_button.configure(
                fg_color="#1A237E", 
                text_color="#FFFFFF",
                hover_color="#303F9F"
            )
        else:
            self.content_frame.pack_forget()
            # Reset to default styling
            self.view_requests_button.configure(
                fg_color="#FFFFFF",
                text_color="#1A237E",
                hover_color="#E8EAF6"
            )

    def load_requests(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get pending requests
        requests = Mechanic.get_pending_requests()
        for request in requests:
            # Check if service is already registered
            business_id, business_name, service_id, zip_code, service_type, vehicle_type = request
            is_registered = Mechanic.check_service_exists(business_id, service_type)
            
            # Add status to the request data
            values = list(request) + ["Already Registered" if is_registered else "Pending"]
            
            # Insert with appropriate tag if registered
            item_id = self.tree.insert("", "end", values=values)
            if is_registered:
                self.tree.item(item_id, tags=("registered",))

    def on_request_select(self, event):
        # Get selected item
        selected_items = self.tree.selection()
        
        if selected_items:
            # Get item data
            item = self.tree.item(selected_items[0])
            self.selected_item = item["values"]
            
            # Check if the request is pending
            if self.selected_item and self.selected_item[-1] == "Pending":
                # Enable buttons
                self.approve_btn.configure(
                    state="normal",
                    fg_color="#FFFFFF",
                    text_color="#27ae60",
                    border_color="#27ae60"
                )
                self.reject_btn.configure(
                    state="normal",
                    fg_color="#FFFFFF",
                    text_color="#e74c3c",
                    border_color="#e74c3c"
                )
            else:
                # Disable buttons
                self.approve_btn.configure(
                    state="disabled",
                    fg_color="#F0F0F0",  # Lighter color for disabled state
                    text_color="#A0A0A0",  # Grayed out text
                    border_color="#C0C0C0"  # Grayed out border
                )
                self.reject_btn.configure(
                    state="disabled",
                    fg_color="#F0F0F0",  # Lighter color for disabled state
                    text_color="#A0A0A0",  # Grayed out text
                    border_color="#C0C0C0"  # Grayed out border
                )
        else:
            # Disable buttons if nothing is selected
            self.approve_btn.configure(
                state="disabled",
                fg_color="#F0F0F0",  # Lighter color for disabled state
                text_color="#A0A0A0",  # Grayed out text
                border_color="#C0C0C0"  # Grayed out border
            )
            self.reject_btn.configure(
                state="disabled",
                fg_color="#F0F0F0",  # Lighter color for disabled state
                text_color="#A0A0A0",  # Grayed out text
                border_color="#C0C0C0"  # Grayed out border
            )

    def handle_request(self, status):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        request_data = item['values']
        
        # Check if service is already registered
        if request_data[6] == "Already Registered":
            messagebox.showinfo("Info", f"Service '{request_data[4]}' is already registered for this mechanic.")
            return

        business_id = request_data[0]
        if Mechanic.update_approval_status(business_id, status):
            messagebox.showinfo("Success", f"Request {status.lower()} successfully!")
            self.load_requests()
        else:
            messagebox.showerror("Error", "Failed to update request status.")

    def generate_admin_report(self):
        import csv
        from datetime import datetime
        from tkinter import messagebox
        
        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create filename with timestamp
        filename = f"admin_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            # Open the file once and keep it open for all operations
            with open(filename, "w", newline='') as csvfile:
                # Create CSV writer
                csv_writer = csv.writer(csvfile)
                
                # Write header row and metadata
                csv_writer.writerow(["Report Type", "Generated On", "Generated By"])
                csv_writer.writerow(["Admin Business Report", current_datetime, "Admin"])
                
                # Add blank row for separation
                csv_writer.writerow([])
                
                # ALL MECHANICS SECTION - SECTION 1
                csv_writer.writerow(["SECTION 1: ALL MECHANICS AND THEIR STATUS"])
                csv_writer.writerow([])
                
                try:
                    from database.config import get_db_connection
                    connection = get_db_connection()
                    cursor = connection.cursor()
                    
                    # First, let's check the actual structure of the database
                    cursor.execute("SHOW TABLES")
                    tables = [table[0] for table in cursor.fetchall()]
                    print("Available tables:", tables)
                    
                    # MECHANICS SECTION
                    # Let's check a simpler query first to get data flowing
                    simple_query = """
                    SELECT * FROM mechanics LIMIT 5
                    """
                    cursor.execute(simple_query)
                    sample_data = cursor.fetchall()
                    print("Sample mechanics data:", sample_data)
                    
                    if not sample_data:
                        csv_writer.writerow(["No mechanic data found in database"])
                        print("No mechanic data found in database")
                    else:
                        # Extract column names from the first row's metadata
                        column_names = [i[0] for i in cursor.description]
                        print("Mechanics table columns:", column_names)
                        
                        # Find the column that is likely the primary key/business ID
                        id_col = None
                        for possible_id in ['id', 'mechanic_id', 'business_id']:
                            if possible_id in column_names:
                                id_col = possible_id
                                break
                        
                        if not id_col:
                            # If no obvious ID column, use the first column
                            id_col = column_names[0]
                        
                        print(f"Using '{id_col}' as the business ID column")
                        
                        # Simplified query that avoids table alias errors
                        query = f"""
                        SELECT 
                            mechanics.{id_col}, 
                            mechanics.business_name,
                            services.serviceid, 
                            mechanics.zipcode, 
                            services.servicename, 
                            services.typeofvehicle, 
                            CASE 
                                WHEN mechanics.approval_status = 1 THEN 'Approved' 
                                WHEN mechanics.approval_status = 2 THEN 'Rejected'
                                ELSE 'Pending' 
                            END as status
                        FROM mechanics 
                        LEFT JOIN services ON mechanics.serviceid = services.serviceid
                        ORDER BY mechanics.business_name
                        """
                        
                        try:
                            cursor.execute(query)
                            all_businesses = cursor.fetchall()
                            
                            # Get the actual column names from the query results
                            result_columns = [i[0] for i in cursor.description]
                            print("Result columns:", result_columns)
                            
                            # Update column name "typeofvehicle" to "Type of Service"
                            for i, col in enumerate(result_columns):
                                if col.lower() == 'typeofvehicle':
                                    result_columns[i] = 'Type of Service'
                            
                            # Write the ACTUAL column headers from the query results
                            csv_writer.writerow(result_columns)
                            
                            # Write all business data to CSV
                            for business in all_businesses:
                                csv_writer.writerow(business)
                        except Exception as query_error:
                            print(f"Error executing main query: {str(query_error)}")
                            csv_writer.writerow([f"Error retrieving business data: {str(query_error)}"])
                
                    # SECTION 2: BOOKING DETAILS - Check if we can find the table
                    csv_writer.writerow([])
                    csv_writer.writerow([])
                    csv_writer.writerow(["SECTION 2: BOOKING DETAILS BY MECHANIC"])
                    csv_writer.writerow([])

                    # Update in the booking details section for both primary and alternative tables
                    try:
                        # Try to inspect the booking_details table directly
                        cursor.execute("SHOW TABLES LIKE 'booking_details'")
                        if cursor.fetchone():
                            booking_table = 'booking_details'
                            csv_writer.writerow([f"Found booking table: {booking_table}"])
                            
                            # Get the structure
                            cursor.execute(f"DESCRIBE {booking_table}")
                            booking_columns = [column[0] for column in cursor.fetchall()]
                            csv_writer.writerow(["Table structure:"])
                            csv_writer.writerow(booking_columns)
                            
                            # Get a sample of data from the booking_details table
                            cursor.execute(f"SELECT * FROM {booking_table} LIMIT 5")
                            sample = cursor.fetchall()
                            
                            if sample:
                                # Important: Get the actual column names from the result
                                actual_columns = [i[0] for i in cursor.description]
                                
                                # Update column name "typeofvehicle" to "Type of Service" in Section 2
                                for i, col in enumerate(actual_columns):
                                    if (col.lower() == 'typeofvehicle'):
                                        actual_columns[i] = 'Type of Service'
                                    
                                csv_writer.writerow([])
                                csv_writer.writerow(["Booking Details Data"])
                                # Write the updated column names
                                csv_writer.writerow(actual_columns)
                                # Write the data rows
                                for row in sample:
                                    csv_writer.writerow(row)
                            else:
                                csv_writer.writerow(["No booking details found in the table"])
                        else:
                            # If not found, check for alternative tables
                            booking_table = None
                            for table_name in tables:
                                if 'book' in table_name.lower() or 'appointment' in table_name.lower():
                                    booking_table = table_name
                                    break
                            
                            if booking_table:
                                csv_writer.writerow([f"Using alternative booking table: {booking_table}"])
                                
                                # Get sample data
                                cursor.execute(f"SELECT * FROM {booking_table} LIMIT 5")
                                sample = cursor.fetchall()
                                if sample:
                                    # Always use the actual column names from the query result
                                    actual_columns = [i[0] for i in cursor.description]
                                    
                                    # Update column name "typeofvehicle" to "Type of Service" here too
                                    for i, col in enumerate(actual_columns):
                                        if col.lower() == 'typeofvehicle':
                                            actual_columns[i] = 'Type of Service'
                                    
                                    csv_writer.writerow(["Available booking data columns:"])
                                    csv_writer.writerow(actual_columns)
                                    csv_writer.writerow(["Sample booking data:"])
                                    for row in sample:
                                        csv_writer.writerow(row)
                                else:
                                    csv_writer.writerow([f"No data found in {booking_table}"])
                            else:
                                csv_writer.writerow(["No booking-related tables found in the database"])
                    except Exception as booking_error:
                        csv_writer.writerow([f"Error retrieving booking details: {str(booking_error)}"])
                    
                    # Close database connections
                    cursor.close()
                    connection.close()
                        
                except Exception as db_error:
                    # In case of database error, log the error
                    csv_writer.writerow([])
                    csv_writer.writerow(["ERROR FETCHING DATA:", str(db_error)])
                    print(f"Database error: {str(db_error)}")
            
            # Success message after file is properly closed
            messagebox.showinfo("Report Generated", f"Comprehensive report saved as '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            print(f"Report generation error: {str(e)}")
