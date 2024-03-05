import ast

# Define a function to convert string representations of numbers, tuples, and lists to actual Python data types
def convert_to_data_type(s):
    try:
        # Try to interpret as an integer
        return int(s)
    except ValueError:
        try:
            # Try to interpret as a tuple
            return tuple(map(int, s.strip('()').split(', ')))
        except ValueError:
            try:
                # Try to interpret as a list of tuples
                return [tuple(map(int, i.strip('()'))) for i in s.strip('][').split('), (')]
            except ValueError:
                try:
                    # Try to interpret as a list of integers
                    return list(map(int, s.strip('][').split(', ')))
                except ValueError:
                    # If all fails, return the string itself
                    return s.strip('"')

# Initialize all variables to None
variables = {
    "Updated": None,
    "Junction": None,
    "Junction_ID": None,
    "Last_violation_upload_time": None,
    "Last_violation_upload_date": None,
    "Green": None,
    "Yellow": None,
    "Red": None,
    "Low_lvl_time": None,
    "Mid_lvl_time": None,
    "High_lvl_time": None,
    "Detection_ROI": None,
    "ROI_1": None,
    "ROI_2": None,
    "ROI_3": None,
    "line_positions": None
}

# Path to the settings file
file_path = 'Settings.conf'
# file_path = 'C:/wamp64/www/ITLS/Settings.txt'

def read_file():
    # Read the file and parse the data
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into key-value pairs
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                # Assign the converted value to the corresponding key in the dictionary
                if key in variables:
                    variables[key] = convert_to_data_type(value)

# Assign values from dictionary to individual variables
Updated = variables["Updated"]
Junction = variables["Junction"]
Junction_ID = variables["Junction_ID"]
Last_violation_upload_time = variables["Last_violation_upload_time"]
Last_violation_upload_date = variables["Last_violation_upload_date"]
Green = variables["Green"]
Yellow = variables["Yellow"]
Red = variables["Red"]


def level_ROI_cords():
    read_file()
    ROI_1 = ast.literal_eval(variables["ROI_1"])
    ROI_2 = ast.literal_eval(variables["ROI_2"])
    ROI_3 = ast.literal_eval(variables["ROI_3"])
    return ROI_1, ROI_2, ROI_3 

def violation_cords():
    read_file()
    Detection_ROI = ast.literal_eval(variables["Detection_ROI"])
    line_positions = variables["line_positions"]
    return Detection_ROI,line_positions

def lvl_timing():
    read_file()
    Low_lvl_time = variables["Low_lvl_time"]
    Mid_lvl_time = variables["Mid_lvl_time"]
    High_lvl_time = variables["High_lvl_time"]
    Yellow = variables["Yellow"]
    return Low_lvl_time, Mid_lvl_time, High_lvl_time, Yellow
