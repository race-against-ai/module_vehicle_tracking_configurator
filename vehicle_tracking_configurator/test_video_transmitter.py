import cv2
import pynng
import time
import numpy as np

source = cv2.VideoCapture("resources/test_video_1.h265")
pub = pynng.Pub0(listen="ipc:///tmp/RAAI/camera_frame.ipc")

while True:
    success, image = source.read()
    if not success:
        source = cv2.VideoCapture("resources/test_video_1.h265")
        success, image = source.read()
        if not success:
            raise FileNotFoundError("The video file could not be found or read.")
    pub.send(np.array(image).tobytes())
    time.sleep(0.016666)
