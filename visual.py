import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, to_hex, to_rgb
from urlparse import parse_nusmods_url
from request import get_module_data
import re

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
    'Sectional Teaching': 'SEC',
    'Seminar-Style Module Class': 'SEM'
}

def shorten_lesson_type(lesson_type):
    for full_form, short_form in lesson_type_mapping.items():
        lesson_type = re.sub(rf'{full_form} Type (\d+)', rf'{short_form}\1', lesson_type)
        lesson_type = re.sub(rf'{full_form} Type ([A-Za-z])', rf'{short_form}\1', lesson_type)
        lesson_type = re.sub(rf'\b{full_form}\b', short_form, lesson_type)
    return lesson_type

def luminance(color):
    rgb = to_rgb(color)
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]

def get_contrasting_text_color(hex_color):
    lum = luminance(hex_color)
    return '#000000' if lum > 0.5 else '#FFFFFF'

def visualize_timetable(timetables_info, LOG_LEVEL=LOG_ERROR, flip_axes=False):

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
                    lesson_type_short = shorten_lesson_type(session['lessonType'])

                    # Calculate the font size based on the block size
                    if flip_axes:
                        # block_height = end_index - start_index
                        font_size = 5 # Adjust the multiplier as needed
                    else:
                        block_width = 1  # Each block represents one student
                        font_size = min(8, block_width * 10)  # Adjust the multiplier as needed

                    # Add text to the block only once
                    if flip_axes:
                        text_color = get_contrasting_text_color(to_hex(color))
                        ax.text(start_index, day_index * num_students + student_index - 0.3, 
                                f"{module}\n{lesson_type_short}", ha='left', va='top', fontsize=font_size, 
                                color=text_color)
                    else:
                        text_color = get_contrasting_text_color(to_hex(color))
                        ax.text(day_index * num_students + student_index - 0.3, start_index, 
                                f"{module}\n{lesson_type_short}", ha='left', va='top', fontsize=font_size, 
                                color=text_color)

            # Compare sets to ensure all sessions are plotted
            if sessions_plotted != sessions_in_timetable:
                if LOG_LEVEL in [LOG_ERROR, LOG_DEBUG]:
                    print(f"Error: Sessions plotted {sessions_plotted} do not match sessions in timetable {sessions_in_timetable} for module {module}")
                any_session_not_plotted = True

    # Define a custom colormap based on the extracted colors
    cmap = ListedColormap(['white'] + colors)

    # Create a heatmap for the timetable
    if flip_axes:
        ax.imshow(timetable_array.T, cmap=cmap, aspect='auto', alpha=0.5)
    else:
        ax.imshow(timetable_array, cmap=cmap, aspect='auto', alpha=0.5)

    # Set the labels for the x-axis and y-axis
    if flip_axes:
        ax.set_xticks(np.arange(0, len(timeslots), 4))  # Show every hour (4 * 15 minutes)
        ax.set_yticks(np.arange(len(days)) * num_students + num_students / 2)
        ax.set_xticklabels([f"{timeslot[:2]}:{timeslot[2:]}" for timeslot in timeslots[::4]])  # Show every hour
        ax.set_yticklabels(days)
    else:
        ax.set_xticks(np.arange(len(days)) * num_students + num_students / 2)
        ax.set_yticks(np.arange(0, len(timeslots), 4))  # Show every hour (4 * 15 minutes)
        ax.set_xticklabels(days)
        ax.set_yticklabels([f"{timeslot[:2]}:{timeslot[2:]}" for timeslot in timeslots[::4]])  # Show every hour

    # Remove the y-axis dashes
    ax.tick_params(axis='y', length=0)

    # Remove the x-axis dashes
    ax.tick_params(axis='x', length=0)

    # Draw lines to separate each day
    if flip_axes:
        for day_index in range(1, len(days)):
            plt.axhline(y=day_index * num_students - 0.5, color='black', linewidth=1)
    else:
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

# # Test the function with example timetables
# url1 = "https://nusmods.com/timetable/sem-1/share?CS3243=TUT:06,LEC:1&EG2401A=TUT:509,LEC:2&GEN2001=LEC:1,TUT:E7&LAC3204=LEC:1&LAJ2202=TUT:A2,TUT2:B2,LEC:1&MA3264=LEC:1,TUT:1"
# url2 = "https://nusmods.com/timetable/sem-1/share?CS1231=TUT:03,SEC:1"
# timetable1 = parse_nusmods_url(url1)
# timetable2 = parse_nusmods_url(url2)
# timetables_info = {
#     "Student A": {"timetable": timetable1, "color": "blue"},
#     "Student B": {"timetable": timetable2, "color": "green"}
# }
# fig = visualize_timetable(timetables_info, LOG_LEVEL=LOG_DEBUG, flip_axes=True)