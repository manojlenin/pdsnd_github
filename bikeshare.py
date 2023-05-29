import time
import pandas as pd
import numpy as np
import sys

""" By Manoj:- Dictionary to store data for csv file for respecitve city. Key hold the city name and value with filename"""
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

""" By Manoj:- List that contains month name in sequesnce. This list will later be used to validate user input"""
MONTHS_DATA = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december','all']

""" By Manoj:- List that contains weekday name in sequesnce. This list will later be used to validate user input"""
WEEKDAYS_DATA = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']

no_of_tries = 3

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

    """ By Manoj:-
    User input needs to be validated against the list to avoid wrong input from user. 
    hence the while loop is been separated to a function get_user_input to avoid redundancy.
    """
    city = get_user_input("Pick a city from \n[Chicago, New York City, Washington] \n: ", CITY_DATA)
    month = get_user_input("Pick a month from January to June or enter 'all' : ", MONTHS_DATA)
    day = get_user_input("You got any specific day of the week? or enter 'all' : ", WEEKDAYS_DATA)

    print('-'*40)
    print('*' * 40)

    """By Manoj:- aquired input is returned as function output"""
    return city, month, day


def get_user_input(inputdesp, listtocheck):
    """ By Manoj:-
    This function will prompt users to enter an raw data for CITY, MONTH and DAY. Which will then be validated against the list
    declared after import statement. the raw input could be of any types, as user have different styles of typing and with poss
    -ible typo as well. to avoid such unexpected input, the raw input is converted lower case, and validated against the list d-
    -clared as mentioned above.
                                Since this a while an counter is been declared to control the loop and exit after certain no of
    iteration. This value can be controlled using the variable "no_of_tries". currently its set to 3.
    :param inputdesp: The text passed to the variable will be displayed to the user while receiving the raw input
    :param listtocheck: This variable holds the list that is been declared at teh beginning of the script
    :return: And returns the raw input that is converted to lower case and validated for CITY, MONTH and DAY
    """
    counter = 1
    while True:

        """By Manoj:- user input is initated and concerted to lower case and stored in rawdata"""
        rawdata = input(inputdesp).lower().strip()

        """By Manoj:- rawdata is validated and check whether it is present in the given list or dictionary"""
        if rawdata in listtocheck:

            """By Manoj:- Since there are two different types of data structure are declared, the type of the data structureis used perfrom validation.
            if the data structure is an DICT, the key is used to reterive the value from dict and returned.
            if the data structure is an LIST then the rawdata is returned directly
            if the validation is true, ie., if user input exists in the data structure, the loop will break and exist at line 76
             """
            if type(listtocheck) is dict:
                userdata = listtocheck[rawdata]
                return userdata
            else:
                return rawdata
            break

        """By Manoj:- Counter is compared with no_of_tried, everytime user entered a wrong data. if counter value is greater that no of tries then the 
        program exists at line 82"""
        if counter >= no_of_tries:
            sys.exit("Exiting program, get correct data and try again!")
            break
        else:
            print("Chances left are : {}/{}\n".format((no_of_tries - counter), no_of_tries))
        counter += 1

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
    """By Manoj:- all .csv files are stored under Datafolder to keep it organized. hence when loading the data, the folder name is
    concatenated with filename that was returned by filter function"""
    df = pd.read_csv("./Datafolder/"+city)

    #filter df by month
    """By Manoj:- Convert Start time to datetime datatype in the dataframe."""
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    """By Manoj:- Create a new column with name month and convert the month int from start date to its corresponding name and store it"""
    df["month"] = df["Start Time"].dt.month_name()

    """By Manoj:- Create a new column with name hour and extract the hour from start time and store in the column"""
    df["hour"] = df["Start Time"].dt.hour

    """By Manoj:- Check whether month variable have value as 'all', because if user request for all month then no need to filter 
    the df on month"""
    if month != 'all':

        """By Manoj:- If user request for certain month, then filter the df for that respective month"""
        df = df[df['month'] == month.title()]

    #--------- filter df by day----------------
    """By Manoj:- Create a new column with name weekdayname and convert the date from start date to its corresponding weekday"""
    df['weekdayname'] = df['Start Time'].dt.day_name()

    """By Manoj:- Check whether day variable have value as 'all', because if user request for all day of the week then no need to filter 
        the df on day"""
    if day != 'all':

        """By Manoj:- If user request for certain day of the week, then filter df for that respective day"""
        df = df[df['weekdayname'] == day.title()]

    """By Manoj:- return the filtered df based on user raw input"""
    return df


