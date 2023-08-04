import random
import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def generate_schedule():
    persons = ['Mom', 'Dad', 'Daughter', 'Son']
    weekdays = list(calendar.day_name)
    random.shuffle(weekdays)  # the weekdays

    schedule = {}
    for i, person in enumerate(persons):
        weekday = weekdays[i % len(weekdays)]
        schedule[person] = {'weekday': weekday}

    return schedule

def generate_rooms():
    rooms = ['kitchen', 'bathroom', 'living room', 'bedroom', 'staircase', 'small bathroom', 'corridor', 'garage', 'basement']
    random.shuffle(rooms)
    return rooms

def assign_rooms(schedule, rooms):
    for person in schedule:
        if 'rooms' not in schedule[person]:
            schedule[person]['rooms'] = random.sample(rooms, random.randint(1, len(rooms)))

        # Calculate cleaning dates
        schedule[person]['cleaning_dates'] = calculate_cleaning_dates(person, schedule, 2, datetime.now().date())

def calculate_cleaning_dates(name, schedule, num_months, first_cleaning_date):
    try:
        data = schedule[name]
        weekday = data['weekday']
        assigned_rooms = data['rooms']

        # Map weekdays to corresponding indices
        weekday_map = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6
        }

        # Calculate the index of the weekday 
        weekday_index = weekday_map.get(weekday)

        # Find the nearest date 
        today = datetime.now().date()
        days_to_count = (weekday_index - first_cleaning_date.weekday()) % 7
        first_date = first_cleaning_date + timedelta(days=days_to_count)

        # Calculate cleaning dates for the next num_months, every 5 days
        dates_and_weekdays = []
        for _ in range(num_months):
            for room in assigned_rooms:
                random_weekday = random.choice(list(weekday_map.keys()))
                weekday_index = weekday_map.get(random_weekday)

                # Calculate the date corresponding to the randomly chosen weekday
                date = first_date + timedelta(weeks=2)
                while date.weekday() != weekday_index:
                    date += timedelta(days=5)

                dates_and_weekdays.append((date, random_weekday))
                first_date = first_date + timedelta(weeks=2)

        return dates_and_weekdays
    except KeyError:
        print(f'Person with the name {name} not found in the schedule.')
        return []

def main():
    print("Who cleans when in the house?:")
    schedule = generate_schedule()
    rooms = generate_rooms()
    assign_rooms(schedule, rooms)
    
    cleaning_dates = {}  # Dictionary to store the calculated cleaning dates for each person

    while True:
        command = input("Enter command:\n1. 'when' - to display upcoming cleaning dates for a person.\n2. 'where' - to display assigned rooms for a person.\n3. 'q' - to quit.\n")

        if command.lower() == 'q':
            break
        elif command.lower() == 'when' or command.lower() == 'where':
            name = input("Enter the person's name to display their information: ")
            name = name.lower().capitalize()

            try:
                data = schedule[name]
                assigned_rooms = data['rooms']

                # Check if calculated cleaning dates for the person are already available 
                if name not in cleaning_dates:
                    # If the dates are not available, calculate them and store in the dictionary
                    cleaning_dates[name] = calculate_cleaning_dates(name, schedule, 2, datetime.now().date())

                if command.lower() == 'when':
                    # Display the cleaning dates from the calculations stored in the dictionary
                    if cleaning_dates[name]:
                        print(f"Upcoming cleaning dates for {name}:")
                        for date, weekday in cleaning_dates[name]:
                            print(date.strftime('%Y-%m-%d') + " - " + weekday)
                    else:
                        print(f"No schedule found for the given person.")
                elif command.lower() == 'where':
                    if assigned_rooms:
                        print(f"{name} cleans:")
                        for i in range(len(assigned_rooms)):
                            date = cleaning_dates[name][i][0]
                            weekday = cleaning_dates[name][i][1]
                            print(f"{assigned_rooms[i]} - {date.strftime('%Y-%m-%d')} ({weekday})")
                    else:
                        print(f"No assigned rooms for {name}.")
            except KeyError:
                print(f'Person with the name {name} not found in the schedule.')
        else:
            print("Unknown command. Enter 'when', 'where', or 'q'.")

if __name__ == "__main__":
    main()
