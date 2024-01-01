import streamlit as st

import streamlit as st
import pandas as pd
from pdfminer.high_level import extract_text

import sqlite3

import re
def fetch_data():
    connection = sqlite3.connect("recruitment_management_system.db")  # Replace with your database file name
    query = "SELECT * FROM candidates"  # Replace with your table name
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

# Function to display data table with filtering
def display_table(data):
    # Use st.dataframe to display a Pandas DataFrame
    st.dataframe(data)
def intro():
    st.write("# Welcome to RMS!")
    st.sidebar.success("Select a demo above.")

    st.markdown("""
     # This is test """)

def cinput():

    st.title(":blue[Recruit Management System]")
    # Create a title for the web application
    st.markdown("""
            This is input page """)
    # Create a form to upload a resume
    st.subheader("Upload a Resume")
    uploaded_file = st.file_uploader("Upload your resume here", type="pdf")

    # Parse the uploaded resume using pdfminer
    if uploaded_file is not None:
        text = extract_text(uploaded_file)

        # Parse the extracted text to identify personal information
        name = re.findall(r"^[A-Za-z]*(?: [A-Za-z]+)*", text)
        email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        phone_number = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
        skills = re.findall(r"(?<!\w)([A-Za-z]+)(?!\w)", text)
        education = re.findall(r"([A-Za-z]+) ([A-Za-z]+) ([A-Za-z]+) ([A-Za-z]+)", text)
        experience = re.findall(r"(?<!\w)([A-Za-z]+)(?!\w)", text)

        # Create a dictionary to store the extracted information
        resume_data = {
            "name": name[0],
            "email": email[0],
            "phone_number": phone_number[0],
            "skills": skills,
            "education": education,
            "experience": experience
        }

        # Create a form to add a candidate to the database
        st.subheader("Add a Candidate")
        candidate_name = st.text_input("Enter the candidate's name", key="candidate_name1",
                                       value=resume_data.get("name", "").title())
        candidate_email = st.text_input("Enter the candidate's email", value=resume_data.get("email", ""))
        candidate_phone_number = st.text_input("Enter the candidate's phone number",
                                               value=resume_data.get("phone_number", ""))
        candidate_skills = st.text_input("Enter the candidate's skills", value=resume_data.get("skills", ""))
        candidate_education = st.text_input("Enter the candidate's education", value=resume_data.get("education", ""))
        candidate_experience = st.text_input("Enter the candidate's experience",
                                             value=resume_data.get("experiance", ""))

    # Create a button to add the candidate to the database
    if st.button("Add Candidate"):
        # Create a database connection
        connection = sqlite3.connect("recruitment_management_system.db")
        cursor = connection.cursor()

        # Insert the candidate's information into the database
        cursor.execute(
            "INSERT INTO candidates (name, email, phone_number, skills, education, experience) VALUES (?, ?, ?, ?, ?, ?)",
            (candidate_name, candidate_email, candidate_phone_number, candidate_skills, candidate_education,
             candidate_experience))

        # Commit the changes to the database
        connection.commit()

        # Close the database connection
        connection.close()

        # Display a message to the user
        st.success("Candidate added to the database")




def cupdate():
    st.write("# Recruit Management System")
    st.markdown("""
        This is Update page """)
    # Connect to SQLite database
    conn = sqlite3.connect('recruitment_management_system.db')

    # Read SQL query into a DataFrame
    df = pd.read_sql_query("SELECT * FROM candidates", conn)

    # Show dataframe in streamlit
    edited_df = st.data_editor(df)

    # If dataframe is edited, update the SQLite database
    if not edited_df.equals(df):
        edited_df.to_sql('candidates', conn, if_exists='replace', index=False)

def creports():

    st.title(":blue[Recruit Management System]")
    st.markdown("""
        Report page """)
    connection = sqlite3.connect("recruitment_management_system.db")  # Replace with your database file name
    query = "SELECT * FROM candidates"  # Replace with your table name
    data = pd.read_sql_query(query, connection)
    connection.close()
    # connection = sqlite3.connect("recruitment_management_system.db")
    # cursor = connection.cursor()

    # data = fetch_data()

    # Display data table
    display_table(data)

# st.set_page_config(
#     page_title="Ex-stream-ly Cool App",
#     page_icon="🧊",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items={
#         'Get Help': 'https://www.extremelycoolapp.com/help',
#         'Report a bug': "https://www.extremelycoolapp.com/bug",
#         'About': "# This is a header. This is an *extremely* cool app!"
#     }
# )
#
# page_names_to_funcs = {
#     "—": intro,
#     "Add Candidate": cinput,
#     "Update": cupdate,
#     "Report": creports
# }

#demo_name = st.sidebar("Choose a demo", page_names_to_funcs.keys())
#page_names_to_funcs[demo_name]()
pages = {
    "Home": intro,
    "Add Candidate": cinput,
     "Update": cupdate,
     "Report": creports
}

# Create a sidebar with navigation links
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page
pages[selection]()
