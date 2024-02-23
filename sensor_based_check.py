import RPi.GPIO as GPIO
import time
import Adafruit_DHT

def sensor_check():
    # GPIO pin assignments
    DHT_SENSOR_PIN = 5
    RAIN_SENSOR_PIN = 6

    # DHT sensor setup
    DHT_SENSOR_TYPE = Adafruit_DHT.DHT11

    # Set up GPIO numbering system
    GPIO.setmode(GPIO.BCM)

    # Set up GPIO pin for rain sensor
    GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Set up DHT and get values
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR_TYPE, DHT_SENSOR_PIN)

    if humidity is not None and temperature is not None:
        if not GPIO.input(RAIN_SENSOR_PIN): #Check whether rain sensor shorts(Wet detected)
            if humidity > 55 and temperature < 28:
                return(True)
            else:
                return(False)
        else:
            return(False)
    else:
        print("Failed to read sensor..")
        return(False)

