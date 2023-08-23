import streamlit as st
import pandas as pd
import numpy as np

data = pd.read_csv("./glucose_data.csv", usecols=["Time (UTC)", "Glucose Reading (mg/dL)"])

# Convert columns to correct data type
data["Time (UTC)"] = pd.to_datetime(data["Time (UTC)"])
data["Glucose Reading (mg/dL)"] = pd.to_numeric(data["Glucose Reading (mg/dL)"], errors='coerce')
data.dropna(inplace=True)  # This will drop rows with NaN values

# Filter out rows older than the given date
cutoff_date = "2023-08-22 7am"
data = data[data["Time (UTC)"] >= cutoff_date]

# Convert to Pacific Time
data["Time (UTC)"] = data["Time (UTC)"].dt.tz_convert('US/Pacific').dt.tz_localize(None)
data = data.rename(columns={"Time (UTC)": "Time (Pacific)"})

st.line_chart(data.set_index("Time (Pacific)"))

# Print full data table
#st.write("Data:")
#st.dataframe(data)
