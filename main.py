from urlparse import parse_nusmods_url
from visual import visualize_timetable
import matplotlib.pyplot as plt

def main():
    timetables_info = {}
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

    # visualize the timetable
    fig = visualize_timetable(timetables_info)
    # display the timetable
    plt.show()

if __name__ == "__main__":
    main()