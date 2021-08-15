import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Initialize 'city' variable
    city = ' '

    # Continue asking for inputs until user selects valid option
    while city not in CITY_DATA:
        try:
            city = input("Enter a city from one of the following (Chicago, New York City, Washington):").lower()
        # Handle ValueErrors and give user another attempt to enter valid option
        except ValueError:
            print('Please try again with a valid city name.')
        # Prompt user for a valid input if one is not chosen
        if city not in CITY_DATA:
            print('Whoops! Looks like that city is not one of the three possible values. Please try again.')

    # Initialize 'month' variable
    month = ' '
    # Continue asking for inputs until user selects valid option
    while month not in MONTHS and month != 'all':
        try:
            month = input("Enter a specific month between to filter on between January through June, or enter 'all' for all months:").lower()
        # Handle ValueErrors and give user another attempt to enter valid option
        except ValueError:
            print('Please try again with a valid month option.')
        # Prompt user for a valid input if one is not chosen
        if month not in MONTHS and month != 'all':
            print('Please try again with a valid month option.')

    # Initialize 'day' variable
    day = ' '

    # Continue asking for inputs until user selects valid option
    while day not in calendar.day_name and day != 'All':
        try:
            day = input("Enter a specific day of the week to filter on or enter 'all' for all days:").title()
        # Handle ValueErrors and give user another attempt to enter valid option
        except ValueError:
            print('Please try again with a valid day option.')
        # Prompt user for a valid input if one is not chosen
        if day not in calendar.day_name and day != 'All':
            print('Please try again with a valid day option.')

    # Make day lowercase to match expected conditionals of other functions
    day = day.lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read CSV file pertaining to the selected city
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    month_mode = df['month'].mode()[0]
    month_mode = MONTHS[month_mode - 1].title()
    print('Most common month of travel is: {}'.format(month_mode))

    # Display the most common day of week
    day_mode = df['day_of_week'].mode()[0]
    print('Most common day of travel is: {}'.format(day_mode))


    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    # Find the most common hour (from 0 to 23)
    hour_mode = df['hour'].mode()[0]
    print('Most common start hour is:', hour_mode)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station_mode = df['Start Station'].mode()[0]
    print('Most common Starting Station is: {}'.format(start_station_mode))

    # Display most commonly used end station
    end_station_mode = df['End Station'].mode()[0]
    print('Most common Ending Station is: {}'.format(end_station_mode))

    # Display most frequent combination of start station and end station trip
    # Creating a new column that combines both stations into one value
    df['Combo Station'] = df['Start Station'] + '/' + df['End Station']

    # Find and print mode of  Combo Station column
    combo_station_mode = df['Combo Station'].mode()[0]
    print('Most common combination of Start and End Station is: {}'.format(combo_station_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('Total travel time is: {} hours'.format(df['Trip Duration'].sum()/3600))

    # Display mean travel time
    print('Mean travel time is: {} minutes'.format(df['Trip Duration'].mean()/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Verify 'User Type' column exists in DataFrame
    if "User Type" in df:
        print('User counts: \n{}\n'.format(df['User Type'].value_counts()))
    else:
        # Alert the user User Type data is not available
        print('User Type data not available, skipping User Type analysis.')


    # Display counts of gender
    # Verify 'Gender' column exists in DataFrame
    if "Gender" in df:
        print('Gender breakdown \n{}\n'.format(df['Gender'].value_counts()))
    else:
        # Alert the user Gender data is not available
        print('Gender data not available, skipping Gender analysis.')


    # Display earliest, most recent, and most common year of birth
    # Verify 'Birth Year' column exists in DataFrame
    if "Birth Year" in df:
        # Find earliest year using .min() method
        print('Earliest year of birth: {}'.format(int(df['Birth Year'].min())))

        # Find most recent year using .max() method
        print('Most recent year of birth: {}'.format(int(df['Birth Year'].max())))

        # Find most common year using .mode() method
        print('Most common year of birth: {}\n'.format(int(df['Birth Year'].mode()[0])))
    else:
        # Alert the user Birth Year data is not available
        print('Birth Year data not available, skipping Birth Year analysis.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask user if they would like to see raw data
        view_data = input('\nWould you like to view the first 5 lines of raw data? Enter yes or no.\n').lower()
        if view_data == 'yes':
            # Initialize 'x' variable to 0
            x = 0
            while view_data == 'yes':
                # Increment 5 lines of data each time the user is prompted
                x += 5
                print(df.head(x))
                view_data = input('\nWould you like to view another 5 lines of raw data? Enter yes or no.\n').lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
