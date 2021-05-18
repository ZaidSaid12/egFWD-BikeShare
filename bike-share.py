#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np


# In[2]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ["january","february","march","april","may","june"]
days = ["saturday","sunday","monday","tuesday","wednesday","thurdsay","friday"]


# In[3]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    # get user input for month (all, january, february, ... , june)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while(True):
        city = input("Please enter the name of the city (chicago, new york city, washington): ").lower().strip()
        if city not in ["chicago", "new york city", "washington"]:
            print("Please enter a valid city from the provided")
            continue
        month = input("Please enter the month to filter{} or write 'all' to show all months: ".format(months)).lower()
        if month not in months and month != "all":
            print("Please enter a valid month")
            continue
        day= input("Please enter the day to filter {} or write 'all: ".format(days)).lower()
        if day not in days and day != "all":
            print("Please enter a valid month")
            continue
        break
    print('-'*40)
    return city, month, day


# In[4]:


def display_data(df):
    index=0
    user_input=input('would you like to display 5 rows of raw data? ').lower()
    while user_input in ['yes','y','yep','yea'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('would you like to display more 5 rows of raw data? ').lower()
    print('-'*40)


# In[12]:


def load_data(city, month , day ):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df =df[df['month'] == month] 
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
   
    print('-'*40)

    return df


# In[6]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    common_month = int(common_month)
    common_month_name = months[common_month-1]
    print("The most common month: ", common_month_name.title())

    # display the most common day of week
    common_day=df['day_of_week'].mode()[0]
    print("The most common day of week: ", common_day.title())


    # display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common start hour: ",common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[7]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most common start station: ", common_start_station)
    
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most common end station: ", common_end_station)

    # display most frequent combination of start station and end station trip
    start_end_combination = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most common combinaton: Start Station: {}, End Station: {}".format(start_end_combination.iloc[0],start_end_combination.iloc[1]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[8]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    seconds = df['Trip Duration'].sum()
    seconds_in_day = 60 * 60 * 24
    seconds_in_hour = 60 * 60
    seconds_in_minute = 60

    days = seconds // seconds_in_day
    hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
    minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute
    seconds = seconds % minutes
    print("Total travel time: {} days, {} hours, {} minutes, {} seconds".format(days, hours, minutes, seconds))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    average_hours = mean_time// seconds_in_hour
    average_minutes = (mean_time - (average_hours * seconds_in_hour)) // seconds_in_minute
    average_seconds = mean_time % average_minutes

    print("Average Trip Duration: {} hours, {} minutes, {} seconds ".format(average_hours, average_minutes, average_seconds))
    
    #display travel time for each user (extra feature)
    user_travel = df[['User Type', 'Trip Duration']].groupby(['User Type']).sum()
    user_travel['hours'] = user_travel['Trip Duration'] // seconds_in_hour
    user_travel['minutes'] = (user_travel['Trip Duration'] - user_travel['hours']*seconds_in_hour)//seconds_in_minute
    user_travel['seconds'] = user_travel['Trip Duration'] % user_travel['minutes']
    user_travel = user_travel.drop(['Trip Duration'], axis=1)
    
    print("\nTrip Duration for each User Type: ")
    print(user_travel)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[9]:


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    subscriber_count= df['User Type'].value_counts().iloc[0]
    customer_count = df['User Type'].value_counts().iloc[1]
    print("Count of Subscribers: {} \nCount of Customers: {}".format(subscriber_count, customer_count)) 
    print('-'*20)
    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    if city in ['chicago', 'new york city']:
        male_count = df['Gender'].value_counts().iloc[0]
        female_count = df['Gender'].value_counts().iloc[1]
        print("Count of Males: {} \nCount of Females: {}".format(male_count, female_count)) 
        print('-'*20)
        print("Earliest year of birth: ", int(df['Birth Year'].min()))
        print("Most recent year of birth: ", int(df['Birth Year'].max()))
        print("Most common year of birth: ", int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[10]:


def main():
    while True:
        city, month, day = get_filters()
        #city, month, day = "chicago", "may", "tuesday"
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Bye, have a nice one!")
            break


# In[13]:


main()


# In[ ]:




