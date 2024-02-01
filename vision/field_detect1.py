import cv2
import numpy as np

def find_foosball_table(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise and help edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Canny edge detector to find edges
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours in the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the contour with the maximum area (assumed to be the foosball table)
    max_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding box of the foosball table
    x, y, w, h = cv2.boundingRect(max_contour)
    
    # Draw a boundary around the foosball table
    cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 2)
    
    # Assign specific coordinates to the corners
    top_left = (x, y)
    top_right = (x + w, y)
    bottom_left = (x, y + h)
    bottom_right = (x + w, y + h)
    
    # Draw circles at the corner coordinates
    cv2.circle(frame, top_left, 5, (255, 0, 0), -1)
    cv2.circle(frame, top_right, 5, (255, 0, 0), -1)
    cv2.circle(frame, bottom_left, 5, (255, 0, 0), -1)
    cv2.circle(frame, bottom_right, 5, (255, 0, 0), -1)
    
    # Display coordinates at the corners
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f'TL: {top_left}', (x - 20, y - 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f'TR: {top_right}', (x + w + 5, y - 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f'BL: {bottom_left}', (x - 20, y + h + 15), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f'BR: {bottom_right}', (x + w + 5, y + h + 15), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
    return frame

# Capture video from the default camera (you can change the argument to use a different camera)
cap = cv2.VideoCapture(2)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()
    
    # Perform foosball table detection
    result_frame = find_foosball_table(frame)
    
    # Display the result
    cv2.imshow('Foosball Table Detection', result_frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
