#===============================IMPORT=================================
import streamlit as st
import pandas as pd #untuk pengolahn data
from pandas import read_csv
import csv #library biar bisa ngabaca file excel/csv
import plotly.express as px
from PIL import Image
import numpy as np
from streamlit_option_menu import option_menu
import mysql.connector

#### ----- NAVIGATION BAR ---- ####
selected = option_menu(
    menu_title="US Covid-19 Data Center",
    options=["Home", "Graph",  "Show"],
    icons=["house", "bar-chart-line","columns"],
    menu_icon="caret-right-square-fill",
    orientation="horizontal",
    styles={
                "container": {"padding": "0!important", "background-color": "black"},
                "icon": {"color": "white", "font-size": "10px"},
                "nav-link": {
                    "font-size": "15px",
                    "font-colour": "white",
                    "text-align": "center",
                    "margin": "0px",
                    "--hover-color": "#eeeee",
                },
                "nav-link-selected": {"background-color": "#696666"},
            },
    )

#### ----- SECTION HOME ---- ####
if selected == "Home":
    
    df = pd.read_csv("123.csv")
    
    #---------------- MAPS --------------------
    nyc_coord = [40.7128, -74.0060]
    df = pd.DataFrame([nyc_coord], columns=["lat", "lon"])
    st.header("Map of NY-United States")
    st.map(df)
    
    #--------- DESCRIPTION  -------------------
    st.header("Description")
    st.markdown("_In 2020, New York was one of the hardest hit states in the United States during the COVID-19 pandemic. The state reported its first case of COVID-19 on March 1st, 2020 and the numbers of cases quickly skyrocketed. By the end of March, New York had become the epicenter of the pandemic in the US, with the largest number of confirmed cases and fatalities. The state implemented a range of measures to curb the spread of the virus, including shutting down non-essential businesses, implementing social distancing guidelines, and encouraging residents to wear masks. Despite these efforts, New York reported over 1 million confirmed cases and over 50,000 deaths by the end of the year._") 
    
    st.markdown("---")

    #--------- COMPLAINT FORM  -------------------
    centered_text = """
    <div style="display: flex; justify-content: center;">
    <h4>Complaint Form </h4>
    </div>
    """
    st.markdown(centered_text, unsafe_allow_html=True)
    # Define the form fields
    form = st.form(key='my_form')
    name = form.text_input('Name')
    location = form.text_input('Location')
    phone = form.text_input('Phone')
    complaint = form.text_area('Complaint')
    submit = form.form_submit_button('Submit')
    st.caption ("u can drop your complaint about covid-19 in this form")
        
    #------------- INFO SECTION ------------------
    st.markdown("---")
    centered_text = """
    <div style="display: flex; justify-content: center; ">
    <h6> <em> It's My First Time w/ Streamlit </em></h6>
    </div>
    """
    st.markdown("Dataset:[OpenAI](https://data.humdata.org/dataset/nyt-covid-19-data/resource/34450bc6-76e5-49a5-879e-26edfa7b3b27)")
    st.markdown(centered_text, unsafe_allow_html=True)
    st.markdown("---")
    
    # Connect to the database
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='covidform')

    # Define a function to show the data in a table
    if submit:
        cursor = cnx.cursor()
        query = "INSERT INTO my_table (name, location, phone, complaint) VALUES (%s, %s, %s, %s)"
        values = (name, location, phone, complaint)
        cursor.execute(query, values)
        cnx.commit()
        st.success("Data added to database")

    # Close the database connection
    cnx.close()
#### ----- SECTION GRAPH ---- ####
if selected == "Graph":
    
        #------ Chart Cases  ------------
        col1, col2 = st.columns([20, 12]) #padding
        data_ = np.random.randn(21, 5)  #jumlah baris, kolom
        data = pd.read_csv("123.csv" )
        col1.markdown("**Cases in State**")
        col1.line_chart(data, x="state", y="cases", height=400, width=800)
        col2.write(data)
        
      #------ Diagram Date Case -----------
        data1 = pd.read_csv("123.csv" ) #path folder of the data file
        bar_Tinggal_state = px.bar(data1, x="date", y="cases", color='state', height=400, width=800, title="State Case Count")
        bar_Tinggal_state.update_layout(title_text='State Case Count')
        st.plotly_chart(bar_Tinggal_state)
        
     #------ Diagram Date Deaths ------------
        bar_Tinggal_death = px.bar(data1, x="date", y="deaths", color='state', height=400, width=800, title="State Death Count")
        bar_Tinggal_death.update_layout(title_text='State Death Count')
        st.plotly_chart(bar_Tinggal_death)
        
     #------ Data Tabel -----------
        st.markdown("**Data Tabel**")
        data1 = data1.groupby('date').mean().head()
        data1 = data1.style.set_properties(**{'background-color': 'black',
                            'color': 'white'})
        st.table(data1)
        
        
 #### ----- SECTION SHOW---- ####   
if selected == "Show":

    data = pd.read_csv("123.csv" ) #path folder of the data file
    
    #----------------------- Search Bar----------------------------------------
    st.header("Search Bar") # Create a title for the dashboard
    search_term = st.text_input("Enter The City") # Add a search box to the top of the dashboard

    #-------- Show the filtered data based on the search term ------------------
    if search_term:
        filtered_df = data[data["state"].str.contains(search_term, case=False)]
        st.write(filtered_df)
    else:
        st.write("Enter a search term to filter the data")

    #-------------------------- Show Full Data Table ---------------------------
    st.header("\n Show Full Data")
    st.table(data)
    #--------------------------------------------------------------------------
