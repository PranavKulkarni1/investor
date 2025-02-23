import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("investors.db", check_same_thread=False)
cursor = conn.cursor()

# Create investors table (if it doesn't exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS investors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        company TEXT,
        aum TEXT,
        sector TEXT
    )
''')
conn.commit()

def add_investor(first_name, last_name, email, phone, company, aum, sector):
    """Function to add an investor to the database"""
    cursor.execute('''
        INSERT INTO investors (first_name, last_name, email, phone, company, aum, sector)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, email, phone, company, aum, sector))
    conn.commit()

def search_investors(query):
    """Function to search for investors based on name, company, or sector"""
    cursor.execute('''
        SELECT * FROM investors 
        WHERE first_name LIKE ? OR last_name LIKE ? OR company LIKE ? OR sector LIKE ?
    ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
    return cursor.fetchall()

def get_all_investors():
    """Function to get all investors"""
    cursor.execute('SELECT * FROM investors')
    return cursor.fetchall()

def add_multiple_investors(investors):
    """Function to bulk insert investors from a list of tuples"""
    cursor.executemany('''
        INSERT INTO investors (first_name, last_name, email, phone, company, aum, sector)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', investors)
    conn.commit()
