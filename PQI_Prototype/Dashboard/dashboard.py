import streamlit as st
import pandas as pd
import sqlite3

st.title("AI Talent Mapping Dashboard")

# Connect to database
conn = sqlite3.connect("../database.db")
df = pd.read_sql_query("SELECT * FROM submissions", conn)
conn.close()

st.write("### All Submissions")
st.dataframe(df)
