import streamlit as st
import sqlite3
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText

# Initialize FastAPI app (for future API use)
app = FastAPI()

# Database Setup (SQLite for simplicity)
conn = sqlite3.connect("investor_db.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS investors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    phone TEXT,
                    company TEXT,
                    aum TEXT,
                    sector TEXT
                )''')
conn.commit()

# User Authentication (Basic Example)
users = {"admin": "password123"}  # Replace with a secure authentication method

# Pydantic Model for Email Requests
class EmailRequest(BaseModel):
    subject: str
    body: str
    recipient: str

@app.post("/send_email")
def send_email(request: EmailRequest):
    try:
        msg = MIMEText(request.body)
        msg["Subject"] = request.subject
        msg["From"] = "your-email@example.com"
        msg["To"] = request.recipient

        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login("your-email@example.com", "your-password")
            server.sendmail("your-email@example.com", request.recipient, msg.as_string())
        
        return {"message": "Email sent successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Streamlit Frontend
st.title("Investor Database & Outreach Platform")

# Login Form
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    if users.get(username) == password:
        st.session_state["authenticated"] = True
        st.success("Logged in successfully!")
    else:
        st.error("Invalid credentials")

# If authenticated, show investor search & email functionality
if "authenticated" in st.session_state:
    st.subheader("Search Investors")
    search_query = st.text_input("Search by Name, Company, or Sector")
    if st.button("Search"):
        df = pd.read_sql_query(f"SELECT * FROM investors WHERE first_name LIKE '%{search_query}%' OR company LIKE '%{search_query}%'", conn)
        st.dataframe(df)
    
    st.subheader("Send Bulk Emails")
    recipient = st.text_input("Recipient Email")
    subject = st.text_input("Email Subject")
    body = st.text_area("Email Body")
    if st.button("Send Email"):
        response = send_email(EmailRequest(subject=subject, body=body, recipient=recipient))
        st.success(response["message"])
