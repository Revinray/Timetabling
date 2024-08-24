import re
from urllib.parse import urlparse, parse_qs

# Define log levels
LOG_NONE = 0
LOG_ERROR = 1
LOG_DEBUG = 2

def parse_nusmods_url(url, LOG_LEVEL=LOG_NONE):
    # Parse the URL
    parsed_url = urlparse(url)
    if LOG_LEVEL == LOG_DEBUG:
        print(f"Parsed URL: {parsed_url}")
    
    # Extract the query parameters
    query_params = parse_qs(parsed_url.query)
    if LOG_LEVEL == LOG_DEBUG:
        print(f"Query Parameters: {query_params}")
    
    # Initialize an empty dictionary to store the timetable
    timetable = {}
    
    # Define a mapping dictionary for session types
    session_type_mapping = {
        'SEM': 'Seminar-Style Module Class',
        'PLEC': 'Packaged Lecture',
        'PTUT': 'Packaged Tutorial',
        'LEC': 'Lecture',
        'TUT': 'Tutorial',
        'LAB': 'Laboratory',
        'SEC': 'Sectional Teaching'
    }
    
    # Iterate over the query parameters
    for module, sessions in query_params.items():
        if LOG_LEVEL == LOG_DEBUG:
            print(f"Module: {module}, Sessions: {sessions}")
        
        # Split the sessions string into a list of sessions
        sessions_list = sessions[0].split(',')
        if LOG_LEVEL == LOG_DEBUG:
            print(f"Sessions List: {sessions_list}")
        
        # Convert session types using the mapping dictionary and regex
        converted_sessions_list = []
        for session in sessions_list:
            # First, handle patterns like TUT2, TUT_ etc.
            for short_form, full_form in session_type_mapping.items():
                session = re.sub(rf'({short_form})(\d+)', rf'{full_form} Type \2', session)
                session = re.sub(rf'({short_form})([A-Za-z])', rf'{full_form} Type \2', session)
            # Then, handle the normal cases without suffixes
            for short_form, full_form in session_type_mapping.items():
                session = re.sub(rf'\b{short_form}\b', full_form, session)
            converted_sessions_list.append(session)
        
        if LOG_LEVEL == LOG_DEBUG:
            print(f"Converted Sessions List: {converted_sessions_list}")
        
        # Store the sessions in the timetable dictionary
        timetable[module] = converted_sessions_list
    
    return timetable

# # Test the function with your example URL
# url = "https://nusmods.com/timetable/sem-1/share?CS3243=TUT:06,LEC:1&EG2401A=TUT:509,LEC:2&GEN2001=LEC:1,TUT:E7&LAC3204=LEC:1&LAJ2202=TUT:A2,TUT2:B2,LEC:1&MA3264=LEC:1,TUT:1"
# print(parse_nusmods_url(url, LOG_LEVEL=LOG_DEBUG))