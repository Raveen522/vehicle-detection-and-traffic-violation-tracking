import cv2

def is_image_blurry(image_path, threshold=100.0):
    # Load the image
    image = cv2.imread(image_path)
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Laplacian edge detection
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    # Calculate the variance
    variance = laplacian.var()
    
    # Determine if the image is blurry or clear
    if variance < threshold:
        print("Image is blurry. Variance:", variance)
        return True
    else:
        print("Image is clear. Variance:", variance)
        return False

# Example usage
image_path = 'footages/images/blur.png'  # Change this to your image path
is_image_blurry(image_path)

# Example usage
# image_path = 'footages/images/blur.png'  # Change this to your image path
# image_path = 'footages/images/input_image_high_traffic.png'  # Change this to your image path
# detect_edges_sobel(image_path)
# detect_edges_canny(image_path)
# detect_edges_laplacian(image_path)