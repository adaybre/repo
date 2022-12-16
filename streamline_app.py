"""
Class: CS230--Section 004
Name: Alden Daybre
Description: Final Project: Boston Crime Data
I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk


# Read in files
def read_in(file1, file2):
    df = pd.read_csv(file1,
                 header = 0)
    dfd = pd.read_csv(file2,
                 header = 0)
    return df, dfd


# Display a map of Boston Crime
def map(df):
    df.rename(columns = {'Long':'lon', 'Lat':'lat'}, inplace = True)
    st.write("Map of Crime in Boston")
    st.map(df)


# Count number of crimes per day of week
def day_count(df):
    a = list(df['DAY_OF_WEEK'])
    dayN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dayC = []
    for day in dayN:
        count = 0
        count = a.count(day)
        dayC.append(count)
    return dayC, dayN


# Count number of crimes per month
def month_count(df):
    month_count_list = []
    monthN = ['January', 'February', 'March', 'April', 'May', 'June']
    for i in range(1,6):
        df2 = df.query('MONTH ==@i')
        count = df2.count()
        number = count[0]
        month_count_list.append(number)
    return month_count_list, monthN


# Radio button selection and display of crime data by hour, day, and month
def crime_time(df, dayC, dayN, month_count_list, monthN):
    st.subheader("Crime by Time")
    time = st.radio("What time filter would you like to use?",
                      ('Hour', 'Day', 'Month'))
    if time == 'Hour':
        st.write('You selected Hour.')
        st.subheader('Number of Crimes by Hour')
        hour_values = np.histogram(
        df['HOUR'], bins=24, range=(0,24))[0]
        # st.bar_chart(hour_values)
        st.line_chart(hour_values)
    elif time == 'Day':
        st.write('You selected Day.')
        chart, ax = plt.subplots()
        plt.xticks(range(len(dayN)), dayN)
        plt.xlabel('Day of Week')
        plt.ylabel('# of Crimes')
        plt.title('Total Crimes by Day of Week, 2021')
        ax.bar(range(len(dayC)), dayC, width=.75, color='b')
        st.pyplot(fig=chart)
    else:
        st.write('You selected Month.')
        st.subheader('Number of Crimes by Month')
        chart, ax = plt.subplots()
        plt.xlabel('Month')
        plt.ylabel('# of Crimes')
        plt.title('Total Crimes by Month, 2021')
        # month_count_list, monthN = month_count(df)
        plt.xticks(range(len(monthN)), monthN)
        ax.bar(range(len(month_count_list)), month_count_list, width=.75)
        st.pyplot(fig=chart)


# Pie chart of shooting vs. non-shooting crime incidents
def shootings(df):
    shootings = []
    for i in range(0,2):
        df2 = df.query('SHOOTING ==@i')
        count = df2.count()
        number = count[0]
        shootings.append(number)
    labels = 'No Shooting', 'Shooting'
    explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    plt.title('Crimes in Boston involving shooting')
    ax1.pie(shootings, explode=explode, labels=labels, autopct='%1.1f%%', startangle=50)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig=fig1)


# Sort dataframe by date and display
def sort_date(df):
    df3 = df.sort_values('OCCURRED_ON_DATE')
    st.dataframe(data=df3)


# Multi-select query of district and offense description and display
# The pie chart is fully responsive to user input, including the title!
def district_crime(df,dfd):
    st.subheader("Crime by District")
    offense_list = df["OFFENSE_DESCRIPTION"].values.tolist()
    unique_offense_list = []
    for i in offense_list:
        if i not in unique_offense_list:
            unique_offense_list.append(i)
    st.dataframe(dfd)
    default_ix = unique_offense_list.index('ROBBERY')
    district_code = st.text_input('Enter a district code', 'A1')
    crime_desc = st.selectbox("Choose a type of crime", unique_offense_list, index=default_ix)
    df3 = df.loc[(df['DISTRICT'] == district_code) & (df['OFFENSE_DESCRIPTION'] == crime_desc)]
    count = df3['OFFENSE_DESCRIPTION'].value_counts()[crime_desc]
    df4 = df.loc[(df['OFFENSE_DESCRIPTION'] == crime_desc)]
    count_total = df4['OFFENSE_DESCRIPTION'].value_counts()[crime_desc]
    st.subheader(f"The number of crime type: '{crime_desc}' in district {district_code} is {count}")
    st.subheader(f"The total number of crime type: '{crime_desc}' is {count_total}")
    other = count_total - count
    dist_pie = []
    dist_pie.append(count)
    dist_pie.append(other)
    labels = district_code, 'Other'
    explode = (0, 0.1)
    fig1, ax1 = plt.subplots()
    plt.title(f'Share of total crime type {crime_desc} for district {district_code}')
    ax1.pie(dist_pie, explode=explode, labels=labels, autopct='%1.1f%%', startangle=180)
    ax1.axis('equal')
    st.pyplot(fig=fig1)


# Streamlit webpage setup and sidebar/page select
df = pd.read_csv('Boston_Crime_Date.csv',
                 header = 0)
df, dfd = read_in('Boston_Crime_Date.csv', 'Boston_Police_Districts.csv')
dayC, dayN = day_count(df)
st.title("Final Project - Alden Daybre")
st.header("Crime Statistics in Boston January - May 2021")
if st.checkbox("Click to display the image!"):
    st.image("Boston.jpeg")
# Image source: https://www.travelandleisure.com/travel-guide/boston
page = st.sidebar.selectbox('Select page',['Time Data', 'Crime Map', 'Shootings', 'Sorted Date', 'District Crime'])
if page == 'Time Data':
    month_count_list, monthN= month_count(df)
    crime_time(df, dayC, dayN, month_count_list, monthN)
elif page == 'Crime Map':
    map(df)
elif page == 'Shootings':
    shootings(df)
elif page == 'Sorted Date':
    sort_date(df)
elif page == 'District Crime':
    district_crime(df, dfd)
else:
    pass



