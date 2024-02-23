import random
import threading
import time

# Dummy function to simulate vehicle detection
def dummy_vehicle_detection():
    return random.choice(['low', 'mid', 'high'])

# Function to calculate green light time based on traffic level
def calculate_green_time(traffic_level):
    if traffic_level == 'low':
        return 15
    elif traffic_level == 'mid':
        return 45
    elif traffic_level == 'high':
        return 60

# Initialize the traffic lights status
traffic_lights = {'T1': 'green', 'T2': 'red', 'T3': 'green', 'T4': 'green', 'T5': 'red', 'T6': 'red'}
green_light_sequence = [ {'T1', 'T2', 'T6'}, {'T4', 'T5', 'T6'}, {'T3', 'T4', 'T1'}]  # Order in which lights will turn green
iteration = 1

print("Iteration No: 1")
print("Detected traffic level of T3, T4, T1: high")
print("Green: {'T3', 'T4', 'T1'} for 60s")
print("Red: T2 -> 60s | T5 -> 60s | T6 -> 60s")
print("\n" + "-" * 37)
time.sleep(60)

# Main loop for the traffic light controller
while True:
    for light in green_light_sequence:
        # Call dummy vehicle detection and calculate green time
        detected_traffic_level = dummy_vehicle_detection()
        green_time = calculate_green_time(detected_traffic_level)

        # Set the green light and calculate red light times for other lights
        red_time = green_time

        # Display the output
        iteration += 1
        print(f"Iteration No: {iteration}")
        print(f"Detected traffic level of {light}: {detected_traffic_level}")
        print(f"Green: {light} for {green_time}s")
        for tl in traffic_lights.keys():
            if tl != light and tl not in light:  # T1, T4, and T6 are always green
                print(f"Red: {tl} -> {red_time}s", end=' | ')
        print("\n" + "-" * 37)

        # Simulate the green light duration and the yellow light duration
        time.sleep(green_time + 5)

