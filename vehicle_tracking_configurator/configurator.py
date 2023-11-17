"""The main backend for the configurator."""
# Copyright (C) 2023, NG:ITL

from json import load, dump, loads, dumps
from pathlib import Path
import numpy as np
import sys

from pynng import Sub0
from PIL import Image
import cv2


def find_base_directory() -> Path:
    """Find the base directory of the project."""
    search_paths = {Path().cwd(), Path().cwd().parent, Path(__file__).parent.parent}
    for directory in search_paths:
        if (directory / "vehicle_tracking_configurator_config.json").exists():
            return directory
    sys.exit(1)


class ConfiguratorHandler:
    """Handles the backend of the configurator."""

    def __init__(self) -> None:
        self.__video_size = (1332, 990)

        with open(find_base_directory() / "vehicle_tracking_configurator_config.json", "r") as config_file:
            conf = load(config_file)
            self.__recv_frames_address = conf["pynng"]["subscribers"]["camera_frame_receiver"]["address"]

        self.__camera_frame_receiver = Sub0(dial=self.__recv_frames_address)
        self.__camera_frame_receiver.subscribe("")

        self.__current_frame: np.ndarray

        self.__region_of_interest_points: list[tuple[int, int]] = [(100, 100), (100, 800), (1200, 800), (1200, 100)]
        self.__transformation_points: dict[str, dict[str, tuple[int, int]]] = {
            "top_left": {"real_world": (2, 2), "image": (300, 300)},
            "top_right": {"real_world": (5, 2), "image": (800, 300)},
            "bottom_left": {"real_world": (5, 2), "image": (300, 1100)},
            "bottom_right": {"real_world": (5, 2), "image": (800, 1100)},
        }

        self.__roi_color = "white"
        self.__roi_colors: dict[str, tuple[int, int, int, int]] = {
            "black": (0, 0, 0, 255),
            "gray": (64, 64, 64, 192),
            "white": (255, 255, 255, 255),
        }

    def read_drawer_frame(self) -> bytes:
        """Reads a new frame from the frames receiver.

        Returns:
            tuple[bytes]: The drawer frame with the points drawn on it.
        """
        frame_bytes: bytearray = self.__camera_frame_receiver.recv()
        self.__current_frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape(
            self.__video_size[1], self.__video_size[0], 3
        )
        frame = self.__current_frame.copy()
        frame = cv2.polylines(frame, [np.array(self.__region_of_interest_points)], True, (255, 255, 255), 2)

        for point_name, point in self.__transformation_points.items():
            if "image" not in point or "real_world" not in point:
                continue
            real_world: tuple[int, int] = point["real_world"]
            image_point: tuple[int, int] = point["image"]
            frame = cv2.circle(frame, image_point, 5, (255, 255, 255), -1)
            text = f"{real_world}; {point_name}"
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            match point_name:
                case "top_left":
                    offset_x = 10
                    offset_y = 10
                case "top_right":
                    offset_x = -text_size[0] - 10
                    offset_y = 10
                case "bottom_left":
                    offset_x = 10
                    offset_y = text_size[1] + 10
                case "bottom_right":
                    offset_x = -text_size[0] - 10
                    offset_y = text_size[1] + 10
                case _:
                    offset_x = 0
                    offset_y = 0
            frame = cv2.putText(
                frame,
                text,
                (image_point[0] + offset_x, image_point[1] + offset_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

        return frame.tobytes()

    def read_shower_frame(self) -> bytes:
        """Reads a new frame from the frames receiver.

        Returns:
            tuple[bytes]: The shower frame with the points drawn on it.
        """
        frame = self.__current_frame.copy()
        image_frame = Image.fromarray(frame)

        rgba_color = self.__roi_colors[self.__roi_color]

        image_mask = Image.new("RGBA", (self.__video_size[0], self.__video_size[1]), rgba_color)
        cv2_mask = np.array(image_mask)
        cv2_mask = cv2.fillPoly(cv2_mask, [np.array(self.__region_of_interest_points)], (0, 0, 0, 0))
        image_mask = Image.fromarray(cv2_mask)

        image_frame.paste(image_mask, mask=image_mask)
        image_frame.convert("RGB")
        frame = np.array(image_frame)

        return frame.tobytes()


if __name__ == "__main__":
    configurator_handler = ConfiguratorHandler()

    while True:
        drawer = configurator_handler.read_drawer_frame()
        shower = configurator_handler.read_shower_frame()
        cv2.imshow("frame", drawer)
        cv2.imshow("shower", shower)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
