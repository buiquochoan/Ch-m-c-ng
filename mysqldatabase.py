import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def insert(sql, val):
    mydb = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE')
    )
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()