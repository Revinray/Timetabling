import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
from urlparse import parse_nusmods_url
from request import get_module_data

# Define log levels
LOG_NONE = 0
LOG_ERROR = 1
LOG_DEBUG = 2

# Mapping dictionary to shorten lessonType text
lesson_type_mapping = {
    'Packaged Lecture': 'PLEC',
    'Packaged Tutorial': 'PTUT',
    'Lecture': 'LEC',
    'Tutorial': 'TUT',
    'Laboratory': 'LAB',
    'Sectional Teaching': 'SEC'
}

def visualize_timetable(timetables_info, LOG_LEVEL=LOG_ERROR):

    # Increase the figure size
    fig, ax = plt.subplots(figsize=(10, 8))

    # Increase the font size
    plt.rcParams.update({'font.size': 10})

    # Define the days of the week and time slots
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    timeslots = [f"{hour:02d}{minute:02d}" for hour in range(8, 23) for minute in range(0, 60, 15)]  # 8:00 to 22:45

    # Number of students
    num_students = len(timetables_info)

    # Initialize an empty array for the timetable
    timetable_array = np.zeros((len(timeslots), len(days) * num_students))

    # List to store patches for the legend
    legend_patches = []

    # Extract unique colors from timetables_info
    colors = []
    for student_index, (name, info) in enumerate(timetables_info.items()):
        color = info.get('color', 'blue')
        if color not in colors:
            colors.append(color)
        legend_patches.append(Patch(color=color, label=name))

    # Flag to track if any sessions are not plotted
    any_session_not_plotted = False

    # Iterate over the timetables_info dictionary
    for student_index, (name, info) in enumerate(timetables_info.items()):
        timetable = info['timetable']
        color = info.get('color', 'blue')  # Default color if not specified

        # Iterate over the timetable
        for module, sessions in timetable.items():
            # Sets to track sessions for each module
            sessions_in_timetable = set(sessions)
            sessions_plotted = set()

            # Get the module data
            module_data = get_module_data(module)
            if LOG_LEVEL == LOG_DEBUG:
                print(f"Module: {module}")
                print(f"Module Data: {module_data}")

            # Iterate over the module data
            for session in module_data:
                # Check if the session is in the timetable
                session_key = f"{session['lessonType']}:{session['classNo']}"
                if session_key in sessions:
                    if LOG_LEVEL == LOG_DEBUG:
                        print(f"Session Key: {session_key} found in sessions")

                    # Calculate the start and end indices for the time slots
                    start_time = session['startTime']
                    end_time = session['endTime']

                    if LOG_LEVEL == LOG_DEBUG:
                        print(f"Start Time: {start_time}, End Time: {end_time}")

                    # Ensure start_time and end_time are in timeslots
                    if start_time not in timeslots or end_time not in timeslots:
                        if LOG_LEVEL in [LOG_ERROR, LOG_DEBUG]:
                            print(f"Error: Start time {start_time} or end time {end_time} not in timeslots")
                        any_session_not_plotted = True
                        continue

                    start_index = timeslots.index(start_time)
                    end_index = timeslots.index(end_time)

                    if LOG_LEVEL == LOG_DEBUG:
                        print(f"Start Index: {start_index}, End Index: {end_index}")

                    # Ensure start_index is less than end_index
                    if start_index >= end_index:
                        if LOG_LEVEL in [LOG_ERROR, LOG_DEBUG]:
                            print(f"Error: Start index {start_index} is not less than end index {end_index}")
                        any_session_not_plotted = True
                        continue

                    # Ensure session['day'] is in days
                    if session['day'] not in days:
                        if LOG_LEVEL in [LOG_ERROR, LOG_DEBUG]:
                            print(f"Error: Day {session['day']} not in days")
                        any_session_not_plotted = True
                        continue

                    # Add the module to the timetable array
                    day_index = days.index(session['day'])
                    timetable_array[start_index:end_index, day_index * num_students + student_index] = student_index + 1
                    sessions_plotted.add(session_key)

                    # Shorten the lessonType text
                    lesson_type_short = lesson_type_mapping.get(session['lessonType'], session['lessonType'])

                    # Add text to the block only once
                    ax.text(day_index * num_students + student_index, (start_index + end_index) / 2, 
                            f"{module}\n{lesson_type_short}", ha='center', va='center', fontsize=8, 
                            color='black', bbox=dict(facecolor='white', alpha=0.5))

            # Compare sets to ensure all sessions are plotted
            if sessions_plotted != sessions_in_timetable:
                if LOG_LEVEL in [LOG_ERROR, LOG_DEBUG]:
                    print(f"Error: Sessions plotted {sessions_plotted} do not match sessions in timetable {sessions_in_timetable} for module {module}")
                any_session_not_plotted = True

    # Define a custom colormap based on the extracted colors
    cmap = ListedColormap(['white'] + colors)

    # Create a heatmap for the timetable
    ax.imshow(timetable_array, cmap=cmap, aspect='auto', alpha=0.5)

    # Set the labels for the x-axis and y-axis
    ax.set_xticks(np.arange(len(days)) * num_students + num_students / 2)
    ax.set_yticks(np.arange(0, len(timeslots), 4))  # Show every hour (4 * 15 minutes)
    ax.set_xticklabels(days)
    ax.set_yticklabels([f"{timeslot[:2]}:{timeslot[2:]}" for timeslot in timeslots[::4]])  # Show every hour

    # Remove the y-axis dashes
    ax.tick_params(axis='y', length=0)

    # Remove the x-axis dashes
    ax.tick_params(axis='x', length=0)

    # Draw vertical lines to separate each day
    for day_index in range(1, len(days)):
        plt.axvline(x=day_index * num_students - 0.5, color='black', linewidth=1)

    # Add legend
    ax.legend(handles=legend_patches)

    # Show the plot if log level is LOG_DEBUG
    if LOG_LEVEL == LOG_DEBUG:
        plt.show()

    # Print error message if any sessions are not plotted and LOG_LEVEL is LOG_ERROR
    if any_session_not_plotted and LOG_LEVEL == LOG_ERROR:
        print("Error: Some timetable sessions were not plotted due to invalid times or days.")

    return fig

# Test the function with example timetables
url1 = "https://nusmods.com/timetable/sem-1/share?EE4704=PLEC:01,PTUT:01&IE2110=LEC:1,TUT:3&IE3102=LEC:1"
url2 = "https://nusmods.com/timetable/sem-1/share?CS1231=TUT:03,SEC:1"
timetable1 = parse_nusmods_url(url1)
timetable2 = parse_nusmods_url(url2)
timetables_info = {
    "Student A": {"timetable": timetable1, "color": "blue"},
    "Student B": {"timetable": timetable2, "color": "green"}
}
fig = visualize_timetable(timetables_info, LOG_LEVEL=LOG_DEBUG)