# 5G Energy Consumption Dashboard (Simple)
# Streamlit app following the same lines/commands as energy-consumtion-dashboard.py
# Fitted to 5G_energy_consumption_dataset.csv

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="5G Energy Consumption Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# data
df = pd.read_csv('5G_energy_consumption_dataset.csv')

# sidebar
st.sidebar.header("5G Energy Consumption Dashboard")
# st.sidebar.image('tips.jpg')  # Commented out as image file is missing
st.sidebar.write("This dashboard is using 5G Energy Consumption dataset for educational purposes.")
st.sidebar.write("")
st.sidebar.write("Filter your data:")

# Add date/hour filtering
st.sidebar.subheader("Time Filtering")
time_filter = st.sidebar.selectbox("Time Filtering",[None,'Time'])
if time_filter == 'Time':
    # Extract hour from Time column for filtering
    df['Hour'] = pd.to_datetime(df['Time']).dt.hour
    hour_filter = st.sidebar.slider("Select Hour Range", 0, 23, (0, 23))
    df_filtered = df[(df['Hour'] >= hour_filter[0]) & (df['Hour'] <= hour_filter[1])]
else:
    df_filtered = df

st.sidebar.write("")
st.sidebar.write("Chart Filtering:")
cat_filter = st.sidebar.selectbox("Categorical Filtering",[None,'BS','Time'])
num_filter = st.sidebar.selectbox("Numerical Filtering",[None,'Energy','load','TXpower'])
size_filter = st.sidebar.selectbox("Size Filtering",[None,'Energy','load','TXpower'])
#row_filter = st.sidebar.selectbox("Row Filtering",[None,'BS'])
#col_filter = st.sidebar.selectbox("Column Filtering",[None,'BS'])
st.sidebar.write("")
st.sidebar.markdown("Made by :satellite: by Eng. Ehab El-Guindy")
# Add LinkedIn and GitHub links
st.sidebar.markdown("**Connect with me:**")
st.sidebar.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/ehab-el-guindy-375a4488)")
st.sidebar.markdown("[🐙 GitHub](https://github.com/ehabelguindy)")

# body

# row a
a1, a2, a3 = st.columns(3)

with a1:
    st.metric("Max. Energy", f"{df_filtered['Energy'].max():.2f} W")
    st.metric("Min. Energy", f"{df_filtered['Energy'].min():.2f} W")

with a2:
    st.metric("Max. Load", f"{df_filtered['load'].max():.2f} %")
    st.metric("Min. Load", f"{df_filtered['load'].min():.2f} %")

with a3:
    st.metric("Max. TX Power", f"{df_filtered['TXpower'].max():.2f} W")
    st.metric("Min. TX Power", f"{df_filtered['TXpower'].min():.2f} W")

# row b
st.subheader("Energy vs. Load (with size filtering)")
fig = px.scatter(data_frame=df_filtered, 
                 x='Energy',
                 y='load',
                 color=num_filter,  # Use num_filter for color intensity
                 size=size_filter,
                 size_max=30,  # Increase max size for better visibility
                 hover_data=['Time', 'BS', 'TXpower'],
                 title="Energy Consumption vs Load with Color and Size Filtering")
st.plotly_chart(fig, use_container_width=True)

# row c - Base Station vs Average Energy Bar Chart
st.subheader("Base Station vs. Average Energy Consumption")
# Calculate average energy by base station (using full dataset, not filtered)
avg_energy_by_bs = df.groupby('BS')['Energy'].mean().reset_index()
avg_energy_by_bs = avg_energy_by_bs.sort_values('Energy', ascending=False)

# Add load-based coloring (high load = red, low load = green)
avg_load_by_bs = df.groupby('BS')['load'].mean().reset_index()
avg_energy_by_bs = avg_energy_by_bs.merge(avg_load_by_bs, on='BS')

# Create color mapping based on load
avg_energy_by_bs['load_category'] = pd.cut(avg_energy_by_bs['load'], 
                                          bins=[0, 50, 100], 
                                          labels=['Low Load', 'High Load'])

fig_bar = px.bar(data_frame=avg_energy_by_bs, 
                 x='BS', 
                 y='Energy',
                 color='load_category',
                 color_discrete_map={'Low Load': 'green', 'High Load': 'red'},
                 title="Average Energy Consumption by Base Station (Colored by Load Level)",
                 labels={'Energy': 'Average Energy (W)', 'BS': 'Base Station'})

fig_bar.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_bar, use_container_width=True)



# row d - Energy Share by Hour (Donut Chart)
st.subheader("Energy Share by Hour")
# Extract hour from Time column (using full dataset, not filtered)
df['Hour'] = pd.to_datetime(df['Time']).dt.hour
df['DayOfWeek'] = pd.to_datetime(df['Time']).dt.day_name()

# Calculate total energy by hour
energy_by_hour = df.groupby('Hour')['Energy'].sum().reset_index()
energy_by_hour['Hour_Label'] = energy_by_hour['Hour'].apply(lambda x: f"{x:02d}:00")

fig_donut = px.pie(data_frame=energy_by_hour, 
                   names='Hour_Label', 
                   values='Energy',
                   hole=0.4,  # Creates donut chart
                   title="Energy Consumption Share by Hour of Day",
                   labels={'Energy': 'Total Energy (W)', 'Hour_Label': 'Hour'})

st.plotly_chart(fig_donut, use_container_width=True)


