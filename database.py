import sqlite3

def connect_db():
    return sqlite3.connect("investors.db", check_same_thread=False)

def search_investors(query):
    conn = connect_db()
    cursor = conn.cursor()

    query = f"%{query}%"
    
    cursor.execute("""
        SELECT DISTINCT first_name, last_name, full_name, job_title, company, location, company_domain, linkedin_profile 
        FROM investors 
        WHERE first_name LIKE ? 
        OR last_name LIKE ? 
        OR full_name LIKE ? 
        OR company LIKE ?
    """, (query, query, query, query))

    results = cursor.fetchall()
    conn.close()
    
    return results
