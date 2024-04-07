import mysql.connector

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost", 
            user="root",
            password="Y@shasvi320",
            database="hotel_mgmt",
            port=3306  
        )

        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection

    except mysql.connector.Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

create_connection()
