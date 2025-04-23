import mysql.connector
from mysql.connector import Error, IntegrityError

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",
            database="Vehicle_Service_DB"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def init_db():
    # First create the database if it doesn't exist
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123"
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS Vehicle_Service_DB")
        connection.close()
        print("Database 'Vehicle_Service_DB' created or already exists.")
    except Error as e:
        print(f"Error creating database: {e}")
        return

    # Now connect to the specific database and create tables
    db_connection = get_db_connection()
    if db_connection is None:
        return

    cursor = db_connection.cursor()

    # Function to check if a table exists
    def table_exists(table_name):
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        return cursor.fetchone() is not None

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
            userid INT NOT NULL,
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
            business_name VARCHAR(255) NOT NULL,
            approval_status ENUM('Pending', 'Approved', 'Rejected') NOT NULL DEFAULT 'Pending'
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
            status ENUM('Pending', 'In Progress', 'Completed', 'Rejected') NOT NULL,
            typeofvehicle VARCHAR(50) NOT NULL,
            FOREIGN KEY (userid) REFERENCES User(userid) ON DELETE CASCADE,
            FOREIGN KEY (mechid) REFERENCES Mechanics(mechid) ON DELETE CASCADE
        )""",
    }

    try:
        # Create tables
        for table_name, create_query in tables.items():
            try:
                cursor.execute(create_query)
                print(f"Table '{table_name}' created successfully.")
            except Error as e:
                print(f"Table '{table_name}' already exists, skipping creation.")
        
        # Insert default roles
        cursor.execute("""
            INSERT IGNORE INTO Roles (roleid, rolename) 
            VALUES 
                (1, 'user'),
                (2, 'mechanic'),
                (3, 'admin')
        """)
        
        # Insert default services
        cursor.execute("""
            INSERT IGNORE INTO Services (servicename, typeofvehicle) 
            VALUES 
                ('Oil Change', 'All'),
                ('Brake Service', 'All'),
                ('Tire Rotation', 'All'),
                ('Engine Tune-up', 'All'),
                ('Transmission Service', 'All'),
                ('Battery Replacement', 'All'),
                ('Air Filter Replacement', 'All'),
                ('Coolant Flush', 'All'),
                ('Wheel Alignment', 'All'),
                ('Suspension Repair', 'All'),
                ('Exhaust System Repair', 'All'),
                ('AC Service', 'All'),
                ('Diagnostic Check', 'All'),
                ('Windshield Wiper Replacement', 'All'),
                ('Headlight/Taillight Repair', 'All')
        """)
        
        # Create default admin user if not exists
        cursor.execute("""
            INSERT IGNORE INTO User (
                firstname, lastname, email, password, 
                phoneno, address1, city, state, zipcode, roleid
            ) VALUES (
                'Admin', 'User', 'admin@vehicle.com', 'Admin@123',
                '1234567890', 'Admin Address', 'Admin City', 'Admin State', '12345', 3
            )
        """)
        
        db_connection.commit()
        print("Database initialized successfully!")
        print("Default admin credentials:")
        print("Email: admin@vehicle.com")
        print("Password: Admin@123")
        
    except Error as e:
        print(f"Error initializing database: {e}")
        db_connection.rollback()
    finally:
        cursor.close()
        db_connection.close()

    print("Database setup completed successfully!")