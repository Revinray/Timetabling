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

## Usage
1. Run the Script: Execute the main.py script using Python:
```sh
python main.py
```
2. Enter NUSMods URL: When prompted, enter the NUSMods URL for the timetable you want to visualize. If you have multiple timetables to visualize, enter each URL one by one.

3. Enter Student Name: After entering the URL, provide a name for the student whose timetable you are adding.

4. Enter Color: Specify a color for the timetable. This color will be used to differentiate this student's timetable from others.

5. Finish Input: If you have finished entering all timetables, type done when prompted for the NUSMods URL.

6. Visualize Timetable: The script will generate a visual representation of the timetables and display it using matplotlib.

## Example
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