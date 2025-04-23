from database.config import get_db_connection
from mysql.connector import Error

class Mechanic:
    @staticmethod
    def register_mechanic(firstname, lastname, email, password, phoneno, address1, city, state, zipcode, business_name, serviceid):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # First register the user with mechanic role (roleid = 2)
            insert_user = """
                INSERT INTO user (firstname, lastname, email, password, phoneno, 
                    address1, city, state, zipcode, roleid) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 2)
            """
            cursor.execute(insert_user, (
                firstname, lastname, email, password, phoneno,
                address1, city, state, zipcode
            ))
            
            # Get the newly created user ID
            user_id = cursor.lastrowid
            
            # Insert into mechanics table, use serviceid from registration
            insert_mechanic = """
                INSERT INTO mechanics (
                    userid, serviceid, firstname, lastname, email, password, 
                    phoneno, address1, city, state, zipcode, business_name, 
                    approval_status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending'
                )
            """
            cursor.execute(insert_mechanic, (
                user_id, serviceid, firstname, lastname, email, password,
                phoneno, address1, city, state, zipcode, business_name
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
            
        except Exception as e:
            print(f"Error registering mechanic: {str(e)}")
            if connection:
                connection.rollback()
            return False

    @staticmethod
    def get_mechanic_by_user_id(user_id):
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT * FROM Mechanics WHERE userid = %s
                """, (user_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error getting mechanic: {e}")
            return None
        finally:
            cursor.close()
            db_connection.close()

    @staticmethod
    def register_business(user_id, business_name, service_id, zip_code, service_type, vehicle_type):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # First get the mechanic ID for the given user ID
            cursor.execute("""
                SELECT mechid FROM mechanics 
                WHERE userid = %s
            """, (user_id,))
            result = cursor.fetchone()
            
            if not result:
                print("No mechanic found for user_id:", user_id)
                return False
                
            mechid = result[0]
            
            # Insert into Mechanic_Businesses table
            insert_business = """
                INSERT INTO Mechanic_Businesses (
                    mechid, business_name, service_id, zip_code,
                    service_type, vehicle_type, approval_status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, 'Pending'
                )
            """
            cursor.execute(insert_business, (
                mechid, business_name, service_id, zip_code,
                service_type, vehicle_type
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
            
        except Exception as e:
            print(f"Error registering business: {str(e)}")
            if 'connection' in locals() and connection:
                connection.rollback()
            return False

    @staticmethod
    def get_pending_requests():
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            cursor.execute("""
                SELECT business_id, business_name, service_id, zip_code, service_type, vehicle_type 
                FROM Mechanic_Businesses
                WHERE approval_status = 'Pending'
            """)
            return cursor.fetchall()
        except Error as e:
            print(f"Error getting pending requests: {e}")
            return []
        finally:
            cursor.close()
            db_connection.close()

    @staticmethod
    def update_approval_status(business_id, status):
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            cursor.execute("""
                UPDATE Mechanic_Businesses 
                SET approval_status = %s 
                WHERE business_id = %s
            """, (status, business_id))
            
            db_connection.commit()
            return True
        except Error as e:
            print(f"Error updating approval status: {e}")
            db_connection.rollback()
            return False
        finally:
            cursor.close()
            db_connection.close()

    @staticmethod
    def search_mechanics(zip_code, service_type):
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            # Join with Services table to get mechanics who offer the selected service
            cursor.execute("""
                SELECT mb.business_name, s.servicename, mb.zip_code, mb.vehicle_type 
                FROM Mechanic_Businesses mb
                JOIN Services s ON mb.service_id = s.serviceid
                WHERE mb.zip_code = %s 
                AND s.servicename = %s
                AND mb.approval_status = 'Approved'
            """, (zip_code, service_type))
            
            return cursor.fetchall()
        except Error as e:
            print(f"Error searching mechanics: {e}")
            return []
        finally:
            cursor.close()
            db_connection.close()

    @staticmethod
    def check_service_exists(business_id, service_type):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Check if the service is already registered and approved
            cursor.execute("""
                SELECT COUNT(*) 
                FROM Mechanic_Businesses 
                WHERE mechid = (SELECT mechid FROM Mechanic_Businesses WHERE business_id = %s)
                AND service_type = %s 
                AND approval_status = 'Approved'
            """, (business_id, service_type))
            
            count = cursor.fetchone()[0]
            return count > 0
            
        except Error as e:
            print(f"Error checking service: {str(e)}")
            return False
        finally:
            if 'connection' in locals():
                connection.close()

    @staticmethod
    def get_registered_services(userid):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Get the mechanic ID first
            cursor.execute("SELECT mechid FROM mechanics WHERE userid = %s", (userid,))
            mechanic = cursor.fetchone()
            
            if not mechanic:
                return []
                
            mechid = mechanic[0]
            
            # Get approved services for this mechanic
            cursor.execute("""
                SELECT service_type 
                FROM Mechanic_Businesses 
                WHERE mechid = %s 
                AND approval_status = 'Approved'
            """, (mechid,))
            
            services = cursor.fetchall()
            return [service[0] for service in services]
            
        except Error as e:
            print(f"Error getting registered services: {str(e)}")
            return []
        finally:
            if 'connection' in locals():
                connection.close()