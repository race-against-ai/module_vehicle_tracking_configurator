"""The backend handling the configuration"""
# Copyright (C) 2023, NG:ITL

from json import load, loads, dumps
from pathlib import Path
import sys

from pynng import Sub0, Pub0
from PIL import Image
import numpy as np
import cv2

from vehicle_tracking_configurator.topview_transformation import TopviewTransformation


REGION_OF_INTEREST = "Region of Interest"
TRANSFORMATION_POINTS = "Transformation Points"


def find_base_directory() -> Path:
    """Find the base directory of the project. If not found exits the program.

    Returns:
        Path: The base directory.
    """
    search_paths = {Path().cwd(), Path().cwd().parent, Path(__file__).parent.parent}
    for directory in search_paths:
        if (directory / "vehicle_tracking_configurator_config.json").exists():
            return directory
    sys.exit(1)


class ConfiguratorHandler:
    """Handles the backend of the configurator."""

    __VIDEO_SIZE = (1332, 990)
    __REAL_WORLD_SIZE = (7.5, 5.0)

    def __init__(self) -> None:
        with open(
            find_base_directory() / "vehicle_tracking_configurator_config.json", "r", encoding="utf-8"
        ) as config_file:
            conf = load(config_file)
            pynng_config = conf["pynng"]
            subscribers = pynng_config["subscribers"]
            publishers = pynng_config["publishers"]
            recv_frames = subscribers["camera_frame_receiver"]
            recv_tracker_config = subscribers["tracker_config"]
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

        self.current_selected_point: dict[str, str | int] = {REGION_OF_INTEREST: 0, TRANSFORMATION_POINTS: "top_left"}
        self.__transformation_points = ["top_left", "top_right", "bottom_left", "bottom_right"]
        self.region_of_interest_points: list[tuple[int, int]] = []
        self.configured_transformation_points: dict[str, dict[str, tuple[float, float] | tuple[int, int]]] = {
            "top_left": {"real_world": (0, 0), "image": (0, 0)},
            "top_right": {"real_world": (0, 0), "image": (0, 0)},
            "bottom_left": {"real_world": (0, 0), "image": (0, 0)},
            "bottom_right": {"real_world": (0, 0), "image": (0, 0)},
        }
        self.__topview_transformation = TopviewTransformation()

        self.roi_color: tuple[int, int, int, int] = (0, 0, 0, 255)
        self.__current_frame: np.ndarray

    def __calculate_real_point(
        self, clicked_point: tuple[int, int], video_size: tuple[int, int], full_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Calculates the real image point of different sized videos.

        Args:
            clicked_point (tuple[int, int]): The clicked point on the video.
            video_size (tuple[int, int]): The size of the video.
            full_size (tuple[int, int]): The size of the video with borders.

        Returns:
            tuple[int, int]: The real image point.
        """
        width_border_subtract = (full_size[0] - video_size[0]) // 2
        height_border_subtract = (full_size[1] - video_size[1]) // 2

        width_factor = self.__VIDEO_SIZE[0] / video_size[0]
        height_factor = self.__VIDEO_SIZE[1] / video_size[1]

        x, y = clicked_point[0] - width_border_subtract, clicked_point[1] - height_border_subtract

        image_x, image_y = int((x * width_factor)), int((y * height_factor))

        image_x = int(np.clip(image_x, 0, self.__VIDEO_SIZE[0]))
        image_y = int(np.clip(image_y, 0, self.__VIDEO_SIZE[1]))

        return image_x, image_y

    def read_drawer_frame(self) -> bytes:
        """Reads a new frame from the frames receiver.

        Returns:
            bytes: The drawer frame with the points drawn on it.
        """
        frame_bytes: bytearray = self.__camera_frame_receiver.recv()
        self.__current_frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape(
            self.__VIDEO_SIZE[1], self.__VIDEO_SIZE[0], 3
        )
        frame = self.__current_frame.copy()
        if len(self.region_of_interest_points) > 0:
            frame = cv2.polylines(frame, [np.array(self.region_of_interest_points)], True, (255, 255, 255), 2)

        for point_name, point in self.configured_transformation_points.items():
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
                    offset_y = text_size[1] - 10
                case "bottom_right":
                    offset_x = -text_size[0] - 10
                    offset_y = text_size[1] - 10
                case _:
                    raise ValueError(f"Point name '{point_name}' is invalid.")
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
            bytes: The shower frame with the points drawn on it.
        """
        frame = self.__current_frame.copy()
        image_frame = Image.fromarray(frame)

        image_mask = Image.new("RGBA", (self.__VIDEO_SIZE[0], self.__VIDEO_SIZE[1]), self.roi_color)
        cv2_mask = np.array(image_mask)
        cv2_mask = cv2.cvtColor(cv2_mask, cv2.COLOR_RGBA2BGRA)
        if len(self.region_of_interest_points) > 0:
            cv2_mask = cv2.fillPoly(cv2_mask, [np.array(self.region_of_interest_points)], (0, 0, 0, 0))
        image_mask = Image.fromarray(cv2_mask)

        image_frame.paste(image_mask, mask=image_mask)
        image_frame.convert("RGB")
        frame = np.array(image_frame)

        return frame.tobytes()

    def receive_config(self) -> None:
        """Receives a new configuration from the supported modules."""
        config_bytes_tracker: bytes = self.__tracker_config_receiver.recv(block=False)
        config_text_tracker: str = config_bytes_tracker.decode("utf-8")
        config_text_tracker = config_text_tracker[config_text_tracker.find(" ") :]
        config_tracker = loads(config_text_tracker)

        self.region_of_interest_points.clear()
        self.configured_transformation_points.clear()
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
            self.configured_transformation_points[point_name] = {
                "image": (point["image"][0], point["image"][1]),
                "real_world": (point["real_world"][0], point["real_world"][1]),
            }

    def send_config(self) -> None:
        """Sends the current configuration to the tracker."""
        config = {
            "region_of_interest": self.region_of_interest_points,
            "transformation_points": self.configured_transformation_points,
        }
        config_text = dumps(config)
        self.__config_sender.send(self.__send_config_topics["tracker"] + config_text.encode("utf-8"))

    def get_real_world_point(self, point: tuple[int, int]) -> tuple[float, float]:
        """Transforms a point from the image to the real world.

        Args:
            point (tuple[int, int]): The point on the image.

        Returns:
            tuple[float, float]: The point in the real world.
        """
        return self.__topview_transformation.image_to_world_transform(point)

    def get_image_point(self, point: tuple[float, float]) -> tuple[int, int]:
        """Transforms a point from the real world to the image.

        Args:
            point (tuple[float, float]): The point in the real world.

        Returns:
            tuple[int, int]: The point on the image.
        """
        return self.__topview_transformation.world_to_image_transform(point)

    def roi_config_text_changed(
        self, is_image_coord: bool, coord_index: int, number: float
    ) -> tuple[int, int, float, float]:
        """Changes the ROI configuration.

        Args:
            is_image_coord (bool): If the changed text is image or real world coordinate.
            coord_index (int): The index of the coordinate.
            number (float): The converted value of the coordinate.

        Returns:
            tuple[int, int, float, float]: The real world and image coordinates.
        """
        current_index = int(self.current_selected_point[REGION_OF_INTEREST])

        if current_index == len(self.region_of_interest_points):
            self.region_of_interest_points.append((0, 0))

        if is_image_coord:
            np.clip(number, 0, self.__VIDEO_SIZE[coord_index])

            image_coords_list = list(self.region_of_interest_points[current_index])
            image_coords_list[coord_index] = int(number)
            image_coords = (image_coords_list[0], image_coords_list[1])
            real_coords_tuple = self.get_real_world_point((image_coords[0], image_coords[1]))
            self.region_of_interest_points[current_index] = (image_coords[0], image_coords[1])
        else:
            np.clip(number, 0, self.__REAL_WORLD_SIZE[coord_index])

            real_coords_tuple = self.get_real_world_point(self.region_of_interest_points[current_index])
            real_coords = list(real_coords_tuple)
            real_coords[coord_index] = number
            real_coords_tuple = (real_coords[0], real_coords[1])
            image_coords = self.get_image_point((real_coords[0], real_coords[1]))
            self.region_of_interest_points[current_index] = (image_coords[0], image_coords[1])

        return int(real_coords_tuple[0]), int(real_coords_tuple[1]), float(image_coords[0]), float(image_coords[1])

    def transformation_config_text_changed(
        self, is_image_coord: bool, coord_index: int, number: float
    ) -> tuple[int, int, float, float]:
        """Changes the transformation configuration.

        Args:
            is_image_coord (bool): If the changed text is image or real world coordinate.
            coord_index (int): The index of the coordinate.
            number (int): The converted value of the coordinate.

        Returns:
            tuple[int, int, float, float]: The real world and image coordinates.
        """
        current_selected = str(self.current_selected_point[TRANSFORMATION_POINTS])
        key: str
        if is_image_coord:
            key = "image"
        else:
            key = "real_world"
        to_change = self.configured_transformation_points[current_selected][key]
        to_change = (number, to_change[1]) if coord_index == 0 else (to_change[0], number)
        self.configured_transformation_points[current_selected][key] = to_change

        image_x, image_y = self.configured_transformation_points[current_selected]["image"]
        real_x, real_y = self.configured_transformation_points[current_selected]["real_world"]

        return (int(image_x), int(image_y), float(real_x), float(real_y))

    def roi_color_changed(self, input_id: str, text: str) -> tuple[int, int, int, int]:
        """Changes the ROI color.

        Args:
            input_id (str): The color that was changed.
            text (str): The new value of the color.

        Returns:
            tuple[int, int, int, int]: The new color.
        """
        value_names = {"red": 0, "green": 1, "blue": 2, "alpha": 3}
        color_index = value_names[input_id]

        if len(text) == 0:
            color_list = list(self.roi_color)
            color_list[color_index] = 0
            self.roi_color = (color_list[0], color_list[1], color_list[2], color_list[3])
        else:
            value = int(text)
            value_clipped = np.clip(value, 0, 255)

            color_list = list(self.roi_color)
            color_list[color_index] = value_clipped
            self.roi_color = (color_list[0], color_list[1], color_list[2], color_list[3])

        return self.roi_color

    def delete_button_pressed(self, config_name: str) -> None:
        """Deletes a point from the configuration.

        Args:
            config_name (str): The name of the configuration.
            current_selected (tuple[int, str]): The currently selected point.
        """
        current_index: str | int
        match config_name:
            case "Region of Interest":
                current_index = int(self.current_selected_point[REGION_OF_INTEREST])
                if current_index == len(self.region_of_interest_points):
                    return
                self.region_of_interest_points.pop(current_index)
                self.current_selected_point[REGION_OF_INTEREST] = np.clip(
                    current_index, 0, len(self.region_of_interest_points)
                )
            case "Transformation Points":
                current_index = str(self.current_selected_point[TRANSFORMATION_POINTS])
                self.add_transformation_point((0, 0), (0.0, 0.0), current_index)

    def add_transformation_point(
        self, image_coords: tuple[int, int], real_coords: tuple[float, float], coord_name: str
    ) -> None:
        """Configures a point in the real world transformation.

        Args:
            image_coords (tuple[int, int]): The coordinates of the point on the image.
            real_coords (tuple[float, float]): The coordinates of the point in the real world.
            coord_name (str): The name of the point.
        """
        self.configured_transformation_points[coord_name] = {"image": image_coords, "real_world": real_coords}
        self.__topview_transformation.set_transformation_point(coord_name, image_coords, real_coords)

    def color_chooser_button(self, button_color: str) -> tuple[int, int, int, int]:
        """Changes the ROI color.

        Args:
            button_color (str): The text of the button that was clicked.

        Returns:
            tuple[int, int, int, int]: The new color.
        """
        color = (0, 0, 0, 0)
        match button_color.lower():
            case "white":
                color = (255, 255, 255, 255)
            case "gray":
                color = (64, 64, 64, 192)
            case "black":
                color = (0, 0, 0, 255)
        self.roi_color = color
        return color

    def points_drawer_clicked(
        self, active_mode: str, clicked_point: tuple[int, int], video_size: tuple[int, int], full_size: tuple[int, int]
    ) -> tuple[int, int, float, float]:
        """Handles the click event on the points drawer.

        Args:
            active_mode (str): The active mode.
            clicked_point (tuple[int, int]): The coordinates of the clicked point.
            video_size (tuple[int, int]): The size of the video.
            full_size (tuple[int, int]): The size of the video with borders.

        Raises:
            ValueError: If the active mode is invalid.

        Returns:
            tuple[int, int, float, float]: The configured point data.
        """
        image_coords = self.__calculate_real_point(clicked_point, video_size, full_size)

        match active_mode:
            case "Region of Interest":
                configured_points = self.__points_drawer_clicked_mode_roi(image_coords)
            case "Transformation Points":
                configured_points = self.__points_drawer_clicked_mode_transformation(image_coords)
            case _:
                raise ValueError(f"Active mode '{active_mode}' is invalid.")

        return configured_points

    def __points_drawer_clicked_mode_roi(self, point_coords: tuple[int, int]) -> tuple[int, int, float, float]:
        """Handles the click event on the points drawer in ROI mode.

        Args:
            point_coords (tuple[int, int]): The coordinates of the clicked point.

        Returns:
            tuple[int, int, float, float]: The clicked point data.
        """
        real_x, real_y = self.get_real_world_point(point_coords)

        current_index = int(self.current_selected_point[REGION_OF_INTEREST])
        is_new = current_index == len(self.region_of_interest_points)
        if is_new:
            self.region_of_interest_points.append((0, 0))
            self.current_selected_point[REGION_OF_INTEREST] = current_index + 1
            return_coords = (0, 0, 0.0, 0.0)
        else:
            return_coords = (int(point_coords[0]), int(point_coords[1]), float(real_x), float(real_y))

        self.region_of_interest_points[current_index] = point_coords

        return return_coords

    def __points_drawer_clicked_mode_transformation(
        self, point_coords: tuple[int, int]
    ) -> tuple[int, int, float, float]:
        """Handles the click event on the points drawer in transformation mode.

        Args:
            point_coords (tuple[int, int]): The coordinates of the clicked point.

        Returns:
            tuple[int, int, float, float]: The clicked point data.
        """
        current_point = str(self.current_selected_point[TRANSFORMATION_POINTS])
        real_x, real_y = self.configured_transformation_points[current_point]["real_world"]

        self.configured_transformation_points[current_point]["image"] = point_coords
        self.add_transformation_point(point_coords, (real_x, real_y), current_point)

        return (int(point_coords[0]), int(point_coords[1]), float(real_x), float(real_y))

    def points_shower_clicked(
        self, clicked_point: tuple[int, int], video_size: tuple[int, int], full_size: tuple[int, int]
    ) -> tuple[int, int, float, float]:
        """Handles the click event on the points shower.

        Args:
            clicked_point (tuple[int, int]): The coordinates of the clicked point.
            video_size (tuple[int, int]): The size of the video.
            full_size (tuple[int, int]): The size of the video with borders.

        Returns:
            tuple[int, int, float, float]: The clicked point data.
        """
        image_x, image_y = self.__calculate_real_point(clicked_point, video_size, full_size)
        real_x, real_y = self.get_real_world_point((image_x, image_y))

        return (int(image_x), int(image_y), float(real_x), float(real_y))

    def arrow_button_clicked(self, config_name: str, direction: str) -> tuple[str, tuple[int, int, float, float]]:
        """Moves the currently selected point.

        Args:
            config_name (str): The name of the configuration.
            direction (str): The direction of the clicked button.

        Raises:
            ValueError: If the config name is invalid.

        Returns:
            tuple[str, tuple[int, int, float, float]]: The new point data.
        """
        match config_name:
            case "Region of Interest":
                return self.__roi_arrow_button_clicked(direction)
            case "Transformation Points":
                return self.__transformation_arrow_button_clicked(direction)
            case _:
                raise ValueError(f"Config name '{config_name}' is invalid.")

    def __roi_arrow_button_clicked(self, direction: str) -> tuple[str, tuple[int, int, float, float]]:
        """Moves the currently selected ROI point.

        Args:
            direction (str): The direction of the clicked button.

        Returns:
            tuple[str, tuple[int, int, float, float]]: The new point data.
        """
        current_index = int(self.current_selected_point[REGION_OF_INTEREST])
        to_modulo_with = len(self.region_of_interest_points) + 1
        next_index = (current_index + 1 if direction == "right" else current_index - 1) % to_modulo_with
        self.current_selected_point[REGION_OF_INTEREST] = next_index

        if next_index == to_modulo_with - 1:
            point_text = "new"
            image_coords, real_coords = (0, 0), (0.0, 0.0)
        else:
            point_text = str(next_index)
            image_coords = self.region_of_interest_points[int(self.current_selected_point[REGION_OF_INTEREST])]
            real_coords = self.get_real_world_point((image_coords[0], image_coords[1]))

        return (
            point_text,
            (int(image_coords[0]), int(image_coords[1]), float(real_coords[0]), float(real_coords[1])),
        )

    def __transformation_arrow_button_clicked(self, direction: str) -> tuple[str, tuple[int, int, float, float]]:
        """Moves the currently selected transformation point.

        Args:
            direction (str): The direction of the clicked button.

        Returns:
            tuple[str, tuple[int, int, float, float]]: The new point data.
        """
        current_index = self.__transformation_points.index(str(self.current_selected_point[TRANSFORMATION_POINTS]))
        next_index = (current_index + 1 if direction == "right" else current_index - 1) % 4
        next_name = self.__transformation_points[next_index]
        self.current_selected_point[TRANSFORMATION_POINTS] = next_name

        conf = self.configured_transformation_points[next_name]
        image_coords = (int(conf["image"][0]), int(conf["image"][1]))
        real_coords = conf["real_world"]

        return (
            next_name,
            (int(image_coords[0]), int(image_coords[1]), float(real_coords[0]), float(real_coords[1])),
        )
