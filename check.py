import json
import os
from datetime import datetime
from request import get_module_data

def load_timetables_info(filename='timetables_info.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def freenow(filename='timetables_info.json'):
    # Load the timetable information
    timetables_info = load_timetables_info(filename)
    
    # Get the current day and time
    now = datetime.now()
    current_day = now.strftime('%A')
    current_time = now.strftime('%H%M')
    
    free_students = []
    
    # Iterate through each student's timetable
    for name, info in timetables_info.items():
        timetable = info['timetable']
        is_free = True
        
        # Check if the current time falls within any of the student's scheduled sessions
        for module, sessions in timetable.items():
            for session in sessions:
                lesson_type, class_no = session.split(':')
                for session_info in get_module_data(module):
                    if (session_info['lessonType'] == lesson_type and 
                        session_info['classNo'] == class_no and 
                        session_info['day'] == current_day and 
                        session_info['startTime'] <= current_time < session_info['endTime']):
                        is_free = False
                        break
                if not is_free:
                    break
            if not is_free:
                break
        
        if is_free:
            free_students.append(name)
    
    return free_students

def freeuntil(filename='timetables_info.json'):
    # Load the timetable information
    timetables_info = load_timetables_info(filename)
    
    # Get the current day and time
    now = datetime.now()
    current_day = now.strftime('%A')
    current_time = now.strftime('%H%M')
    
    free_until = {}
    
    # Iterate through each student's timetable
    for name, info in timetables_info.items():
        timetable = info['timetable']
        is_free = True
        next_session_start = None
        
        # Check if the current time falls within any of the student's scheduled sessions
        for module, sessions in timetable.items():
            for session in sessions:
                lesson_type, class_no = session.split(':')
                for session_info in get_module_data(module):
                    if (session_info['lessonType'] == lesson_type and 
                        session_info['classNo'] == class_no and 
                        session_info['day'] == current_day):
                        if session_info['startTime'] <= current_time < session_info['endTime']:
                            is_free = False
                            break
                        elif session_info['startTime'] > current_time:
                            if next_session_start is None or session_info['startTime'] < next_session_start:
                                next_session_start = session_info['startTime']
                if not is_free:
                    break
            if not is_free:
                break
        
        if is_free:
            free_until[name] = next_session_start if next_session_start else 'End of day'
    
    return free_until

def freewhen(name, filename='timetables_info.json'):
    # Load the timetable information
    timetables_info = load_timetables_info(filename)
    
    # Get the current day and time
    now = datetime.now()
    current_day = now.strftime('%A')
    current_time = now.strftime('%H%M')
    
    # Find the student's timetable
    if name not in timetables_info:
        return f"No timetable found for {name}"
    
    timetable = timetables_info[name]['timetable']
    next_free_time = None
    current_session_end = None
    
    # Iterate through the student's sessions to find the next free time slot
    for module, sessions in timetable.items():
        for session in sessions:
            lesson_type, class_no = session.split(':')
            for session_info in get_module_data(module):
                if (session_info['lessonType'] == lesson_type and 
                    session_info['classNo'] == class_no and 
                    session_info['day'] == current_day):
                    if session_info['startTime'] <= current_time < session_info['endTime']:
                        current_session_end = session_info['endTime']
                    elif session_info['startTime'] > current_time:
                        if next_free_time is None or session_info['startTime'] < next_free_time:
                            next_free_time = session_info['startTime']
    
    if current_session_end:
        return f"Currently busy, free at {current_session_end}"
    return 'now' if next_free_time is None else f"Free now, next busy at {next_free_time}"

# Example usage
if __name__ == "__main__":
    free_students = freenow()
    print("Students who are free now:", free_students)
    
    free_until = freeuntil()
    print("Students who are free and until when:", free_until)
    
    student_name = "JITTO"
    next_free_time = freewhen(student_name)
    print(f"{student_name} is next free at:", next_free_time)