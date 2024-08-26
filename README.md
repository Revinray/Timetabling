# Timetable Visualizer with Friends

This project allows you to visualize timetables from NUSMods URLs (optionally with friends). Follow the instructions below to use the `main.py` script.

## Prerequisites

Ensure you have the following Python packages installed:
- `matplotlib`
- `numpy`
- `requests`

You can install them using pip:
```sh
pip install matplotlib numpy requests
```

## Manual Usage
1. Run the Script: Execute the main.py script using Python:
```sh
python main.py
```
2. Enter NUSMods URL: When prompted, enter the NUSMods URL for the timetable you want to visualize. If you have multiple timetables to visualize, enter each URL one by one.

3. Enter Student Name: After entering the URL, provide a name for the student whose timetable you are adding.

4. Enter Color: Specify a color for the timetable. This color will be used to differentiate this student's timetable from others.

5. Finish Input: If you have finished entering all timetables, type done when prompted for the NUSMods URL.

6. Visualize Timetable: The script will generate a visual representation of the timetables and display it using matplotlib.

### Example
```sh
Enter NUSMods URL (or 'done' to finish): https://nusmods.com/timetable/sem-1/share?CS1231=TUT:03,SEC:1
Enter student name: Student A
Enter color for the timetable: blue
Enter NUSMods URL (or 'done' to finish): https://nusmods.com/timetable/sem-1/share?EE4704=PLEC:01,PTUT:01
Enter student name: Student B
Enter color for the timetable: green
Enter NUSMods URL (or 'done' to finish): done
```
After entering the above information, a timetable visualization will be displayed with Student A's timetable in blue and Student B's timetable in green. 

## JSON Usage
You can also store the timetable information in a JSON file and load it when running the script. This allows you to reuse the timetable data without re-entering it each time.

Save Timetable Information: After entering the timetable information, the script will save it to a file named timetables_info.json.

Load Timetable Information: If the timetables_info.json file exists, the script will automatically load the timetable information from this file when no arguments are provided.

### Example JSON file
```JSON
{
    "STUDENT A": {
      "timetable": {
        "CLC3307": ["Seminar-Style Module Class:1"],
        "EE4704": ["Packaged Lecture:01", "Packaged Tutorial:01"],
        "ESP3903": ["Laboratory:1", "Lecture:1"],
        "GEX1015": ["Lecture:1", "Tutorial:W3"],
        "PC3242": ["Tutorial:1", "Lecture:1"],
        "PC3247": ["Lecture:1"]
      },
      "color": "lime"
    },
    "STUDENT B": {
      "timetable": {
        "ESP2106": ["Lecture:1", "Tutorial:1"],
        "ESP3201": ["Laboratory:1", "Lecture:1", "Tutorial:1"],
        "LAJ2202": ["Tutorial:A2", "Tutorial Type 2:B2", "Lecture:1"],
        "PC2130": ["Lecture:1"]
      },
      "color": "crimson"
    }
}
```


## Running with Arguments
You can also run the script with arguments to specify the number of people and their timetable information directly:
```sh
python main.py 2 "Student A,https://nusmods.com/timetable/sem-1/share?CS1231=TUT:03,SEC:1,blue" "Student B,https://nusmods.com/timetable/sem-1/share?EE4704=PLEC:01,PTUT:01,green"
```
This will directly visualize the timetables for Student A and Student B without prompting for input.

#### Note
Ensure that the timetables_info.json file is in the same directory as main.py for the script to load the timetable information automatically.
If you want to start fresh and ignore the saved JSON file, you can delete the timetables_info.json file before running the script.