def time_stats(df,city, month, day):
    """Displays statistics on the most frequent times of travel."""
    """By Manoj:- This function performs the filter and displauing of statical data on time"""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    """By Manoj:- This scenario is valid only when there are more than 1 month in the dataframe, 
    hence check whether user opted for all month or or just one month"""
    if month == 'all':

        """By Manoj:- The method mode() returns the most frequent data from a column, in this case is the month that is most frequent
        and the using the value and index 0 the month name is returned and displayed"""
        print("-> Month that had high frequency travel is  : ",df.month.mode().values[0])

        """By Manoj:- the below method value_counts() will return top 5 frequent months from DF, hence slicing is used on value_counts and converted to list.
        the list is then iterated over to display the month name in its order"""
        print(">>>Top 5 most frequent month are :")
        idx = 1
        for monthname in df.month.value_counts()[:5].index.tolist():
            print("\t\t{}. {}".format(idx, monthname))
            idx += 1

    # display the most common day of week
    """By Manoj:- The method mode() returns the most frequent data from a column, in this case is the weekday that is most frequent
        and by using the value and index 0 the weekday name is returned and displayed"""
    if day == 'all':
        print("*> Weekday that had high frequency travel is : ",df.weekdayname.mode().values[0])

        # display the most common start hour
        """By Manoj:- The method mode() returns the most frequent data from a column, in this case is the hour that is most frequent
                and by using the value and index 0 the hour is returned and displayed"""
        print("*> Most frequent hour of travel is : ",df.hour.mode().values[0])

    """By Manoj:- the below method  value_counts() will return top 5 frequent hours from DF, hence slicing is used on value_counts and converted to list.
           the list is then iterated over to display the weekday name in its order"""
    print(">>>Top 5 most frequent hours are :")
    hridx = 1
    for hrs in df.hour.value_counts()[:5].index.tolist():
        print("\t\t{}. {}".format(hridx, hrs))
        hridx += 1

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    """By Manoj:- Using the method mode() the most frequent start station is returned"""
    print("\n*> Start station that had frequent users is : ", df["Start Station"].mode().values[0])

    # display most commonly used end station
    """By Manoj:- Using the method mode() the most frequent end station is returned"""
    print("\n*> Most station where the trip ended is : ", df["End Station"].mode().values[0])


    # display most frequent combination of start station and end station trip
    """By Manoj:- Group by method is used to combine data from two column and the max count of the data is returned as set. Then the idex of the 
        returned value is used to display the station combination"""
    station_trip_between = df.groupby(["Start Station","End Station"]).size().idxmax()
    print("\n*> Most frequest trip between stations are :\n\tStart station: \t\t{} \n\tEnd station: \t\t{}".format(station_trip_between[0],station_trip_between[1]))

    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    """By Manoj:- All the hours in DF after being filtred based on the user input is returned using sum(). The returned value is then
        formatted using time library to display in HH:MM:SS format"""
    tot_time = time.strftime("%H:%M:%S", time.gmtime(df["Trip Duration"].sum()))

    """"By Manoj:- This is the raw value returned by sum() method"""
    print("Raw value of the total travel time is :", df["Trip Duration"].sum())

    """"By Manoj:- This is the formatted time value"""
    print("*> Total trip duration until given period is : ",formattime(tot_time))


    # display mean travel time
    """"By Manoj:- mean() is used to get the mean values for the hours in DF. the returned values is hen formatted 
        using time lib to H:M:S format"""
    mean_time = time.strftime("%H:%M:%S", time.gmtime(df["Trip Duration"].mean()))

    """"By Manoj:- below is the raw value from the mean() method"""
    print("\nRaw value of the mean travel time is :", df["Trip Duration"].mean())

    """"By Manoj:- below is the formatted value from the mean() method"""
    print("*> Mean value of trip duration until given period is : ", formattime(mean_time))

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)

