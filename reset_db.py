import mysql.connector
from mysql.connector import Error

def reset_database():
    try:
        # Connect to MySQL Server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin"
        )
        cursor = connection.cursor()

        # Drop the database if it exists
        cursor.execute("DROP DATABASE IF EXISTS Vehicle_Service_DB")
        print("Database dropped successfully.")

        # Create the database
        cursor.execute("CREATE DATABASE Vehicle_Service_DB")
        print("Database created successfully.")

        # Use the database
        cursor.execute("USE Vehicle_Service_DB")

        # Create Roles table
        cursor.execute("""
        CREATE TABLE Roles (
            roleid INT PRIMARY KEY AUTO_INCREMENT,
            rolename ENUM('user', 'mechanic', 'admin') NOT NULL UNIQUE
        )""")
        print("Roles table created successfully.")

        # Insert predefined roles
        cursor.execute("INSERT INTO Roles (roleid, rolename) VALUES (1, 'user'), (2, 'mechanic'), (3, 'admin')")
        print("Predefined roles inserted successfully.")

        # Commit the changes
        connection.commit()
        print("Database reset completed successfully!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    reset_database() 