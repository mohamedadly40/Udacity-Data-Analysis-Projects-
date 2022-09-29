import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

filter_city = 'All'
filter_month = 'All'
filter_day = 'All'
start_Bold = '\033[1m'
end_Bold = '\033[0;0m'
start_underline = '\033[4m'
end_underline = '\033[0m'

def get_filters():
    print(start_Bold + '\nHello! Let\'s explore some US bikeshare data!' + end_Bold)
    global filter_city
    filter_city = input('>>> Would you like to see data for "Chicago", "New York City", or "Washington"?').title()
    while filter_city not in CITY_DATA.keys():
        print('Invalid Selection')
        filter_city = input('>>> Would you like to see data for "Chicago", "New York City", or "Washington"?').title()

    filter_month_day = input('\n>>> Would you like to filter the data by "month", "day", or "both"?').lower()
    while filter_month_day not in(['month', 'day', 'both']):
        print('Invalid Selection')
        filter_month_day = input('>>> Would you like to filter the data by "month", "day", or "both"?').lower()

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    if filter_month_day == 'month' or filter_month_day == 'both':
        global filter_month
        filter_month = input('\n>>> Which month from below months list or select "all"\n{}.'.format(months[:6])).title()
        while filter_month not in months:
            print('Invalid Selection')
            filter_month = input('>>> Which month from below months list or select "all"\n{}.'.format(months[:6])).title()

    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']
    if filter_month_day == 'day' or filter_month_day == 'both':
        global filter_day
        filter_day = input('\n>>> Which day from below months list or select "all"\n{}.'.format(days[:7])).title()
        while filter_day not in days:
            print('Invalid Selection')
            filter_day = input('>>> Which day from below months list or select "all"\n{}.'.format(days[:7])).title()

    print('\nYour selections are (City: "{}", Month: "{}" and Day: "{}").'.format(filter_city, filter_month, filter_day))
    print('-'*40)
    return filter_city, filter_month, filter_day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Month'] = df['Month'].replace([1, 2, 3, 4, 5, 6], ['January', 'February', 'March', 'April', 'May', 'June'])
    df['Day'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    df['User Type'] = df['User Type'].fillna('Unknown User Type')
    if filter_city != 'Washington':
        df['Gender'] = df['Gender'].fillna('Unknown Gender')

    if month != 'All':
        df = df[df['Month'] == month.title()]
    if day != 'All':
        df = df[df['Day'] == day.title()]
    return df

def time_stats(df):
    print(start_Bold + 'Displays Popular "Times Of Travel" Statistics...\n' + end_Bold)
    start_time = time.time()
    print('-- The most Popular month of travel is : "{}"'.format(df['Month'].mode()[0]))
    print('-- The most Popular day of travel is : "{}"'.format(df['Day'].mode()[0]))
    print('-- The most Popular hour of travel is : "{}"'.format(df['Hour'].mode()[0]))

    print("\n-- This took %s seconds." % (time.time() - start_time))
    print('-' * 40)

    return

def station_stats(df):
    print(start_Bold + 'Displays Popular "Stations & Trip" Statistics...\n' + end_Bold)
    start_time = time.time()
    print('-- The most Popular start station: {}'.format(df['Start Station'].mode()[0]))
    print('-- The most Popular end station: {}'.format(df['End Station'].mode()[0]))
    df['Trip_from_to'] = df['Start Station']+" - "+df['End Station']
    print('-- The most Popular combination of start station and end station: {}'.format(df['Trip_from_to'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return

def trip_duration_stats(df):
    print(start_Bold + 'Displays "Total & Average Trip Duration" Statistics...\n' + end_Bold)
    start_time = time.time()

    print('-- Total Travel Time in Seconds: {}'.format(df['Trip Duration'].sum()))
    print('-- Average Travel Time in Seconds: {}'.format(df['Trip Duration'].mean()))

    print("\n-- This took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return

def user_stats(df):

    print(start_Bold + 'Displays "Bike-share Users" Statistics...\n' + end_Bold)
    start_time = time.time()
    user_type = df['User Type'].value_counts()
    print(start_underline + (start_Bold+'User Type Statistics'+end_Bold) + end_underline)
    print(user_type)
    if filter_city != 'Washington':
        gender_type = df['Gender'].value_counts()
        print(start_underline + (start_Bold+'\nGender Type Statistics'+end_Bold) + end_underline)
        print(gender_type)
        print('\n-- The Earliest birth year: {}'.format(df['Birth Year'].min()))
        print('-- The Most Recent birth year: {}'.format(df['Birth Year'].max()))
        print('-- The Most Common year of birth: {}'.format(df['Birth Year'].mode()[0]))

    print("\n-- This took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data not in(['yes', 'no']):
        print('Invalid Selection')
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    while view_data != 'no':
        print(df.iloc[start_loc:(start_loc+5)])
        start_loc += 5
        view_data = input('\nDo you wish another 5 rows\n').lower()

    return

def main():
    while True:
        filter_city, filter_month, filter_day = get_filters()
        df = load_data(filter_city, filter_month, filter_day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
