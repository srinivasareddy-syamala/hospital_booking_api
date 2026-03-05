from fastapi import FastAPI
import pymysql

app = FastAPI()

# MySQL connection
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="hospital_db",
    cursorclass=pymysql.cursors.DictCursor
)

# Home route
@app.get("/")
def home():
    return {"message": "Hospital Appointment API running"}

# Book appointment
@app.post("/book_appointment")
def book_appointment(name: str, phone: str, date: str, time: str):

    cur = conn.cursor()

    # check if slot already booked
    check_query = """
    SELECT * FROM appointments 
    WHERE appointment_date=%s AND appointment_time=%s
    """

    cur.execute(check_query, (date, time))
    existing = cur.fetchone()

    if existing:
        return {"message": "This time slot is already booked"}

    insert_query = """
    INSERT INTO appointments
    (name, phone, appointment_date, appointment_time)
    VALUES (%s,%s,%s,%s)
    """

    cur.execute(insert_query, (name, phone, date, time))
    conn.commit()

    return {"message": "Appointment booked successfully"}

# View all appointments
@app.get("/appointments")
def view_appointments():

    cur = conn.cursor()

    cur.execute("SELECT * FROM appointments")

    data = cur.fetchall()

    return data
