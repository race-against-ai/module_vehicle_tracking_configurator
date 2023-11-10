import cv2
import pynng
import time
import numpy as np

source = cv2.VideoCapture("test_video_1.h265")

pub = pynng.Pub0(listen="ipc:///tmp/RAAI/camera_frame.ipc")

while source.isOpened():
    success, image = source.read()
    if not success:
        source.release()
    print("yes")
    cv2.imshow("test", image)
    cv2.waitKey(1)
    pub.send(np.array(image).tobytes())
    time.sleep(0.16666)
