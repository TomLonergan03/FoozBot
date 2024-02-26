from model import Model, Location, Trajectory
import pandas as pd
import cv2
from collections import deque
from copy import deepcopy


ball_location = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

futures = deque(maxlen=10)

with open("frames_done_30fps.csv") as g:
    while line := g.readline():
        if "frame" in line:
            continue
        _, frame, x, y = line.split(",")
        ball_location[int(frame)] = (int(x), int(y))
ball_location_cleaned = [x for x in ball_location if x is not None]

# import video
video = cv2.VideoCapture("2024-02-22-113446.webm")
cv2.namedWindow("Video")

out = cv2.VideoWriter("output.avi",
                      cv2.VideoWriter_fourcc(*"MJPG"), 30, (1280, 720))

ATTRACTION_FORCE_X = 0.000001
ATTRACTION_FORCE_Y = 0.00001
FRICTION = 0.05
FRICTION_LIMIT = 0
ATTRACTION_MIN_SPEED = 0

CALCULATE_AVG = False

model = Model(Location(0, 0, 0), FRICTION, ATTRACTION_FORCE_X,
              ATTRACTION_FORCE_Y, 92, 41, 1190, 614, iterations=20,
              friction_limit=FRICTION_LIMIT, attraction_min_speed=ATTRACTION_MIN_SPEED)


def process_frame(frame, location, frame_number):
    cv2.putText(frame, f"Frame: {frame_number}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    for j in range(1, len(ball_location_cleaned)):
        cv2.line(frame, ball_location_cleaned[j - 1],
                 ball_location_cleaned[j], (255, 0, 0), 5)
    if location is not None:
        cv2.circle(frame, location, 5, (0, 0, 255), -1)
        trajectory = model.update(Location(
            location[0], location[1], frame_number))
        futures.append(trajectory)
        if CALCULATE_AVG:
            for future in futures:
                for frame_number in range(1, len(future.locations)):
                    cv2.line(frame, (int(future.locations[frame_number-1].x), int(future.locations[frame_number-1].y)),
                             (int(future.locations[frame_number].x), int(future.locations[frame_number].y)), (0, 180, 100), 2)
            avg = [] * len(futures[0].locations)
            for frame_number in range(len(futures[0].locations)):
                avg.append(Location(0, 0, 0))
            for future in futures:
                for frame_number in range(len(future.locations)):
                    avg[frame_number] = Location(avg[frame_number].x + future.locations[frame_number].x,
                                                 avg[frame_number].y + future.locations[frame_number].y, future.locations[frame_number].time)
            for av in avg:
                av.x = av.x / len(futures)
                av.y = av.y / len(futures)
        else:
            avg = futures[-1].locations
        for frame_number in range(1, len(avg)):
            cv2.line(frame, (int(avg[frame_number-1].x), int(avg[frame_number-1].y)),
                     (int(avg[frame_number].x), int(avg[frame_number].y)), (0, 255, 0), 2)
    out.write(frame.astype('uint8'))
    cv2.imshow("Video", frame)


for i in range(int(video.get(cv2.CAP_PROP_FRAME_WIDTH))):
    ret, frame = video.read()
    if i == 85:
        break


cv2.createTrackbar("ATTRACTION_FORCE_X", "Video", 1, 100, lambda x: None)
cv2.createTrackbar("ATTRACTION_FORCE_Y", "Video", 10, 100, lambda x: None)
cv2.createTrackbar("FRICTION", "Video", 5, 100, lambda x: None)
cv2.createTrackbar("FRICTION_LIMIT", "Video", 0, 100, lambda x: None)
cv2.createTrackbar("ATTRACTION_MIN_SPEED", "Video", 0, 100, lambda x: None)

history = deque([Location(x=735.6293778215095, y=506.8194098974294, time=79),
                 Location(x=769.5864975316671, y=503.2721885544023, time=80)], maxlen=2)


while True:
    ret, frame = video.read()
    raw_frame = frame
    raw_model = deepcopy(model)
    i += 1
    while True:
        frame = deepcopy(raw_frame)
        model = deepcopy(raw_model)
        model.atraction_force_x = cv2.getTrackbarPos(
            "ATTRACTION_FORCE_X", "Video") / 1000000
        model.atraction_force_y = cv2.getTrackbarPos(
            "ATTRACTION_FORCE_Y", "Video") / 1000000
        model.friction = 1 - cv2.getTrackbarPos("FRICTION", "Video") / 1000
        model.friction_limit = cv2.getTrackbarPos(
            "FRICTION_LIMIT", "Video") / 100
        model.attraction_min_speed = cv2.getTrackbarPos(
            "ATTRACTION_MIN_SPEED", "Video") / 100
        process_frame(frame, ball_location[i], i)
        cv2.imshow("Video", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            video.release()
            out.release()
            exit()
        elif key == ord('n'):
            break

video.release()
out.release()
