import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


data = pd.read_csv("./glucose_data.csv", usecols=["Time (UTC)", "Glucose Reading (mg/dL)"])

# Convert columns to correct data type
data["Time (UTC)"] = pd.to_datetime(data["Time (UTC)"])
data["Glucose Reading (mg/dL)"] = pd.to_numeric(data["Glucose Reading (mg/dL)"], errors='coerce')
data.dropna(inplace=True)  # This will drop rows with NaN values

# Filter out rows older than the given date
cutoff_date = "2023-08-22 7am"
data = data[data["Time (UTC)"] >= cutoff_date]

# Convert to Pacific Time
data["Time (Pacific)"] = data["Time (UTC)"].dt.tz_convert('US/Pacific')

# Full timerange in one chart
st.line_chart(data[["Time (Pacific)", "Glucose Reading (mg/dL)"]].set_index("Time (Pacific)"))

# One line per day, to compare easily
data["Day"] = data["Time (UTC)"].dt.tz_convert('US/Pacific').dt.date
data = data.reset_index().rename(columns={"index": "Row Number"})
chart = alt.Chart(data).mark_line().encode(
    x=alt.X('hoursminutes(Time (Pacific)):T', title='Time of Day'),
    y='Glucose Reading (mg/dL):Q',
    color=alt.Color('Day:N', timeUnit='yearmonthdate', title='Date', legend=alt.Legend(format='%a %b %d')),
    tooltip=['Row Number:O', 'Day:N', 'Glucose Reading (mg/dL):Q', 'hoursminutes(Time (Pacific)):T']
).interactive()

st.altair_chart(chart, use_container_width=True)

# Print full data table
st.write("Data:")
st.dataframe(data)
