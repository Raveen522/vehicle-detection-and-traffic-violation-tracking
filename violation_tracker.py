import cv2
import cvzone
import math
from datetime import datetime
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolo_models/yolov8n.pt')

# Function to process each frame
def process_frame(frame, line_positions, cross_percentage, min_confidence=20, resize=None):
    if resize:
        frame = cv2.resize(frame, resize)
    results = model(frame, stream=True)

    # Define colors for the lines
    line_colors = [(0, 255, 255), (0, 165, 255), (0, 0, 255)]  # Yellow, Orange, Red
    line_names = ["yellow", "orange", "red"]
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confident_number = math.ceil(box.conf[0] * 100)
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if currentClass in ["car", "truck", "bus", "motorbike"] and confident_number > min_confidence:
                cvzone.putTextRect(frame, f'{currentClass} {confident_number}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
                cvzone.cornerRect(frame, (x1, y1, x2-x1, y2-y1), l=5)

                # Calculate the crossing threshold based on the percentage
                crossing_threshold = y2 - (y2 - y1) * (cross_percentage / 100.0)

                # Check if the crossing threshold of the vehicle's bounding box is beyond the first line
                if crossing_threshold > line_positions[0]:
                    text = "Vehicle crossed" if crossing_threshold <= line_positions[1] else "Violation"
                    text_color = line_colors[0] if crossing_threshold <= line_positions[1] else line_colors[1]
                    cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)

    # Draw the lines
    for i, line_y in enumerate(line_positions):
        cv2.line(frame, (0, line_y), (frame.shape[1], line_y), line_colors[i], 2)

    return frame

def main(video_path, model_path, stop_line_y=200, cross_percentage=60, resize=None):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)

    while True:
        success, frame = cap.read()
        if not success:
            break
            
        line_positions = [200, 300, 400]  # Example positions for the three lines
        processed_frame = process_frame(frame, line_positions, cross_percentage=40, resize=(640, 480))


        cv2.imshow("Vehicle Detection", processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]
    main("footages/videos/input_video_04.mp4", "yolo_models/yolov8n.pt", resize=(640, 480))
