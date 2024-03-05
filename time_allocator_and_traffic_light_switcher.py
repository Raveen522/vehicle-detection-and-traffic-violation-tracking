import random
import time
from load_settings import*

# Dummy function to simulate vehicle detection
def dummy_vehicle_detection():
    return random.choice(['low', 'mid', 'high'])

# Function to calculate green light time based on traffic level
Low_lvl_time, Mid_lvl_time, High_lvl_time, Yellow_time  = lvl_timing()

def calculate_green_time(traffic_level):
    if traffic_level == 'low':
        return Low_lvl_time
    elif traffic_level == 'mid':
        return Mid_lvl_time
    elif traffic_level == 'high':
        return High_lvl_time

# Initialize the traffic lights status
traffic_lights = {'T1': 'green', 'T2': 'red', 'T3': 'green', 'T4': 'green', 'T5': 'red', 'T6': 'green'}
green_light_sequence = ['T3', 'T2', 'T5']  # Order in which lights will turn green
iteration = 0

# Main loop for the traffic light controller
while True:
    for light in green_light_sequence:

        # Call dummy vehicle detection and calculate green time
        detected_traffic_level = dummy_vehicle_detection()
        green_time = calculate_green_time(detected_traffic_level)

        # Set the green light and calculate red light times for other lights
        red_time = 120 - green_time

        # Display the output
        iteration += 1
        print(f"Iteration No: {iteration}")
        print(f"Detected traffic level of {light}: {detected_traffic_level}")
        print(f"Green: {light} for {green_time}s")
        for tl in traffic_lights.keys():
            if tl != light and tl not in ['T1', 'T4', 'T6']:  # T1, T4, and T6 are always green
                print(f"Red: {tl} -> {red_time}s", end=' | ')
        print("\n" + "-" * 37)

        # Simulate the green light duration and the yellow light duration
        time.sleep(green_time + Yellow_time)

# Print a message when the program is stopped
print("Traffic light program terminated.")
