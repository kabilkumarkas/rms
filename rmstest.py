import streamlit as st
import pandas as pd
import pdfminer
from pdfminer.high_level import extract_text

import sqlite3
import io
import re
import string
import os
import numpy as np
import datetime
import uuid
def fetch_data():
    connection = sqlite3.connect("recruitment_management_system.db")  # Replace with your database file name
    query = "SELECT * FROM your_table"  # Replace with your table name
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

# Function to display data table with filtering
def display_table(data):
    # Use st.dataframe to display a Pandas DataFrame
    st.dataframe(data)
# Define the main function
def main():
    # Create a title for the web application
    st.title("Recruitment Management System")

    # Create a form to upload a resume
    st.subheader("Upload a Resume")
    uploaded_file = st.file_uploader("Upload your resume here", type="pdf")

    # Parse the uploaded resume using pdfminer
    if uploaded_file is not None:
        text = extract_text(uploaded_file)

        # Parse the extracted text to identify personal information
        name = re.findall(r"^[A-Za-z]*(?: [A-Za-z]+)*", text)
        email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        phone_number = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',text)
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

        # Display the extracted information on the web application
        #st.subheader("Extracted Resume Information")
        #st.write(resume_data)
        #resume_data = pd.DataFrame(resume_data)

        # Save the extracted information to a CSV file
        #with open("resume_data.csv", "w") as f:
           # f.write(resume_data.to_csv())

        # Create a form to add a candidate to the database
        st.subheader("Add a Candidate")
        candidate_name = st.text_input("Enter the candidate's name", key="candidate_name1", value=resume_data.get("name", ""))
        candidate_email = st.text_input("Enter the candidate's email", value=resume_data.get("email", ""))
        candidate_phone_number = st.text_input("Enter the candidate's phone number",value=resume_data.get("phone_number", ""))
        candidate_skills = st.text_input("Enter the candidate's skills",value=resume_data.get("skills", ""))
        candidate_education = st.text_input("Enter the candidate's education", value=resume_data.get("education", ""))
        candidate_experience = st.text_input("Enter the candidate's experience", value=resume_data.get("experiance", ""))

    # Create a button to add the candidate to the database
    if st.button("Add Candidate"):
        # Create a database connection
        connection = sqlite3.connect("recruitment_management_system.db")
        cursor = connection.cursor()

        # Insert the candidate's information into the database
        cursor.execute("INSERT INTO candidates (name, email, phone_number, skills, education, experience) VALUES (?, ?, ?, ?, ?, ?)", (candidate_name, candidate_email, candidate_phone_number, candidate_skills, candidate_education, candidate_experience))

        # Commit the changes to the database
        connection.commit()

        # Close the database connection
        connection.close()

        # Display a message to the user
        st.success("Candidate added to the database")

    # Create a form to search for a candidate
    st.subheader("Search for a Candidate")
    candidate_name = st.text_input("Enter the candidate's name",key="candidate_name2")

    # Create a button to search for the candidate
    if st.button("Search"):
        # Create a database connection
        connection = sqlite3.connect("recruitment_management_system.db")
        cursor = connection.cursor()

        # Select the candidate's information from the database
        cursor.execute("SELECT * FROM candidates WHERE name = ?", (candidate_name,))

        # Fetch the candidate's information from the database
        candidate_data = cursor.fetchone()

        # Close the database connection
        connection.close()

        # Display the candidate's information on the web application
        st.subheader("Candidate Information")
        #st.write(candidate_data)
        st.dataframe(candidate_data)
    # Create a form to generate a report
    st.subheader("Generate a Report")
    report_type = st.selectbox("Select the type of report", ["All Candidates", "Candidates by Skill", "Candidates by Education", "Candidates by Experience"])

    # Create a button to generate the report
    if st.button("Generate Report"):
        # Create a database connection
        connection = sqlite3.connect("recruitment_management_system.db")  # Replace with your database file name
        query = "SELECT * FROM candidates"  # Replace with your table name
        data = pd.read_sql_query(query, connection)
        connection.close()
        #connection = sqlite3.connect("recruitment_management_system.db")
        #cursor = connection.cursor()

        #data = fetch_data()

        # Display data table
        display_table(data)
        # Generate the report based on the selected report type

        #
    if st.button("Filter Report"):
        connection = sqlite3.connect("recruitment_management_system.db")  # Replace with your database file name
        query = "SELECT * FROM candidates"  # Replace with your table name
        data = pd.read_sql_query(query, connection)
        connection.close()
        # Display the report on the web application
        #st.subheader("Report")
        # Add a filter to the data table
        filter_column = st.selectbox("Select a column for filtering", data.columns)
        filter_value = st.text_input(f"Enter {filter_column} value to filter")

        # Apply the filter to the data
        filtered_data = data[data[filter_column] == filter_value]

        # Display the filtered data
        st.subheader("Filtered Data")
        st.dataframe(filtered_data)
        #st.write(report_data)
        #st.dataframe(report_data)
if __name__ == "__main__":
    main()
