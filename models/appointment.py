from database.config import get_db_connection
from mysql.connector import Error
from datetime import datetime

class Appointment:
    def __init__(self, appointmentid=None, userid=None, mechid=None, appointmentdate=None, 
                 appointmenttime=None, status=None, typeofvehicle=None):
        self.appointmentid = appointmentid
        self.userid = userid
        self.mechid = mechid
        self.appointmentdate = appointmentdate
        self.appointmenttime = appointmenttime
        self.status = status
        self.typeofvehicle = typeofvehicle

    @staticmethod
    def check_mechanic_availability(mechid, date_str, time_str):
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            # Convert date and time to proper format
            date_obj = datetime.strptime(date_str, '%m/%d/%y')
            formatted_date = date_obj.strftime('%Y-%m-%d')
            time_obj = datetime.strptime(time_str, '%I:%M %p')
            formatted_time = time_obj.strftime('%H:%M:00')

            # Check for existing appointments that are either Pending or In Progress
            cursor.execute("""
                SELECT COUNT(*) FROM Appointments 
                WHERE mechid = %s 
                AND appointmentdate = %s 
                AND appointmenttime = %s 
                AND status IN ('Pending', 'In Progress')
            """, (mechid, formatted_date, formatted_time))
            
            count = cursor.fetchone()[0]
            return count == 0  # Returns True if the slot is available
            
        except Error as e:
            print(f"Error checking mechanic availability: {e}")
            return False
        finally:
            cursor.close()
            db_connection.close()

    @staticmethod
    def create_appointment(userid, mechid, date_str, time_str, vehicle_type):
        # First check availability
        if not Appointment.check_mechanic_availability(mechid, date_str, time_str):
            return False, "This time slot is already booked or the mechanic is busy"

        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            # Convert date from MM/DD/YY to YYYY-MM-DD
            date_obj = datetime.strptime(date_str, '%m/%d/%y')
            formatted_date = date_obj.strftime('%Y-%m-%d')

            # Convert time from 12-hour to 24-hour format
            time_obj = datetime.strptime(time_str, '%I:%M %p')
            formatted_time = time_obj.strftime('%H:%M:00')

            cursor.execute("""
                INSERT INTO Appointments 
                (userid, mechid, appointmentdate, appointmenttime, status, typeofvehicle) 
                VALUES (%s, %s, %s, %s, 'Pending', %s)
                """, (userid, mechid, formatted_date, formatted_time, vehicle_type))
            
            db_connection.commit()
            return True, "Appointment booked successfully"
        except Error as e:
            print(f"Error creating appointment: {e}")
            return False, f"Error creating appointment: {str(e)}"
        finally:
            cursor.close()
            db_connection.close()

    @staticmethod
    def get_user_appointments(userid):
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            cursor.execute("""
                SELECT DISTINCT M.business_name, A.appointmentdate, A.typeofvehicle, 
                       A.appointmenttime, A.status
                FROM Appointments A
                JOIN Mechanics M ON A.mechid = M.mechid
                WHERE A.userid = %s
                ORDER BY A.appointmentdate, A.appointmenttime
                """, (userid,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Error getting user appointments: {e}")
            return []
        finally:
            db_connection.close()

    @staticmethod
    def get_mechanic_appointments(userid):
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            cursor.execute("""
                SELECT DISTINCT A.appointmenttime, U.firstname, A.typeofvehicle, 
                       A.appointmentdate, A.status, A.appointmentid
                FROM Appointments A
                JOIN User U ON A.userid = U.userid
                JOIN Mechanics M ON A.mechid = M.mechid
                WHERE M.userid = %s
                ORDER BY A.appointmentdate, A.appointmenttime
                """, (userid,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Error getting mechanic appointments: {e}")
            return []
        finally:
            db_connection.close()

    @staticmethod
    def update_appointment_status(appointmentid, status):
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            cursor.execute("""
                UPDATE Appointments 
                SET status = %s 
                WHERE appointmentid = %s
                """, (status, appointmentid))
            db_connection.commit()
            return True
        except Error as e:
            print(f"Error updating appointment status: {e}")
            return False
        finally:
            cursor.close()
            db_connection.close()

    @staticmethod
    def get_booked_slots(date, mechid):
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            cursor.execute("""
                SELECT appointmenttime 
                FROM Appointments 
                WHERE appointmentdate = %s 
                AND mechid = %s 
                AND status IN ('Pending', 'In Progress')
                """, (date, mechid))
            results = cursor.fetchall()
            cursor.close()
            return [row[0] for row in results]
        except Error as e:
            print(f"Error getting booked slots: {e}")
            return []
        finally:
            db_connection.close()