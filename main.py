from urlparse import parse_nusmods_url
from visual import visualize_timetable
import matplotlib.pyplot as plt
import json
import os

def save_timetables_info(timetables_info, filename='timetables_info.json'):
    with open(filename, 'w') as f:
        json.dump(timetables_info, f)

def load_timetables_info(filename='timetables_info.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def main(args=[]):
    timetables_info = {}
    if not args:
        timetables_info = load_timetables_info()
        if not timetables_info:
            print("No saved timetables found. Please enter the timetables manually")
            while True:
                # request user input
                url = input("Enter NUSMods URL (or 'done' to finish): ")
                if url.lower() == 'done':
                    break
                name = input("Enter student name: ")
                color = input("Enter color for the timetable: ")
                # parse the URL
                timetable = parse_nusmods_url(url)
                # add to timetables_info
                timetables_info[name] = {"timetable": timetable, "color": color}
            # Save the timetables_info to a file
            save_timetables_info(timetables_info)
    else:
        num_ppl = int(args[0])
        info = args[1]
        for person in range(num_ppl):
            name, url, color = info[person]
            timetable = parse_nusmods_url(url)
            timetables_info[name] = {"timetable": timetable, "color": color}

    # visualize the timetable
    fig = visualize_timetable(timetables_info, flip_axes=True)
    # display the timetable
    plt.show()

if __name__ == "__main__":
    main()