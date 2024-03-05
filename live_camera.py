import cv2
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
    draw_label(frame,f"Camera ID: {camera_id}",(1050, 20))
    draw_label(frame,f"Signal light {signal_light_id}",(1050, 42))
    draw_label(frame,"Signal light status:",(1050, 65))
    if (signal_status == "Green"):
        draw_label(frame,signal_status,(1208, 65),(0, 230, 0))
    elif(signal_status == "Red"):
        draw_label(frame,signal_status,(1208, 65),(0, 0, 230))
    elif(signal_status == "Yellow"):
        draw_label(frame,signal_status,(1208, 65),(0, 230, 230))

    draw_label(frame,f"Road: {road_id}",(1050, 88))

    draw_label(frame,time_string,(20, 20))
    draw_label(frame,date_string,(20, 42))
#---------------------------------------------------------------------
    
# Function to take a snapshot and process it
def take_snapshot_and_process(camera_id, signal_light_id, signal_status, road_id, video_capture):
    # Read a frame from the video capture
    ret, frame = video_capture.read()

    # Check if the frame is successfully captured
    if not ret:
        print("Error: Unable to capture frame.")
        return

    # Overlay information on the frame
    overlay_info(camera_id, signal_light_id, signal_status, road_id, frame)

    # Display the live video
    cv2.imshow('Live Video', frame)
    cv2.waitKey(1)  # Adjust the waitKey value as needed for your frame rate

    # Take a snapshot
    snapshot_path = f"temp/snapshots/temp_snapshot_{camera_id}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    cv2.imwrite(snapshot_path, frame)

    # Send the snapshot to the image processing function
    process_image(snapshot_path)
#---------------------------------------------------------------------
    
# Function for image processing (replace this with your actual image processing logic)
def process_image(image_path):
    print(f"Processing image: {image_path}")
    # Your image processing logic goes here

# Function to display live video with overlay
def display_live_video(camera_id, signal_light_id, signal_status, road_id, video_capture):
    while True:
        # Read a frame from the video capture
        ret, frame = video_capture.read()

        # Check if the frame is successfully captured
        if not ret:
            print("Error: Unable to capture frame.")
            break

        # Overlay information on the frame
        overlay_info(camera_id, signal_light_id, signal_status, road_id, frame)

        # Display the live video
        cv2.imshow('Live Video', frame)
        key = cv2.waitKey(30)  # Adjust the waitKey value as needed for your frame rate

        # Check if the 's' key is pressed
        if key == ord('s'):
            # Take a snapshot and process it
            take_snapshot_and_process(camera_id, signal_light_id, signal_status, road_id, video_capture)

        # Break the loop if the 'q' key is pressed
        if key == ord('q'):
            break
#---------------------------------------------------------------------
        
# Test with sample data
camera_id = 1
signal_light_id = 123
road_id = 456
signal_status = "Green"

# Video capture from a file (replace with camera input)
video_capture = cv2.VideoCapture("footages/videos/input_video_01.mp4") #using video file
# video_capture = cv2.VideoCapture(0) #camera input

# Check if the video capture is successful
if not video_capture.isOpened():
    print("Error: Unable to open video capture.")
    exit()

# Display live video with overlay
display_live_video(camera_id, signal_light_id, signal_status, road_id, video_capture)

# Release the video capture object
video_capture.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
