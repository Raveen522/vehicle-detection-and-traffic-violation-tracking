import RPi.GPIO as GPIO
import time

# Define GPIO pins for the traffic lights based on Raspberry Pi GPIO numbering
# T1
greenT1, yellowT1, redT1 = 2, 3, 4  # Arduino pins 2, 3, 4
# T2
greenT2, yellowT2, redT2 = 17, 27, 22  # Arduino pins 5, 6, 7
# T3
greenT3, yellowT3, redT3 = 10, 9, 11  # Arduino pins 8, 9, 10
# T4
greenT4, yellowT4, redT4 = 5, 6, 13  # Arduino pins 11, 12, 13
# T5 (using GPIO pins as analog pin counterparts)
greenT5, yellowT5, redT5 = 19, 26, 21  # Arduino pins A0, A1, A2
# T6 (using GPIO pins as analog pin counterparts)
greenT6, yellowT6, redT6 = 20, 16, 12  # Arduino pins A3, A4, A5

# Timing for the lights (in seconds)
greenTime = 15
yellowTime = 5
redTime = greenTime + yellowTime

# Setup GPIO
GPIO.setmode(GPIO.BCM)
all_lights = [greenT1, yellowT1, redT1, greenT2, yellowT2, redT2,
              greenT3, yellowT3, redT3, greenT4, yellowT4, redT4,
              greenT5, yellowT5, redT5, greenT6, yellowT6, redT6]

for light in all_lights:
    GPIO.setup(light, GPIO.OUT)

def allRed():
    for light in all_lights:
        GPIO.output(light, GPIO.LOW)
    for red in [redT1, redT2, redT3, redT4, redT5, redT6]:
        GPIO.output(red, GPIO.HIGH)

def control_lights():
    allRed()
    time.sleep(2)  # Initial delay before starting the cycle

    while True:
        # Pattern 1: T1, T3, T4 are green; T2, T5, T6 are red
        allRed()  # Ensure all are red before changing to green
        for light in [greenT1, greenT3, greenT4]:
            GPIO.output(light, GPIO.HIGH)
        time.sleep(greenTime)
        
        # Transition to yellow for T1, T3, T4
        for light in [greenT1, greenT3, greenT4]:
            GPIO.output(light, GPIO.LOW)
        for light in [yellowT1, yellowT3, yellowT4]:
            GPIO.output(light, GPIO.HIGH)
        time.sleep(yellowTime)
        
        # Pattern 2: T2, T5, T6 are green; T1, T3, T4 are red
        allRed()
        for light in [greenT2, greenT5, greenT6]:
            GPIO.output(light, GPIO.HIGH)
        time.sleep(greenTime)
        
        # Transition to yellow for T2, T5, T6
        for light in [greenT2, greenT5, greenT6]:
            GPIO.output(light, GPIO.LOW)
        for light in [yellowT2, yellowT5, yellowT6]:
            GPIO.output(light, GPIO.HIGH)
        time.sleep(yellowTime)

        # Additional patterns can be added following the same structure

try:
    control_lights()
except KeyboardInterrupt:
    GPIO.cleanup()
