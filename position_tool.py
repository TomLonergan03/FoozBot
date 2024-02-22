import cv2
import pandas as pd

f = open("frames.csv", "w")


def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        line = f'{i}, {x}, {y}\n'
        print(line)
        f.write(line)


# import video
video = cv2.VideoCapture("2024-02-22-113446.webm")
cv2.namedWindow("Video")
cv2.setMouseCallback("Video", draw_circle)


for i in range(int(video.get(cv2.CAP_PROP_FRAME_WIDTH))):
    ret, frame = video.read()
    if not ret:
        break
    cv2.putText(frame, f"Frame: {i}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Video", frame)
    if i < 0:
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
    else:
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
f.close()
