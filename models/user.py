from database.config import get_db_connection
from mysql.connector import Error

class User:
    def __init__(self, userid=None, firstname=None, lastname=None, email=None, password=None, 
                 phoneno=None, address1=None, city=None, state=None, zipcode=None, roleid=None):
        self.userid = userid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.phoneno = phoneno
        self.address1 = address1
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.roleid = roleid

    @staticmethod
    def authenticate(email, password):
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            cursor.execute("SELECT userid, roleid FROM User WHERE email = %s AND password = %s", 
                         (email, password))
            result = cursor.fetchone()
            return result if result else None
        except Error as e:
            print(f"Error authenticating user: {e}")
            return None
        finally:
            cursor.close()
            db_connection.close()

    @staticmethod
    def register(firstname, lastname, email, password, phoneno, address1, city, state, zipcode, roleid):
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO User (firstname, lastname, email, password, phoneno, address1, city, state, zipcode, roleid) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (firstname, lastname, email, password, phoneno, address1, city, state, zipcode, roleid))
            
            # Get the last inserted user_id
            cursor.execute("SELECT LAST_INSERT_ID()")
            user_id = cursor.fetchone()[0]
            
            db_connection.commit()
            return user_id
        except Error as e:
            print(f"Error registering user: {e}")
            return None
        finally:
            cursor.close()
            db_connection.close()

    @staticmethod
    def get_user_by_email(email):
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        
        try:
            cursor.execute("SELECT firstname FROM User WHERE email = %s", (email,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            cursor.close()
            db_connection.close() 