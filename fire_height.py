"""
Attempts to calculate the flame height of a single image
"""
import numpy as np
import cv2
import time

start_frame_number = 7000
def get_frames(filename):
    video = cv2.VideoCapture(filename)
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number)
    while video.isOpened():
        rete, frame = video.read()
        if rete:
            yield frame
        else:
            continue
    video.release()
    yield None

video_path = "./B_1096.MOV"

# Visualize frame-differencing
last_frame = next(get_frames(video_path))
avg_frame = last_frame
num_frames = 1
for frame in get_frames(video_path):
    diff = avg_frame - frame
    diff = np.linalg.norm(diff, axis=(2))
    idx = diff < 50
    diff[idx] = 0

    diff_3_channel = cv2.cvtColor(diff.astype(np.float32), cv2.COLOR_GRAY2BGR)
    h1,w1 = diff_3_channel.shape[:2]
    h2,w2 = frame.shape[:2]
    side_by_side = np.zeros((max(h1,h2), w1+w2, 3), np.uint8)
    side_by_side[:h1, :w1,:3] = diff_3_channel
    side_by_side[:h2, w1:w1+w2,:3] = frame 

    cv2.imshow('frame', side_by_side)

    if cv2.waitKey(10) == 40:
        break

    last_frame = frame
    avg_frame = (avg_frame * num_frames + last_frame) / (num_frames + 1)
    num_frames += 1

    time.sleep(0.03)
