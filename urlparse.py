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
    
    # Iterate over the query parameters
    for module, sessions in query_params.items():
        if LOG_LEVEL == LOG_DEBUG:
            print(f"Module: {module}, Sessions: {sessions}")
        
        # Split the sessions string into a list of sessions
        sessions_list = sessions[0].split(',')
        if LOG_LEVEL == LOG_DEBUG:
            print(f"Sessions List: {sessions_list}")
        
        # Convert LEC to Lecture, TUT to Tutorial, LAB to Laboratory, PLEC to Packaged Lecture, PTUT to Packaged Tutorial
        sessions_list = [session.replace('PLEC', 'Packaged Lecture').replace('PTUT', 'Packaged Tutorial').replace('LEC', 'Lecture').replace('TUT', 'Tutorial').replace('LAB', 'Laboratory').replace('SEC', 'Sectional Teaching') for session in sessions_list]
        if LOG_LEVEL == LOG_DEBUG:
            print(f"Converted Sessions List: {sessions_list}")
        
        # Store the sessions in the timetable dictionary
        timetable[module] = sessions_list
    
    return timetable

# # Test the function with your example URL
# url = "https://nusmods.com/timetable/sem-1/share?CS1231=TUT:03,SEC:1"
# print(parse_nusmods_url(url, LOG_LEVEL=LOG_DEBUG))