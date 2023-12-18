"""Transmits a video file over IPC to the RAAI camera frame subscriber."""""
# Copyright (C) 2023, NG:ITL

import time

import numpy as np
import pynng
import cv2

from utils.shared_functions import find_base_directory


BASE_DIR, error = find_base_directory()

if error:
    raise error
del error

source = cv2.VideoCapture(str(BASE_DIR / "resources" / "test_video_1.h265"))

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
