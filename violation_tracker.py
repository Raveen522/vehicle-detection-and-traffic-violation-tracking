#This code detects vehicle are crossing lines and take snapshot of them.
  
import cv2
import math
import numpy as np
from ultralytics import YOLO
import os

# Load the YOLO model
model = YOLO('yolo_models/yolov8n.pt')

# Function to process each frame
def process_frame(frame, line_positions, cross_percentage, roi_points, snapshot_callback, min_confidence=20, resize=None, snapshot_flags=None):
    if resize:
        frame = cv2.resize(frame, resize)

    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [np.array(roi_points)], (255, 255, 255))
    masked_frame = cv2.bitwise_and(frame, mask)

    results = model(masked_frame, stream=True)
    line_colors = [(0, 255, 255), (0, 165, 255), (0, 0, 255)]  # Yellow, Orange, Red

    if snapshot_flags is None:
        snapshot_flags = [False, False, False]  # Flags for each line

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confident_number = math.ceil(box.conf[0] * 100)

            if confident_number > min_confidence:
                crossing_threshold = y2 - (y2 - y1) * (cross_percentage / 100.0)
                bbox_color = (255, 0, 255)  # Initial color (pink)
                annotation_text = ""

                for i, line_y in enumerate(line_positions):
                    if crossing_threshold > line_y and not snapshot_flags[i]:
                        snapshot_callback(frame)
                        snapshot_flags[i] = True

                cv2.rectangle(frame, (x1, y1), (x2, y2), bbox_color, 1)
                text_position = (x1, y2 + 20)

                if annotation_text:
                    cv2.putText(frame, annotation_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, bbox_color, 1)

    for i, line_y in enumerate(line_positions):
        cv2.line(frame, (0, line_y), (frame.shape[1], line_y), line_colors[i], 1)

    cv2.polylines(frame, [np.array(roi_points)], True, (255, 255, 255), 1)

    return frame, snapshot_flags


def take_snapshot(frame, frame_count, snapshot_dir="snapshots"):
    if not os.path.exists(snapshot_dir):
        os.makedirs(snapshot_dir)
    
    snapshot_filename = os.path.join(snapshot_dir, f"snapshot_{frame_count}.jpg")
    cv2.imwrite(snapshot_filename, frame)
    print(f"Snapshot saved: {snapshot_filename}")


def main(video_path, model_path, stop_line_y=200, cross_percentage=60, resize=None):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    snapshot_flags = None  # Initialize snapshot flags

    while True:
        success, frame = cap.read()
        if not success:
            break

        line_positions = [200, 300, 400]
        roi_points = [(250, 100), (350, 100), (400, 470), (0, 470)]

        processed_frame, snapshot_flags = process_frame(
            frame, line_positions, cross_percentage, roi_points,
            lambda f: take_snapshot(f, frame_count),
            snapshot_flags=snapshot_flags, resize=(640, 480)
        )

        cv2.imshow("Vehicle Detection", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main("footages/videos/input_video_06.mp4", "yolo_models/yolov8n.pt", resize=(640, 480))

# End of the program
