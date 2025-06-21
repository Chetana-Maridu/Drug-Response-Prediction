import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # replace with your MySQL username
        password='######',  # replace #  with your MySQL password
        database='drug_response'
    )
    return connection
