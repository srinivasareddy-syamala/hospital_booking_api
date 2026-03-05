from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import os

app = FastAPI()

# MySQL connection using Railway variables
db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT"))
)

cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    appointment_date DATE,
    appointment_time TIME
)
""")

db.commit()

# Data model
class Appointment(BaseModel):
    name: str
    phone: str
    date: str
    time: str

# Test route
@app.get("/")
def home():
    return {"message": "Hospital Appointment API Running"}

# Book appointment
@app.post("/book_appointment")
def book_appointment(a: Appointment):

    query = """
    INSERT INTO appointments (name, phone, appointment_date, appointment_time)
    VALUES (%s,%s,%s,%s)
    """

    values = (a.name, a.phone, a.date, a.time)

    cursor.execute(query, values)
    db.commit()

    return {"status": "Appointment Booked Successfully"}
