import os
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Corrected database connection using an absolute path
base_dir = os.path.dirname(__file__)
db_path = os.path.join(base_dir, '..', 'db.sqlite3')

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

def add_fuel_log(vehicle_id, fuel_date, fuel_quantity, total_cost):
    conn = get_db_connection()
    conn.execute('INSERT INTO fuel_log (vehicle_id, fuel_date, fuel_quantity, total_cost) VALUES (?, ?, ?, ?)', (vehicle_id, fuel_date, fuel_quantity, total_cost))
    conn.commit()
    conn.close()

def get_fuel_logs():
    conn = get_db_connection()
    fuel_logs = conn.execute('SELECT * FROM fuel_log').fetchall()
    conn.close()
    return fuel_logs

# Set page title and general information
st.title('Fleet Management System')
st.markdown('Welcome to our Fleet Management System. This dashboard allows you to manage vehicles, drivers, and maintenance records.')

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = ""

# Sidebar Navigation with Buttons
st.sidebar.title("Navigation")
st.sidebar.markdown('---')  # Add a horizontal line for better separation
if st.sidebar.button("Vehicle Information", key="vehicle_info_btn", help="Click to view vehicle information"):
    st.session_state['page'] = "Vehicle Information"
if st.sidebar.button("Driver Information", key="driver_info_btn", help="Click to view driver information"):
    st.session_state['page'] = "Driver Information"
if st.sidebar.button("Maintenance Information", key="maintenance_info_btn", help="Click to view maintenance information"):
    st.session_state['page'] = "Maintenance Information"
if st.sidebar.button("Fuel Log Information", key="fuel_log_info_btn", help="Click to view fuel log information"):
    st.session_state['page'] = "Fuel Log Information"

# Main content based on selected page
if st.session_state['page'] == "Vehicle Information":
    st.title('Vehicle Information')
    vehicles = pd.read_sql_query('SELECT * FROM vehicles', get_db_connection())
    st.dataframe(vehicles)

    # Add New Vehicle Section
    st.subheader('Add New Vehicle')
    make = st.text_input('Make', key='make_input')
    model = st.text_input('Model', key='model_input')
    year = st.number_input('Year', key='year_input')
    if st.button('Add Vehicle', key='add_vehicle_btn'):
        add_vehicle(make, model, year)
        st.success('Vehicle added successfully!')

elif st.session_state['page'] == "Driver Information":
    st.title('Driver Information')
    drivers = pd.read_sql_query('SELECT * FROM drivers', get_db_connection())
    st.dataframe(drivers)

    # Add New Driver Section
    st.subheader('Add New Driver')
    name = st.text_input('Name', key='name_input')
    license_number = st.text_input('License Number', key='license_input')
    if st.button('Add Driver', key='add_driver_btn'):
        add_driver(name, license_number)
        st.success('Driver added successfully!')

elif st.session_state['page'] == "Maintenance Information":
    st.title('Maintenance Information')
    maintenance_records = pd.read_sql_query('SELECT * FROM maintenance', get_db_connection())
    st.dataframe(maintenance_records)

    # Add New Maintenance
    st.subheader('Add New Maintenance')
    description = st.text_input('Description', key='description_input')
    date = st.date_input('Date', key='date_input')
    if st.button('Add Maintenance', key='add_maintenance_btn'):
        add_maintenance(description, date)
        st.success('Maintenance added successfully!')

elif st.session_state['page'] == "Fuel Log Information":
    st.title('Fuel Log Information')
    fuel_logs = get_fuel_logs()
    df_fuel_logs = pd.DataFrame(fuel_logs, columns=['id', 'vehicle_id', 'fuel_date', 'fuel_quantity', 'total_cost'])
    
    # Responsive Bar Chart for Fuel Levels
    df_fuel_logs['fuel_level'] = df_fuel_logs['fuel_quantity'] / df_fuel_logs['total_cost']
    df_fuel_logs['fuel_status'] = df_fuel_logs['fuel_status'] = df_fuel_logs['fuel_level'].apply(lambda x: 'Full' if x >= 0.8 else ('Moderate' if x >= 0.4 else 'Low'))
    
    # Responsive Bar Chart for Fuel Levels
    fig_fuel = px.bar(df_fuel_logs, x='fuel_date', y='fuel_quantity', color='fuel_status', title='Fuel Log with Status')
    st.plotly_chart(fig_fuel)