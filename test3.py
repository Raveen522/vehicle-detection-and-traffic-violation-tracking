import cv2
import numpy as np
from vehicle_detector import VehicleDetector

# Initialize vehicle detector
vd = VehicleDetector()

# Load the image
img_footage = cv2.imread("footages/images/input_image_low_traffic.png") # low traffic
# img_footage = cv2.imread("footages/images/input_image_mid_traffic.png") # mid traffic
# img_footage = cv2.imread("footages/images/input_image_high_traffic.png") # high traffic

# Define the three ROIs
roi1_points = np.array([[200, 480], [900, 480], [1100, 750], [50, 750]], np.int32)
roi2_points = np.array([[300, 345], [720, 345], [900, 475], [200, 475]], np.int32)
roi3_points = np.array([[400, 200], [550, 200], [720, 340], [300, 340]], np.int32)

def process_roi(roi_points, color, img_footage):
    mask = np.zeros_like(img_footage)
    cv2.fillPoly(mask, [roi_points], (255, 255, 255))
    roi_img = cv2.bitwise_and(img_footage, mask)
    cv2.polylines(img_footage, [roi_points], isClosed=True, color=color, thickness=2)

    vehicle_boxes = vd.detect_vehicles(roi_img)
    vehicle_count = len(vehicle_boxes)
    text = "Vehicles Detected: " + str(vehicle_count) if vehicle_count > 0 else "No Vehicles"

    # Draw bounding boxes and text inside the ROI
    for box in vehicle_boxes:
        x, y, w, h = box
        cv2.rectangle(img_footage, (x, y), (x + w, y + h), color, 2)

    text_position = roi_points[0][0] + [20, -10]  # Adjust position as needed
    cv2.putText(img_footage, text, tuple(text_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (31, 31, 31), 2)

    return vehicle_count

# Process each ROI and get vehicle counts
vehicle_count1 = process_roi(roi1_points, (0, 255, 0), img_footage)  # Green
vehicle_count2 = process_roi(roi2_points, (0, 165, 255), img_footage)  # Orange
vehicle_count3 = process_roi(roi3_points, (0, 0, 255), img_footage)  # Red

# Determine traffic level
if vehicle_count3 > 0:
    traffic_status = "High Traffic"
elif vehicle_count2 > 0:
    traffic_status = "Mid Traffic"
elif vehicle_count1 > 0:
    traffic_status = "Low Traffic"
else:
    traffic_status = "No Traffic"

# Display traffic status
cv2.putText(img_footage, traffic_status, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (31, 31, 31), 2)

# Show the output
cv2.imshow("Vehicles", img_footage)
cv2.waitKey(0)
