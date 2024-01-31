import cv2
import numpy as np

# Start capturing video
vid = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = vid.read()
    if not ret:
        print("Failed to grab frame")
        break
    origin_x = 0
    origin_y = 0
    max_x = 100
    max_y = 100
    biggest_pink = 0
    biggest_green = 0
    # Convert the captured frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_pink = np.array([113, 69, 154])
    upper_pink = np.array([182, 189, 245])
    lower_green = np.array([35, 28, 114])
    upper_green = np.array([78, 224, 215])

    mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the masks
    contours_pink, _ = cv2.findContours(mask_pink, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours
    for contour in contours_pink:   
        # Approximate the contour
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        # Find the bounding box of the contour
        x, y, w, h = cv2.boundingRect(approx)
        # Draw the bounding box on the original frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Find top left of the pink assuming pink is origin
        if w >= biggest_pink and h >= biggest_pink:
            origin_x = int(x + w/2)
            origin_y = int(y + h/2)
            if h > w:
                biggest_pink = h
            else:
                biggest_pink = w

    
    # Loop over the contours
    for contour in contours_green:   
        # Approximate the contour
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        # Find the bounding box of the contour
        x, y, w, h = cv2.boundingRect(approx)
        # Draw the bounding box on the original frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)

        # Find bottom right of the green assuming green is maximum
        if w >= biggest_green and h >= biggest_green:    
            max_x = int(x + w/2)
            max_y = int(y + h/2)
            if h > w:
                biggest_green = h
            else:
                biggest_green = w
    
    # Swap origin and max if the player has rotated the board 180 degrees
    if origin_x > max_x or origin_y > max_y:
        temp = origin_x
        origin_x = max_x
        max_x = temp
        temp = origin_y
        origin_y = max_y
        max_y = temp

    cv2.putText(frame, str(origin_x) + " , " + str(origin_y), (origin_x, origin_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0))
    cv2.putText(frame, str(max_x) + " , " + str(max_y), (max_x, max_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (110, 110, 110))
    cv2.rectangle(frame, (origin_x, origin_y), (max_x, max_y), (255, 0, 0), 2)

    # Display the original frame with bounding box
    cv2.imshow('frame with bounding box', frame)

    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy all windows
vid.release()
cv2.destroyAllWindows()
