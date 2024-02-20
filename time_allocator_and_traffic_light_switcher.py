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

# Initialize the stop flag to False
stop_flag = False

# This function checks for the user input to stop the program
def check_for_quit():
    global stop_flag
    input("Press 'Q' and Enter to stop the program at any time...")
    stop_flag = True

# Start the thread that listens for quit command
quit_thread = threading.Thread(target=check_for_quit)
quit_thread.daemon = True  # This ensures the thread will close when the main program exits
quit_thread.start()

# Initialize the traffic lights status
traffic_lights = {'T1': 'green', 'T2': 'red', 'T3': 'green', 'T4': 'green', 'T5': 'red', 'T6': 'green'}
green_light_sequence = ['T3', 'T2', 'T5']  # Order in which lights will turn green
iteration = 0

# Main loop for the traffic light controller
while not stop_flag:
    for light in green_light_sequence:
        if stop_flag:
            break

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
        time.sleep(green_time + 5)

# Print a message when the program is stopped
print("Traffic light program terminated.")
