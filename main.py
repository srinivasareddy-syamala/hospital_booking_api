from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

# Railway automatically provides DATABASE_URL
DATABASE_URL = os.getenv("mysql://root:UwOxBlybefyaXrLAlmudeSVXPqXDlaOM@yamanote.proxy.rlwy.net:25439/railway")

def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


# ===============================
# Create Table (runs automatically)
# ===============================
@app.on_event("startup")
def create_table():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id SERIAL PRIMARY KEY,
        patient_name TEXT,
        doctor_name TEXT,
        appointment_date DATE,
        appointment_time TEXT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


# ===============================
# Check availability
# ===============================
@app.get("/check")
def check_availability(doctor: str, date: str, time: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM appointments
        WHERE doctor_name=%s
        AND appointment_date=%s
        AND appointment_time=%s
        """,
        (doctor, date, time)
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return {"available": False}

    return {"available": True}


# ===============================
# Book appointment
# ===============================
@app.post("/book")
def book_appointment(name: str, doctor: str, date: str, time: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO appointments
        (patient_name, doctor_name, appointment_date, appointment_time)
        VALUES (%s,%s,%s,%s)
        """,
        (name, doctor, date, time)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Appointment booked successfully"}

