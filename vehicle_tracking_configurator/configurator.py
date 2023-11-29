"""The main backend for the configurator."""
# Copyright (C) 2023, NG:ITL

from json import load, loads, dumps
from pathlib import Path
import numpy as np
import sys

from pynng import Sub0, Pub0
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
            pynng_config = conf["pynng"]
            receivers = pynng_config["subscribers"]
            publishers = pynng_config["publishers"]
            recv_frames = receivers["camera_frame_receiver"]
            recv_tracker_config = receivers["tracker_config"]
            send_config = publishers["config_sender"]
            self.__recv_frames_address = recv_frames["address"]
            self.__recv_frames_topics: dict[str, str] = recv_frames["topics"]
            self.__recv_tracker_config_address = recv_tracker_config["address"]
            self.__recv_tracker_config_topics = recv_tracker_config["topics"]
            self.__send_config_address = send_config["address"]
            self.__send_config_topics = send_config["topics"]

        self.__camera_frame_receiver = Sub0(dial=self.__recv_frames_address)
        self.__camera_frame_receiver.subscribe(list(self.__recv_frames_topics.values()))
        self.__tracker_config_receiver = Sub0(dial=self.__recv_tracker_config_address)
        self.__tracker_config_receiver.subscribe(list(self.__recv_tracker_config_topics.values()))

        self.__config_sender = Pub0(listen=self.__send_config_address)

        self.__current_frame: np.ndarray

        self.region_of_interest_points: list[tuple[int, int]] = [(100, 100), (100, 800), (1200, 800), (1200, 100)]
        self.transformation_points: dict[str, dict[str, tuple[float, float] | tuple[int, int]]] = {
            "top_left": {"real_world": (2, 2), "image": (300, 300)},
            "top_right": {"real_world": (5, 2), "image": (800, 300)},
            "bottom_left": {"real_world": (5, 2), "image": (300, 1100)},
            "bottom_right": {"real_world": (5, 2), "image": (800, 1100)},
        }
        self.__transformation_points_ready: bool = False

        self.roi_color: tuple[int, int, int, int] = (0, 0, 0, 255)

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
        frame = cv2.polylines(frame, [np.array(self.region_of_interest_points)], True, (255, 255, 255), 2)

        for point_name, point in self.transformation_points.items():
            if "image" not in point or "real_world" not in point:
                continue
            real_world = point["real_world"]
            image_point = point["image"]
            image_point = (int(image_point[0]), int(image_point[1]))
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

        image_mask = Image.new("RGBA", (self.__video_size[0], self.__video_size[1]), self.roi_color)
        cv2_mask = np.array(image_mask)
        cv2_mask = cv2.cvtColor(cv2_mask, cv2.COLOR_RGBA2BGRA)
        cv2_mask = cv2.fillPoly(cv2_mask, [np.array(self.region_of_interest_points)], (0, 0, 0, 0))
        image_mask = Image.fromarray(cv2_mask)

        image_frame.paste(image_mask, mask=image_mask)
        image_frame.convert("RGB")
        frame = np.array(image_frame)

        return frame.tobytes()

    def receive_config(self) -> None:
        """Receives a new configuration from the tracker."""
        config_bytes_tracker: bytes = self.__tracker_config_receiver.recv()
        config_text_tracker: str = config_bytes_tracker.decode("utf-8")
        config_text_tracker = config_text_tracker[config_text_tracker.find(" ") :]
        config_tracker = loads(config_text_tracker)

        self.region_of_interest_points.clear()
        self.transformation_points.clear()
        for point in config_tracker["region_of_interest"]:
            if isinstance(point[0], int) and isinstance(point[1], int):
                self.region_of_interest_points.append((point[0], point[1]))
        for point_name, point in config_tracker["transformation_points"].items():
            if (
                "image" not in point
                or "real_world" not in point
                or not isinstance(point["image"][0], int)
                or not isinstance(point["image"][1], int)
                or not isinstance(point["real_world"][0], float)
                or not isinstance(point["real_world"][1], float)
            ):
                continue
            self.transformation_points[point_name] = {
                "image": (point["image"][0], point["image"][1]),
                "real_world": (point["real_world"][0], point["real_world"][1]),
            }

    def send_config(self) -> None:
        """Sends the current configuration to the tracker."""
        config = {
            "region_of_interest": self.region_of_interest_points,
            "transformation_points": self.transformation_points,
        }
        config_text = dumps(config)
        self.__config_sender.send(self.__send_config_topics["tracker"] + config_text.encode("utf-8"))

    def get_real_world_point(self, point: tuple[int, int]) -> tuple[float, float]:
        """Gets the real world coordinates of a point in the image."""
        if self.__transformation_points_ready:
            # TODO: Add the method to calculate the real world coordinates of a point.
            raise NotImplementedError()
        else:
            return (0, 0)

    def delete_button_pressed(self, config_name: str, current_selected: tuple[int, str]) -> None:
        """Deletes a point from the configuration."""
        if config_name == "region_of_interest" and isinstance(current_selected, int):
            self.region_of_interest_points.pop(current_selected[0])
        elif config_name == "transformation_points" and isinstance(current_selected, str):
            self.transformation_points[current_selected[1]].clear()

    def configure_points(self, coord: tuple[int, int]) -> None:
        """Configures a point."""
        # TODO: Implement the function into the code. Implement when function chooser is merged.
        print(coord)


if __name__ == "__main__":
    configurator_handler = ConfiguratorHandler()

    while True:
        drawer = np.frombuffer(configurator_handler.read_drawer_frame())
        shower = np.frombuffer(configurator_handler.read_shower_frame())
        cv2.imshow("frame", drawer)
        cv2.imshow("shower", shower)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
