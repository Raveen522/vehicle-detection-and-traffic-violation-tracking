#this code detect vehicles are crossing 3 defined lines
#don't change this code. save it for future studies.


import cv2
import math
import numpy as np
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolo_models/yolov8n.pt')

# Function to process each frame
def process_frame(frame, line_positions, cross_percentage, roi_points, min_confidence=20, resize=None):
    if resize:
        frame = cv2.resize(frame, resize)

    # Create a mask for the polygonal ROI
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [np.array(roi_points)], (255, 255, 255))
    masked_frame = cv2.bitwise_and(frame, mask)

    results = model(masked_frame, stream=True)

    # Define colors for the lines and bounding boxes
    line_colors = [(0, 255, 255), (0, 165, 255), (0, 0, 255)]  # Yellow, Orange, Red

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confident_number = math.ceil(box.conf[0] * 100)

            if confident_number > min_confidence:
                # Calculate the crossing threshold based on the percentage, measuring from bottom to top
                crossing_threshold = y2 - (y2 - y1) * (cross_percentage / 100.0)

                # Determine the color of the bounding box and annotation text based on crossing
                bbox_color = (255, 0, 255)  # Initial color (pink)
                annotation_text = ""
                if crossing_threshold > line_positions[0]:
                    bbox_color = line_colors[0]  # Yellow
                    annotation_text = "Vehicle crossed"
                    if crossing_threshold > line_positions[1]:
                        bbox_color = line_colors[1]  # Orange
                        annotation_text = "Violation"
                        if crossing_threshold > line_positions[2]:
                            bbox_color = line_colors[2]  # Red

                # Draw the bounding box with the determined color and reduced thickness
                cv2.rectangle(frame, (x1, y1), (x2, y2), bbox_color, 1)

                # Put the annotation text ("Vehicle crossed" or "Violation") on the frame, if applicable
                text_position = (x1, y2 + 20)  # Adjust '20' to change the vertical distance from the bottom of the box

                if annotation_text:
                    cv2.putText(frame, annotation_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, bbox_color, 1)

    # Draw the lines
    for i, line_y in enumerate(line_positions):
        cv2.line(frame, (0, line_y), (frame.shape[1], line_y), line_colors[i], 1)

    # Draw the polygonal ROI on the frame (optional)
    cv2.polylines(frame, [np.array(roi_points)], True, (255, 255, 255), 1)  # White color for the ROI polygon

    return frame

def main(video_path, model_path, stop_line_y=200, cross_percentage=60, resize=None):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)

    while True:
        success, frame = cap.read()
        if not success:
            break
            
        line_positions = [200, 300, 400]  # Example positions for the three lines
        # Example ROI definition
        roi_points = [(250, 100), (350, 100), (400, 470), (0, 470)]  # List of (x, y) tuples

        # Call the process_frame function with the polygonal ROI
        processed_frame = process_frame(frame, line_positions, cross_percentage=70, roi_points=roi_points, resize=(640, 480))

        cv2.imshow("Vehicle Detection", processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main("footages/videos/input_video_04.mp4", "yolo_models/yolov8n.pt", resize=(640, 480))

# End of the program
