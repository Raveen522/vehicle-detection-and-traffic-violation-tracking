from ultralytics import YOLO
import cv2
import cvzone
import math

model = YOLO('yolo_models/yolov8n.pt')
# results = model("footages/images/input_image_03.png", show = True) 
cv2.waitKey(0)

cap = cv2.VideoCapture(0) #input camera
# cap = cv2.VideoCapture("footages/videos/night.mp4") #input camera
# cap = cv2.VideoCapture("footages/videos/bikes.mp4") #input camera
# cap = cv2.VideoCapture("footages/videos/jam.mp4") #input camera
cap.set(3, 1280)
cap.set(4, 720)


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

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)

            #confidence ratio
            confident_number = math.ceil((box.conf[0]*100))

            #Class names
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            if currentClass == "car" or currentClass == "truck" or currentClass == "bus" or currentClass == "motorbike" and confident_number > 20:
                cvzone.putTextRect(img,f'{currentClass} {confident_number}',(max(0,x1),max(35,y1)), scale=1,thickness=1)
                
                #draw bounding box
                w, h = x2-x1, y2-y1    
                cvzone.cornerRect(img,(x1,y1,w,h),l=5)

    cv2.imshow("Image",img)
    cv2.waitKey(1)