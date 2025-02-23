import streamlit as st
import database  # Import database functions
import pandas as pd

st.title("Investor Database & Outreach Platform")

# Login Section
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    if username == "admin" and password == "password123":
        st.session_state["authenticated"] = True
        st.success("Logged in successfully!")
    else:
        st.error("Invalid credentials")

# If authenticated, show investor management functionalities
if "authenticated" in st.session_state:

    # Search Investors
    st.subheader("Search Investors")
    search_query = st.text_input("Search by Name, Company, or Sector")
    if st.button("Search"):
        results = database.search_investors(search_query)
        if results:
            df = pd.DataFrame(results, columns=["ID", "First Name", "Last Name", "Email", "Phone", "Company", "AUM", "Sector"])
            st.dataframe(df)
        else:
            st.warning("No investors found.")

    # Upload CSV File
    st.subheader("Upload Investor Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded Data:")
        st.dataframe(df)

        # Check if required columns exist
        required_columns = ["First Name", "Last Name", "Email", "Phone", "Company", "AUM", "Sector"]
        if all(col in df.columns for col in required_columns):
            investors = df[required_columns].values.tolist()
            database.add_multiple_investors(investors)
            st.success(f"Successfully added {len(investors)} investors to the database!")
        else:
            st.error("CSV file must contain columns: First Name, Last Name, Email, Phone, Company, AUM, Sector")

    # Display All Investors
    st.subheader("All Investors")
    all_investors = database.get_all_investors()
    if all_investors:
        df_all = pd.DataFrame(all_investors, columns=["ID", "First Name", "Last Name", "Email", "Phone", "Company", "AUM", "Sector"])
        st.dataframe(df_all)
    else:
        st.warning("No investors in the database.")
