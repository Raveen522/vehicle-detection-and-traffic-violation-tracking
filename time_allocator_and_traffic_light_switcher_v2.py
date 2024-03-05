import random
import time
import RPi.GPIO as GPIO
from load_settings import*

GPIO.setmode(GPIO.BCM)

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

    
def yellow_selector(greens, reds):
    for item in greens:
        if traffic_lights.get(item) != "green":
            yellow_light_list.append(item)

    for item in reds:
        if traffic_lights.get(item) != "red":
            yellow_light_list.append(item)
    print(yellow_light_list)


#GPIO pins for traffic light units
traffic_light_GPIO = {"T1":[0,5,6], "T2":[13,19,26], "T3":[2,3,4], "T4":[16,20,21], "T5":[12,1,7], "T6":[23,24,25]}

def green_GPIO_select(green_lights):
    for gl in green_lights:
        for tl in traffic_light_GPIO.keys():
            if tl == gl:
                on_traffic_light(traffic_light_GPIO[tl][0], traffic_light_GPIO[tl][1], traffic_light_GPIO[tl][2], "GPIO.HIGH", "GPIO.LOW", "GPIO.LOW")

def yellow_GPIO_select(yellow_lights):
    for light in yellow_lights:
        for tl in traffic_light_GPIO.keys():
            if tl == light:
                on_traffic_light(traffic_light_GPIO[tl][0], traffic_light_GPIO[tl][1], traffic_light_GPIO[tl][2], "GPIO.LOW", "GPIO.HIGH", "GPIO.LOW")

def red_GPIO_select(red_lights):
    for rl in red_lights:
        for tl in traffic_light_GPIO.keys():
            if tl == rl:
                on_traffic_light(traffic_light_GPIO[tl][0], traffic_light_GPIO[tl][1], traffic_light_GPIO[tl][2], "GPIO.LOW", "GPIO.LOW", "GPIO.HIGH")
    

def on_traffic_light(Green_pin, Yellow_pin, Red_pin, green_status, yellow_status, red_status):
    GPIO.setup(Green_pin, GPIO.OUT)
    GPIO.setup(Yellow_pin, GPIO.OUT)
    GPIO.setup(Red_pin, GPIO.OUT)

    GPIO.output(Green_pin, green_status)
    GPIO.output(Yellow_pin, yellow_status)
    GPIO.output(Red_pin, red_status)

# Initialize the traffic lights status
traffic_lights = {'T1': 'green', 'T2': 'red', 'T3': 'green', 'T4': 'green', 'T5': 'red', 'T6': 'red'}
green_light_sequence = [ {'T1', 'T2', 'T6'}, {'T4', 'T5', 'T6'}, {'T3', 'T4', 'T1'}]  # Order in which lights will turn green
default_yellow_delay = Yellow_time
green_light_list = []
yellow_light_list = []
red_light_list = []
iteration = 0

# Main loop for the traffic light controller
try:
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
            for rtl in traffic_lights.keys():
                if rtl != light and rtl not in light:  
                    print(f"Red: {rtl} -> {red_time}s", end=' | ')
                    red_light_list.append(rtl)
            for gtl in light:
                green_light_list.append(gtl)

            
            yellow_light_list.clear() # Clean the yellow list
            yellow_selector(green_light_list, red_light_list) # Define new yellow list
            yellow_GPIO_select(yellow_light_list) # Turn on yellow
            time.sleep(default_yellow_delay)  # Yellow waiting

            # Update next traffic light status
            for status_ligt in green_light_list:
                traffic_lights[status_ligt] = "green"
            for status_ligt in red_light_list:
                traffic_lights[status_ligt] = "red"


            green_GPIO_select(green_light_list) # Turn on Green
            red_GPIO_select(red_light_list) # Turn on Red

            green_light_list.clear() # Clean previous green list
            red_light_list.clear() # Clean previous red list
            print("\n" + "-" * 37)

            # Simulate the green light duration
            time.sleep(green_time - default_yellow_delay)
finally:
    GPIO.cleanup()