from taipy import Gui
from datetime import date
import pandas as pd
import sqlite3

con = sqlite3.connect("backup.db")
Name=""
Designation=""
Location=""
DOJ=""
name =""
designation=""
location=""
doj=""
def connect_database():
    global mycursor, con
    con = sqlite3.connect("backup.db")
    mycursor = con.cursor()
    query = """CREATE TABLE IF NOT EXISTS 
        employee(id INTEGER PRIMARY KEY, 
        Name TEXT,
        Designation TEXT,
        Location TEXT,
        DOJ TEXT
         )"""
    mycursor.execute(query)
    con.commit()


page = """
### CRUD Test Project


<|{name}|input|label=Name|>
<|{designation}|input|label=Designation|>
<|{location}|input|label=Location|>
<|{doj}|input|label=Date of Joining|>

<|Submit|button|on_action=add_data|>



"""
def add_data(state):
    connect_database()
    Name.state = name.state.get()
    Designation = designation.state
    Location = location.state
    DOJ = doj.state

    mycursor.execute("INSERT INTO employee(Name, Designation, Location, DOJ) VALUES(?,?,?,?)", (name.state.get(),designation.state, location.state,doj.state));
    # commit changes to the database
    con.commit()

gui = Gui(page)
#partial = gui.add_partial(partial_md)
gui.run(dark_mode=False, title="RMS",use_reloader=True)