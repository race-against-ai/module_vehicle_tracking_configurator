# Copyright (C) 2023, NG:ITL

from pathlib import Path
import numpy as np
import time
import sys

import pynng
import cv2

def find_base_directory() -> Path:
    """Find the base directory of the project."""
    search_paths = {Path().cwd(), Path().cwd().parent, Path(__file__).parent.parent}
    for directory in search_paths:
        if (directory / "vehicle_tracking_configurator_config.json").exists():
            return directory
    sys.exit(1)

base_dir = find_base_directory()

source = cv2.VideoCapture(str(base_dir / "resources" / "test_video_1.h265"))

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
