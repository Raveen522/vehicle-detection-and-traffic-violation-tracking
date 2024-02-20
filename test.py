import cv2

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

image_path = 'footages/images/blur.png' 

image = cv2.imread(image_path)
if image is None:
    print("Error loading image")
else:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    threshold = 5000
    if fm > threshold:
        print(f"Image is blurry, focus measure: {fm}")
    else:
        print(f"Image is clear, focus measure: {fm}")