def formattime(in_time):
    timefrac = in_time.split(":")
    return "{}Hrs {}mins {}sec".format(timefrac[0],timefrac[1],timefrac[2])


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    """"By Manoj:- value_cout() is used to return the count of user types, although the returned values was not in formatted manner
    hence the axis are renamed with rename_axis as user type and counts respectively"""
    usertypes = df['User Type'].value_counts().rename_axis('user types').reset_index(name='counts')
    print("*> Types of user and its count in the given data are \n{}".format(usertypes))


    # Display counts of gender
    """"By Manoj:- value_cout() is used to return the count of user types, although the returned values was not in formatted manner
        hence the axis are renamed with rename_axis as user type and counts respectively"""
    print("\nGender types and its count in the given data are:")

    """"By Manoj:- Not all DF have the gender column, hence this 'if' condition is used to manage this request"""
    if 'Gender' in df.columns:

        """"By Manoj:- if the column exists then the relavent data is reterieved and axis names are renamed and published"""
        gendercount = df['Gender'].value_counts().rename_axis('Gender').reset_index(name='counts')
        print("\n{}".format(gendercount))
    else:

        """"By Manoj:- if the column does not exists then a msg to notify that the column not available"""
        print("\t\tNo column exist for the given data set")

    # Display earliest, most recent, and most common year of birth
    """"By Manoj:- Not all DF have the gender column, hence this 'if' condition is used to manage this request"""
    if 'Birth Year' in df:

        """"By Manoj:- if the column exists then the relavent data is reterieved and axis names are renamed and published"""
        """"By Manoj:- Birth year column data type was float, hence the returned data had decimal values. in order to convert the 
            the column values to int astypes is used. If there happens to be any NAN values then the astypes to int will fail.
            Hence the DF is cleaned by replacing the NAN to 0 and then changes to astypes int."""
        df['Birth Year'] = df['Birth Year'].fillna(0).astype(int)

        """"By Manoj:- Since the column has the value as 0, the min values would alway be 0, which is not a values output, hence the DF is filtered 
            to remove 0 from the column and aggreation operation is performed on the resulting data."""
        df = df[df['Birth Year'] != 0]
        earliestyear = df['Birth Year'].min()
        recentyear = df['Birth Year'].max()
        commonyear = df['Birth Year'].mode().values[0]
        print("\nEarliest entry of year of birth \t{} \nmost recent entry of birth year \t{} \nAnd most common year of birth \t\t{}".format(earliestyear,recentyear, commonyear))
    else:

        """"By Manoj:- if the column does not exists then a msg to notify that the column not available"""
        print("Earliest year of birth details.\n\t\tNo such column exists in the df")


    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)

def reterieve_all_data(df):
    """"By Manoj:- This function reterieves 5 rows of data at a time from the filtered df based on user input from function get_filters().
    This function, prompts user a choice whether they would like to see the data, if user choose yes or y, the data will be shown else will
    break the loop and exit the function."""

    """"By Manoj:- variable i for start row (inclusive) and r for end row (exclusive)"""
    i,r = 0,5
    raw = input("Do you want raw data to be shown? 'yes/no or 'y/n'\n").lower().strip()
    print('-' * 40)
    pd.set_option('display.max_columns',200)

    while True:
        if raw == 'no' or raw == 'n':
            break
        elif raw == 'yes' or raw == 'y':
            """"By Manoj:- From the to rows nos are displayed along with the total no of rows in the df"""
            print("Displaying rows {}-{}/{} total rows.".format(i+1, r ,df.shape[0]))
            print('-' * 40)

            """"By Manoj:- At any given time only 5 rows of data will be shown. and the set will be incremented each time"""
            print(df[i:r])
            raw = input("Do you want raw data to be shown? 'yes/no or 'y/n'.\n").lower().strip()
            i,r = i + 5, r + 5
        else:
            raw = input("\nDo you want raw data to be shown? 'yes/no or 'y/n'.\n").lower().strip()

def is_user_want_to_continue():
    """"By Manoj:- This function is being invoked from main to validate user input for yes or no to continue.
    the loop will be called over and over until user enters a valid data."""

    while True:
        restart = input("\nWould you like to restart? Enter 'yes/no' or 'y/n'.\n").lower().strip()

        """"By Manoj:- An array of valid input are stored, and used to validate against user input"""
        if restart in ['yes','y','no','n']:

            """"By Manoj:- if user opted to exit the program, the True will be returned otherwise False"""
            if restart == 'yes' or restart == 'y':
                return False
                # break
            elif restart == 'no' or restart == 'n':
                return True
                # break
            else:
                continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        """By Manoj:- try catch block is used to catch an unexpected error from the programe and to handle the error."""
        try:
            time_stats(df,city, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            reterieve_all_data(df)
        except IndexError:

            """By Manoj:- If the error is an Index error ( data issue), the program will be returned back to loop"""
            print("Data not available for given input. try changing your input.\n !!! Available data are from 'January' to 'June'")
        except Exception as erx:

            """By Manoj:- If theres other exception, the programe will print the error and return to the loop"""
            print("Need attention to error ", (type(erx).__name__),erx.args)

        """"By Manoj:- Based on the return value from funtion is_user_want_to_continue(), the current while loop will be decided. If the 
         function returns Trie the loop breaks otherwise it continues."""
        if is_user_want_to_continue():
            break



if __name__ == "__main__":
	main()
