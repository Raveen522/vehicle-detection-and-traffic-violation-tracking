# vehicle_detector.py file
import cv2
import numpy as np

class VehicleDetector:
    def __init__(self):
        # Load Network
        net = cv2.dnn.readNet("models\YOLOv4\yolov4.weights", "models\YOLOv4\yolov4.cfg")
        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(832, 832), scale=1 / 255)

        # Allow classes containing Vehicles only
        self.classes_allowed = [2, 3, 5, 6, 7, 8, 9]  # Include new class IDs for van (8) and three-wheelers (9)

    def detect_vehicles(self, img):
        # Detect Objects
        vehicles_boxes = []
        class_ids, scores, boxes = self.model.detect(img, nmsThreshold=0.4)
        for class_id, score, box in zip(class_ids, scores, boxes):
            if score < 0.5:
                # Skip detection with low confidence
                continue

            if class_id in self.classes_allowed:
                vehicles_boxes.append(box)

        return vehicles_boxes

    def detect_vehicles_with_labels(self, img):
        # Detect Objects with Labels
        vehicles_results = []
        class_ids, scores, boxes = self.model.detect(img, nmsThreshold=0.4)
        for class_id, score, box in zip(class_ids, scores, boxes):
            if score < 0.5:
                # Skip detection with low confidence
                continue

            if class_id in self.classes_allowed:
                x, y, w, h = box
                label = self.get_label(class_id)
                vehicles_results.append((x, y, w, h, label))

        return vehicles_results

    def get_label(self, class_id):
        # Map class ID to a label (customize this function based on your class labels)
        label_map = {2: 'Car', 3: 'Motorbike', 5: 'Bus', 6: 'Truck', 8: 'Van', 9: 'Three-Wheeler'}
        return label_map.get(class_id, 'Unknown')

    def draw_labeled_box(self, img, box, label, bg_color=(255, 255, 255), text_color=(0, 0, 0)):
        x, y, w, h = box

        # Calculate the width of the text
        (text_width, _), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

        # Draw background rectangle for the label with adjusted width
        cv2.rectangle(img, (x, y - 20), (x + text_width, y), bg_color, -1)

        # Draw rectangle around the vehicle
        cv2.rectangle(img, (x, y), (x + w, y + h), (57, 44, 226), 1)

        # Draw label on top of the rectangle
        cv2.putText(img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)