import time
import pandas as pd


CITY_DATA = {
    "chicago": "chicago.csv",
    "new york": "new_york_city.csv",
    "washington": "washington.csv"
}

MONTHS = {
    "january": 1, "february": 2, "march": 3,
    "april": 4, "may": 5, "june": 6
}

DAYS = ["sunday", "monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday"]

SEPARATOR = "-" * 40

def get_choice(prompt, valid_options):
    while True:
        choice = input(prompt).lower()
        if choice in valid_options:
            return choice
        print("Invalid input, please try again.")


def get_filters():
    print("Hello! Let's explore some US bikeshare data!")

    city = get_choice(
        "Choose city (Chicago, New York, Washington):\n",
        CITY_DATA.keys()
    )

    filter_type = get_choice(
        "Filter by month, day, or none?\n",
        ["month", "day", "none"]
    )

    month = day = "all"

    if filter_type == "month":
        month = get_choice(
            "Enter month (January–June) or 'all':\n",
            list(MONTHS.keys()) + ["all"]
        )

    elif filter_type == "day":
        day = get_choice(
            "Enter day (Sunday–Saturday) or 'all':\n",
            DAYS + ["all"]
        )

    print(SEPARATOR)
    return city, month, day

def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])

    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()

    if month != "all":
        df = df[df["month"] == MONTHS[month]]

    if day != "all":
        df = df[df["day_of_week"].str.lower() == day]

    return df

def print_completion(start):
    print(f"\nCompleted in {time.time() - start:.2f} seconds")
    print(SEPARATOR)


def time_stats(df):
    print("\nMost Popular Times of Travel\n")
    start = time.time()

    print("Most Common Month:", df["month"].mode()[0])
    print("Most Common Day:", df["day_of_week"].mode()[0])
    print("Most Common Hour:", df["Start Time"].dt.hour.mode()[0])

    print_completion(start)


def station_stats(df):
    print("\nMost Popular Stations and Trips\n")
    start = time.time()

    print("Start Station:", df["Start Station"].mode()[0])
    print("End Station:", df["End Station"].mode()[0])

    trip = (df["Start Station"] + " → " + df["End Station"]).mode()[0]
    print("Most Common Trip:", trip)

    print_completion(start)


def trip_duration_stats(df):
    print("\nTrip Duration Stats\n")
    start = time.time()

    total = df["Trip Duration"].sum()
    avg = df["Trip Duration"].mean()

    print("Total Travel Time (sec):", total)
    print("Average Travel Time (sec):", round(avg))

    print_completion(start)


def user_stats(df, city):
    print("\nUser Stats\n")
    start = time.time()

    print("User Types:\n", df["User Type"].value_counts())

    if "Gender" in df:
        print("\nGender Counts:\n", df["Gender"].value_counts())

    if "Birth Year" in df:
        print("\nOldest Birth Year:", int(df["Birth Year"].min()))
        print("Youngest Birth Year:", int(df["Birth Year"].max()))
        print("Most Common Birth Year:", int(df["Birth Year"].mode()[0]))
    print_completion(start)



def show_raw_data(df):
    i = 0
    while True:
        show = input("Show 5 rows of raw data? (yes/no): ").lower()
        if show != "yes":
            break
        print(df.iloc[i:i+5])
        i += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_data(df)

        if input("Restart? (yes/no): ").lower() != "yes":
            break

if __name__ == "__main__":
    main()
