import cv2
import numpy as np

# Load the image
image_path = 'footages/images/blur.png'
# image_path = 'footages/images/input_image_700x480.png'  # Update this to the path of your image
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert image to grayscale

# Apply Laplacian operator in the image
laplacian = cv2.Laplacian(image, cv2.CV_64F)

# Calculate the variance of the laplacian
variance = laplacian.var()

print(f'Laplacian Variance: {variance}')

# Display the original image and the laplacian
cv2.imshow('Original Image', image)
cv2.imshow('Laplacian', laplacian)
cv2.waitKey(0)
cv2.destroyAllWindows()
