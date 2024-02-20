#This code detects vehicle are crossing lines and take snapshot of them.
import cv2
import math
import numpy as np
from ultralytics import YOLO
import os
from datetime import datetime

# Function to make label with background color and text color
def draw_label(img, text, pos=(0, 0), text_color=(255, 255, 255), text_color_bg=(0, 0, 0)):
    font=cv2.FONT_HERSHEY_PLAIN
    font_scale = 1
    font_thickness = 1
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (x + text_w + 10, y + text_h + 10), text_color_bg, -1)
    cv2.putText(img, text, (x + 2, y + text_h + font_scale + 2), font, font_scale, text_color, font_thickness)

    return text_size
#---------------------------------------------------------------------

# Function to overlay information on the video frame
def overlay_info(camera_id, signal_light_id, signal_status, road_id, frame):
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    date_string = now.strftime("%d/%m/%Y")

    # Overlay information on the video frame
    draw_label(frame,f"Camera ID: {camera_id}",(400, 20))
    draw_label(frame,f"Signal light ID: {signal_light_id}",(400, 42))
    draw_label(frame,"Signal light status:",(400, 65))
    if (signal_status == "Green"):
        draw_label(frame,signal_status,(568, 65),(0, 230, 0))
    elif(signal_status == "Red"):
        draw_label(frame,signal_status,(568, 65),(0, 0, 230))
    elif(signal_status == "Yellow"):
        draw_label(frame,signal_status,(568, 65),(0, 230, 230))

    draw_label(frame,f"Road: {road_id}",(400, 88))

    draw_label(frame,time_string,(20, 20))
    draw_label(frame,date_string,(20, 42))
#---------------------------------------------------------------------

# Load the YOLO model
model = YOLO('yolo_models/yolov8n.pt')

# Function to process each frame
def process_frame(frame, line_positions, cross_percentage, roi_points, 
                  snapshot_callback, min_confidence=20, resize=None, snapshot_flags=None):
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

                overlay_info(camera_id, signal_light_id, signal_status, road_id, frame)

                if annotation_text:
                    cv2.putText(frame, annotation_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, bbox_color, 1)

    for i, line_y in enumerate(line_positions):
        cv2.line(frame, (0, line_y), (frame.shape[1], line_y), line_colors[i], 1)

    cv2.polylines(frame, [np.array(roi_points)], True, (255, 255, 255), 1)

    return frame, snapshot_flags


def take_snapshot(frame, frame_count, snapshot_dir="snapshots"):
    if not os.path.exists(snapshot_dir):
        os.makedirs(snapshot_dir)
    
    now = datetime.now()
    time_string = now.strftime("%H_%M_%S")
    date_string = now.strftime("%d_%m_%Y")

    snapshot_filename = os.path.join(snapshot_dir, f"violation_on_{date_string}_at_{time_string}_{frame_count}.jpg")
    cv2.imwrite(snapshot_filename, frame)
    print(f"Snapshot saved: {snapshot_filename}")


def main(video_path, stop_line_y=200, cross_percentage=60, resize=None):
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

camera_id = 1
signal_light_id = 123
signal_status = "Red"
road_id = 456

if __name__ == "__main__":
    main("footages/videos/input_video_06.mp4", resize=(640, 480))

