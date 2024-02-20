import random

# Define traffic light constants
GREEN = "GREEN"
YELLOW = "YELLOW"
RED = "RED"

# Define road and traffic light mappings
road_to_traffic_light = {
    "C": "T3",
    "D": "T4",
    "B": "T2",
    "A": "T1",
    "E": "T5",
    "F": "T6",
}

traffic_light_to_road = {
    "T1": "A",
    "T2": "B",
    "T3": "C",
    "T4": "D",
    "T5": "E",
    "T6": "F",
}

# Define the maximum green light and red light durations
MAX_GREEN_LIGHT = 60
MAX_RED_LIGHT = 120
YELLOW_LIGHT_TIME = 5

# Define a dummy vehicle detection function that returns random traffic levels
def dummy_vehicle_detection(traffic_light_id):
    return random.choice(["low", "mid", "high"])

# Define the main program loop
iteration_number = 1
while True:
    # Get the current green, yellow, and red lights
    green_lights = []
    yellow_lights = []
    red_lights = []

    # Determine the first set of green lights (C, D, A)
    green_lights.extend(["T3", "T4", "T1"])
    red_lights.extend(["T2", "T5", "T6"])

    # Run the traffic light cycle for each set of green lights
    for _ in range(3):
        # Display the iteration number, detected traffic levels, and light assignments
        print(f"Iteration No: {iteration_number}")
        for traffic_light in green_lights:
            detected_traffic_level = dummy_vehicle_detection(traffic_light)
            print(f"Detected traffic level of {traffic_light}: {detected_traffic_level}")
        print(f"Green: {', '.join([f'{light} -> {MAX_GREEN_LIGHT}s' for light in green_lights])}")
        print(f"Red: {', '.join([f'{light} -> {MAX_RED_LIGHT}s' for light in red_lights])}")
        print("-" * 40)

        # Simulate the yellow light phase
        for _ in range(YELLOW_LIGHT_TIME):
            # Update the traffic light states
            for traffic_light in green_lights:
                yellow_lights.append(traffic_light)
            for traffic_light in red_lights:
                red_lights.remove(traffic_light)

        # Simulate the red light phase
        for _ in range(MAX_RED_LIGHT - YELLOW_LIGHT_TIME):
            # Update the traffic light states
            for traffic_light in yellow_lights:
                red_lights.append(traffic_light)
            for traffic_light in yellow_lights:
                yellow_lights.remove(traffic_light)

        # Determine the next set of green lights based on detected traffic levels
        next_green_lights = []
        for road in ["C", "B", "E"]:
            traffic_light_id = road_to_traffic_light[road]
            detected_traffic_level = dummy_vehicle_detection(traffic_light_id)
            if detected_traffic_level == "low":
                green_light_duration = 15
            elif detected_traffic_level == "mid":
                green_light_duration = 45
            else:
                green_light_duration = MAX_GREEN_LIGHT
            if traffic_light_id not in red_lights:
                next_green_lights.append(traffic_light_id)

        # Update the green, yellow, and red lights for the next iteration
        green_lights = next_green_lights
        red_lights = [
            traffic_light_id
            for traffic_light_id in traffic_light_to_road.values()
            if traffic_light_id not in green_lights
        ]

        # Check if the user wants to stop the program
        # Add logic to accept user input to stop the program

        iteration_number += 1
