import pandas as pd
import sqlite3

# Load the CSV file
file_path = "investors.csv"  # Make sure this matches the actual file name
df = pd.read_csv(file_path)

# Select relevant columns
df = df[["First Name", "Last Name", "Full Name", "Job Title", "Company Name", "Location", "Company Domain", "LinkedIn Profile"]]

# Rename columns to match the database schema
df.columns = ["first_name", "last_name", "full_name", "job_title", "company", "location", "company_domain", "linkedin_profile"]

# Connect to SQLite database
conn = sqlite3.connect("investors.db")
cursor = conn.cursor()

# Insert data into the database
investors = df.values.tolist()
cursor.executemany('''
    INSERT INTO investors (first_name, last_name, full_name, job_title, company, location, company_domain, linkedin_profile)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', investors)

conn.commit()
conn.close()

print(f"✅ Successfully inserted {len(investors)} investors into the database!")
