# Vehicle Service & Maintenance Management System

A comprehensive system for managing vehicle service and maintenance appointments between users and mechanics.

## Features

- User Registration and Authentication
- Mechanic Business Registration
- Service Booking System
- Appointment Management
- Admin Dashboard for Request Approvals
- Report Generation

## Project Structure

```
.
├── database/
│   └── config.py           # Database configuration and initialization
├── models/
│   ├── user.py            # User model
│   ├── mechanic.py        # Mechanic model
│   └── appointment.py     # Appointment model
├── pages/
│   ├── login_page.py      # Login page
│   ├── registration_page.py # Registration page
│   ├── user_dashboard.py  # User dashboard
│   ├── mechanic_dashboard.py # Mechanic dashboard
│   └── admin_dashboard.py # Admin dashboard
├── UI/                    # UI assets
├── main.py               # Main application file
└── requirements.txt      # Project dependencies
```

## Setup Instructions

1. Install Python 3.8 or higher
2. Install MySQL Server
3. Create a MySQL user with username 'root' and password 'admin'
4. Install required packages:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   python main.py
   ```

## User Types

1. Regular User
   - Can search for mechanics
   - Can book appointments
   - Can view booking history

2. Mechanic
   - Can register their business
   - Can manage appointments
   - Can update appointment status

3. Admin
   - Can approve/reject mechanic registrations
   - Can generate reports
   - Can monitor system activity

## Database Schema

The system uses MySQL with the following main tables:
- User
- Mechanics
- Services
- Appointments
- Mechanic_Businesses
- Roles

## Dependencies

- mysql-connector-python: MySQL database connector
- Pillow: Image processing
- customtkinter: Modern UI widgets
- tkcalendar: Calendar widget
- fpdf: PDF report generation 