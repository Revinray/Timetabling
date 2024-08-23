import requests

# Define log levels
LOG_NONE = 0
LOG_ERROR = 1
LOG_DEBUG = 2

def get_module_data(module, LOG_LEVEL=LOG_NONE):
    # Define the URL for the NUSMods API endpoint
    url = f"https://api.nusmods.com/v2/2024-2025/modules/{module}.json"

    if LOG_LEVEL == LOG_DEBUG:
        print(f"Fetching data for module: {module} from URL: {url}")

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        if LOG_LEVEL == LOG_DEBUG:
            print(f"Successfully fetched data for module: {module}")

        # Parse the JSON response
        data = response.json()

        # Extract the timetable information
        timetable = data['semesterData'][0]['timetable']

        return timetable

    else:
        if LOG_LEVEL in [LOG_ERROR, LOG_DEBUG]:
            print(f"Failed to get data for module {module}. Status code: {response.status_code}")
        return None

# Test the function with an example module
# print(get_module_data("IE2110", LOG_LEVEL=LOG_DEBUG))