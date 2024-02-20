# vehicle_detection_in_image.py file
import cv2
import numpy as np
from vehicle_detector_v2 import VehicleDetector

# Loading vehicle detector
vd = VehicleDetector()

# Load the image footage
img_footage = cv2.imread("footages/images/input_image_1120x768.png")

# Define the region of interest (ROI) as a polygon
roi_points = np.array([[350, 300], [630, 300], [1000, 750], [50, 750]], np.int32)
roi_points = roi_points.reshape((-1, 1, 2))

# Create an empty mask of the same size as the image
mask = np.zeros_like(img_footage)

# Fill the ROI polygon with white color (255) on the mask
cv2.fillPoly(mask, [roi_points], (255, 255, 255))

# Apply the mask to the image to extract the ROI
roi_img = cv2.bitwise_and(img_footage, mask)

# Draw lines to outline the ROI
cv2.polylines(img_footage, [roi_points], isClosed=True, color=(0, 255, 0), thickness=2)

# Get the coordinates and labels of detected vehicles within the ROI
vehicle_results = vd.detect_vehicles_with_labels(roi_img)

# Count the vehicles by category
vehicle_category_count = {'Car': 0, 'Motorbike': 0, 'Bus': 0, 'Truck': 0, 'Train': 0, 'Van': 0, 'Three-Wheeler': 0}

# Draw rectangles and labels for detected vehicles within the ROI
for result in vehicle_results:
    category = result[4]
    vehicle_category_count[category] += 1
    vd.draw_labeled_box(img_footage, result[:4], category, bg_color=(255, 255, 255), text_color=(0, 0, 0))

# Put vehicle count by categories
cv2.putText(img_footage, f"Car Count: {vehicle_category_count['Car']}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (31, 31, 31), 2)
cv2.putText(img_footage, f"Motorbike Count: {vehicle_category_count['Motorbike']}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (31, 31, 31), 2)
cv2.putText(img_footage, f"Bus Count: {vehicle_category_count['Bus']}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (31, 31, 31), 2)
cv2.putText(img_footage, f"Truck Count: {vehicle_category_count['Truck']}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (31, 31, 31), 2)
cv2.putText(img_footage, f"Van Count: {vehicle_category_count['Van']}", (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (31, 31, 31), 2)
cv2.putText(img_footage, f"Three-Wheeler Count: {vehicle_category_count['Three-Wheeler']}", (20, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (31, 31, 31), 2)
cv2.putText(img_footage, f"Total Count: {sum(vehicle_category_count.values())}", (20, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (31, 31, 31), 2)

# Show the output
cv2.imshow("Vehicles", img_footage)
cv2.waitKey(0)
