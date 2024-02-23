import cv2
from sensor_based_check import *
from weather_API import *


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

image_path = 'footages/images/blur.png' 

image = cv2.imread(image_path)
if image is None:
    print("Error loading image")
else:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    threshold = 5000
    if fm > threshold:
        print(f"Image is blurry, focus measure: {fm}")
        if sensor_check():
            if get_weather():
                print("Bad weather")
            else:
                print("Local location Error")
        else:
            print("Camera Error")
    else:
        print(f"Image is clear, focus measure: {fm}")