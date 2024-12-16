#!/usr/bin/env python
"""Transmits a video file over IPC to the RAAI camera frame subscriber.""" ""
# Copyright (C) 2023, NG:ITL

from pathlib import Path
import time

import numpy as np
import pynng
import cv2


BASE_DIR = Path(__file__).parent.parent


source = cv2.VideoCapture(str(BASE_DIR / "resources" / "test_video_1.h265"))

pub = pynng.Pub0(listen="ipc:///tmp/RAAI/camera_frame.ipc")

print("Starting Transmission")

while True:
    success, image = source.read()
    if not success:
        source = cv2.VideoCapture("resources/test_video_1.h265")
        success, image = source.read()
        if not success:
            raise FileNotFoundError("The video file could not be found or read.")
    pub.send(np.array(image).tobytes())
    time.sleep(0.016666)
