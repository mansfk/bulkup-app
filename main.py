
import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from supabase import create_client, Client

# Supabase setup
url = "https://jydhavzqnssytylwhijc.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp5ZGhhdnpxbnNzeXR5bHdoaWpjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYxMjA3NDQsImV4cCI6MjA2MTY5Njc0NH0.GbrMVfaBk8yX-eViaxc9Fiur03fR7kNYXNjTdd6vE9g"
supabase: Client = create_client(url, key)

st.set_page_config(page_title="BulkUp", layout="centered")
st.title("💪 BulkUp: Persistent Weight Tracker")

# Input form
st.subheader("Log Your Weight")
weight = st.number_input("Today's Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
if st.button("Submit"):
    today = datetime.date.today().isoformat()
    data = {
        "date": today,
        "weight": weight
    }
    response = supabase.table("weight_logs").insert(data).execute()

    if isinstance(response.data, list) or response.data is not None:
        st.success("✅ Weight logged successfully.")
else:
    st.error("❌ Failed to log weight.")

# Fetch and display historical weights
st.subheader("📈 Weight History")
res = supabase.table("weight_logs").select("*").order("date", desc=False).execute()
rows = res.data

if rows:
    df = pd.DataFrame(rows)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values("date")
    st.line_chart(df.set_index("date")["weight"])
    st.dataframe(df[['date', 'weight']].rename(columns={'date': 'Date', 'weight': 'Weight (kg)'}))
else:
    st.info("No weight logs yet.")
