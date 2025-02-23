import streamlit as st
import sqlite3

# Apply Custom Streamlit Theme
st.set_page_config(
    page_title="Investor Database & Outreach Platform",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7f9;
    }
    .stButton>button {
        background-color: #2c7c4f !important;
        color: white !important;
        font-size: 16px;
        border-radius: 5px;
        padding: 10px 24px;
    }
    .stTextInput>div>div>input {
        border: 2px solid #2c7c4f;
        border-radius: 5px;
    }
    .stMarkdown {
        font-size: 18px;
    }
    .search-results {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Database connection
conn = sqlite3.connect("investors.db")
cursor = conn.cursor()

# Page Title
st.markdown("<h1 style='color: #2c7c4f;'>Investor Database & Outreach Platform</h1>", unsafe_allow_html=True)

# Login Section
st.subheader("Login")
username = st.text_input("Username", value="", key="username")
password = st.text_input("Password", value="", type="password", key="password")

if st.button("Login"):
    if username == "admin" and password == "password":
        st.success("Logged in successfully!")
        st.session_state["logged_in"] = True
    else:
        st.error("Invalid credentials!")

# Only show the search section if logged in
if st.session_state.get("logged_in"):
    st.markdown("---")
    st.subheader("Search Investors")

    query = st.text_input("Search by Name, Company, or Sector", key="search_query")

    if st.button("Search", key="search_btn"):
        cursor.execute("""
            SELECT DISTINCT full_name, job_title, company, location, linkedin_profile 
            FROM investors 
            WHERE full_name LIKE ? OR company LIKE ? OR job_title LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))

        results = cursor.fetchall()

        # If duplicates still exist, remove them in Python
        unique_results = list(set(results))

        if unique_results:
            for investor in unique_results:
                st.markdown(
                    f"""
                    <div class="search-results">
                        <strong>{investor[0]}</strong> - {investor[1]} at {investor[2]}<br>
                        <em>Location:</em> {investor[3]} | <a href="{investor[4]}" target="_blank">LinkedIn</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("No investors found.")

# Close database connection
conn.close()
