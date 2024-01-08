import cv2
import numpy as np
from ultralytics import YOLO
from sort import Sort  # Make sure to have the SORT algorithm implementation
import time

# Initialize the YOLO model
model = YOLO('yolo_models/yolov8n.pt')

# Initialize SORT tracker
tracker = Sort() 

# Define the ROI coordinates
roi_points = np.array([[350, 200], [700, 200], [700, 700], [10, 700]])

# Function to process each frame
def process_frame(frame):
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [roi_points], (255, 255, 255))
    masked_frame = cv2.bitwise_and(frame, mask)

    results = model(masked_frame, stream=True)

    # Extract bounding boxes and confidences
    detections = []
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            detections.append([x1, y1, x2, y2, conf])

    # Update SORT tracker with current detections
    tracked_objects = tracker.update(np.array(detections))

    # Draw tracked objects and their IDs
    for obj in tracked_objects:
        x1, y1, x2, y2, obj_id = map(int, obj)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, str(obj_id), (x1, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.polylines(frame, [roi_points], isClosed=True, color=(0, 255, 0), thickness=2)
    
    return frame, len(tracked_objects)

# Main function to process the video
def main(video_path):
    cap = cv2.VideoCapture(video_path)
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, vehicle_count = process_frame(frame)

        # Display vehicle count every 3 seconds
        if time.time() - start_time > 3:
            print(f"Vehicle count: {vehicle_count}")
            start_time = time.time()

        cv2.imshow("Vehicle Tracking", processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main("footages/videos/input_video_04.mp4")