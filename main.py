import datetime
import pytz

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib as mpl


def compute_colors(base_color, n, lighten_factor=0.25):
    colors = [base_color]
    for i in range(1, n):
        base_color = mpl.colors.to_rgb(base_color)
        # Lighten the color
        base_color = [min(1, c + lighten_factor) for c in base_color]
        colors.append(mpl.colors.to_hex(base_color))
    colors = colors[1:] + ["red"]
    return colors


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

pacific = pytz.timezone('US/Pacific')
now = datetime.datetime.now(pacific)
data['DaysAgo'] = (now - data['Time (Pacific)']).dt.days

num_days = data['DaysAgo'].nunique()
colors_range = compute_colors('#000080', num_days)

data = data.reset_index().rename(columns={"index": "Row Number"})
chart = alt.Chart(data).mark_line().encode(
    x=alt.X('hoursminutes(Time (Pacific)):T', title='Time of Day'),
    y='Glucose Reading (mg/dL):Q',
    color=alt.Color(
        'DaysAgo:O',
        scale=alt.Scale(
            domain=list(range(num_days)),
            range=colors_range
        ),
        legend=None),
    tooltip=['Row Number:O', 'Day:N', 'Glucose Reading (mg/dL):Q', 'hoursminutes(Time (Pacific)):T']
).interactive()

st.altair_chart(chart, use_container_width=True)

# Print full data table
st.write("Data:")
st.dataframe(data)
