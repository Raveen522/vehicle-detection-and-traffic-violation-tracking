import cv2
import numpy as np
from ultralytics import YOLO
from sort import Sort
import time

model = YOLO('yolo_models/yolov8n.pt')
# model = YOLO('yolo_models/yolov8s.pt')
tracker = Sort()

roi_points = [(100, 200), (900, 200), (1150, 700), (100,700)]

def process_frame(frame, model, tracker, roi_points):
    # Apply ROI mask
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [np.array(roi_points)], (255, 255, 255))
    masked_frame = cv2.bitwise_and(frame, mask)

    # Vehicle detection with YOLO
    results = model(masked_frame, stream=True)

    # Prepare data for SORT
    detections = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detections.append([x1, y1, x2, y2])

    # Update SORT tracker
    tracked_objects = tracker.update(np.array(detections))

    # Draw tracked objects and ROI
    tracked_ids = set()
    for obj in tracked_objects:
        cv2.rectangle(frame, (int(obj[0]), int(obj[1])), (int(obj[2]), int(obj[3])), (0, 255, 0), 1)
        vehicle_id = int(obj[4])
        tracked_ids.add(vehicle_id)
        cv2.putText(frame, str(vehicle_id), (int(obj[0]), int(obj[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.polylines(frame, [np.array(roi_points)], True, (255, 0, 0), 2)

    return frame, len(tracked_objects), tracked_ids

def main(video_path):
    cap = cv2.VideoCapture(video_path)
    initial_vehicle_count = 0
    initial_vehicle_ids = set()
    vehicle_ids = set()
    start_time = time.time()
    traffic_jam_checked = False
    traffic_jam_detected = False

    while True:
        success, frame = cap.read()
        if not success:
            break

        processed_frame, current_count, current_ids = process_frame(frame, model, tracker, roi_points)
        elapsed_time = time.time() - start_time

        # Store initial counts and IDs within the first 3 seconds
        if elapsed_time <= 3:
            initial_vehicle_count = current_count
            initial_vehicle_ids = current_ids
        # Check for traffic jam conditions after 10 seconds
        elif elapsed_time > 10 and not traffic_jam_checked:
            vehicle_ids = current_ids
            traffic_jam_checked = True
            reduced_count_threshold = initial_vehicle_count * 0.6  # 40% reduction
            current_common_ids = initial_vehicle_ids.intersection(vehicle_ids)
            if current_count > reduced_count_threshold and len(current_common_ids) >= len(initial_vehicle_ids) * 0.4:
                traffic_jam_detected = True

        # Display initial vehicle count and IDs
        cv2.putText(processed_frame, f"Initial Count: {initial_vehicle_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(processed_frame, f"Initial IDs: {', '.join(map(str, initial_vehicle_ids))}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Display traffic jam status and current vehicle count and IDs
        traffic_jam_text = "Traffic Jam detected" if traffic_jam_detected else "No Traffic Jam detected"
        traffic_jam_text_color = (0, 0, 255) if traffic_jam_detected else (0, 255, 0)
        cv2.putText(processed_frame, traffic_jam_text, (frame.shape[1] - 250, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, traffic_jam_text_color, 2)
        cv2.putText(processed_frame, f"Current Count: {current_count}", (frame.shape[1] - 250, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, traffic_jam_text_color, 2)
        cv2.putText(processed_frame, f"Current IDs: {', '.join(map(str, vehicle_ids))}", (frame.shape[1] - 250, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, traffic_jam_text_color, 2)

        cv2.imshow("Traffic Jam Detection", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main("footages/videos/input_video_01.mp4")
