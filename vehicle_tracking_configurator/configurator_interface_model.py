# Copyright (C) 2023, NG:ITL

from PySide6.QtCore import QObject, Signal, Slot, SignalInstance
from numpy import clip

from vehicle_tracking_configurator.configurator import ConfiguratorHandler


REGION_OF_INTEREST = "Region of Interest"
TRANSFORMATION_POINTS = "Transformation Points"


class ModelVehicleTrackingConfigurator(QObject):
    """The main backend for the configurator.

    Args:
        configurator (ConfiguratorHandler): The configuration handler.
    """

    reload_image = Signal(name="reloadImage")

    color_text_changed_signal = Signal(list, name="colorTextChanged")

    region_of_interest_points_changed_signal = Signal(list, name="regionOfInterestPointsChanged")
    transformation_points_changed_signal = Signal(list, name="transformationPointsChanged")
    real_world_points_changed_signal = Signal(list, name="realWorldPointsChanged")

    region_of_interest_point_chosen_signal = Signal(str, name="regionOfInterestPointChosen")
    transformation_point_chosen_signal = Signal(str, name="transformationPointChosen")

    def __init__(self, configurator: ConfiguratorHandler) -> None:
        QObject.__init__(self)
        self.__configurator = configurator
        self.__current_selected_point: dict[str, str | int] = {REGION_OF_INTEREST: 1, TRANSFORMATION_POINTS: "top_left"}
        self.__transformation_points = ["top_left", "top_right", "bottom_left", "bottom_right"]

    def init_ui_data(self) -> None:
        # TODO: Implement the function into the code. Sets basic first data.
        print("!! IMPLEMENTATION NEEDED !!")

    @Slot(bool, bool, bool)  # type: ignore[arg-type]
    def updated_mode(self, roi_state: bool, t_point_state: bool, time_tracking_state: bool) -> None:
        print(f"roi_state: {roi_state}\n t_point_state: {t_point_state}\n time_tracking_state: {time_tracking_state}\n")

    @Slot(str)  # type: ignore[arg-type]
    def config_button_pressed(self, button_text: str) -> None:
        match button_text:
            case "Receive Config":
                self.__configurator.receive_config()
            case "Transmit Config":
                self.__configurator.send_config()

    @Slot(str, str, str)  # type: ignore[arg-type]
    def coordinate_text_changed(self, input_id: str, config_name: str, text: str) -> None:
        # TODO: Modify this to work with changing real world points
        # * Input: "imagePointXInput | Region of Interest | 1"
        if self.__current_selected_point[REGION_OF_INTEREST] == len(self.__configurator.region_of_interest_points):
            self.__configurator.region_of_interest_points.append((0, 0))

        point_index = 0 if input_id.find("X") != -1 else 1
        is_image_point = input_id.find("image") != -1

        if len(text) == 0:
            current_point_tuple = self.__configurator.region_of_interest_points[
                int(self.__current_selected_point[REGION_OF_INTEREST])
            ]
            current_point = list(current_point_tuple)
            current_point_tuple = (current_point[0], current_point[1])
            current_point[point_index] = 0
            match config_name:
                case "Region of Interest":
                    if is_image_point:
                        real_x, real_y = self.__configurator.get_real_world_point(current_point_tuple)
                        self.region_of_interest_points_changed_signal.emit(
                            [current_point[0], current_point[1], real_x, real_y]
                        )
                    else:
                        raise NotImplementedError()
                case "Transformation Points":
                    if is_image_point:
                        real_x, real_y = self.__configurator.get_real_world_point(current_point_tuple)
                        self.real_world_points_changed_signal.emit([current_point[0], current_point[1], real_x, real_y])
                    else:
                        raise NotImplementedError()

    @Slot(str, str)  # type: ignore[arg-type]
    def color_text_changed(self, input_id: str, text: str) -> None:
        value_names = {"red": 0, "green": 1, "blue": 2, "alpha": 3}
        color_index = value_names[input_id]

        if len(text) == 0:
            color_list = list(self.__configurator.roi_color)
            color_list[color_index] = 0
            self.__configurator.roi_color = (color_list[0], color_list[1], color_list[2], color_list[3])
            self.color_text_changed_signal.emit([str(clr) for clr in self.__configurator.roi_color])
            return

        value = int(text)
        value_clipped = clip(value, 0, 255)

        color_list = list(self.__configurator.roi_color)
        color_list[color_index] = value_clipped
        self.__configurator.roi_color = (color_list[0], color_list[1], color_list[2], color_list[3])

        if value != value_clipped:
            self.color_text_changed_signal.emit([str(clr) for clr in self.__configurator.roi_color])

    @Slot(str)  # type: ignore[arg-type]
    def delete_button_clicked(self, config_name: str) -> None:
        if config_name in ["region_of_interest", "transformation_points"]:
            points: tuple[int, str] = (
                int(self.__current_selected_point[REGION_OF_INTEREST]),
                str(self.__current_selected_point[TRANSFORMATION_POINTS]),
            )
            self.__configurator.delete_button_pressed(config_name, points)

    @Slot(str, str)  # type: ignore[arg-type]
    def arrow_button_clicked(self, config_name: str, direction: str) -> None:
        match config_name:
            case "Transformation Points":
                current_index = self.__transformation_points.index(
                    str(self.__current_selected_point[TRANSFORMATION_POINTS])
                )
                next_index = (current_index + 1 if direction == "right" else current_index - 1) % 4
                next_name = self.__transformation_points[next_index]
                self.__current_selected_point[TRANSFORMATION_POINTS] = next_name
                conf = self.__configurator.transformation_points[next_name]
                image_coords = conf["image"]
                real_coords = conf["real_world"]
                self.transformation_point_chosen_signal.emit(next_name)
                self.transformation_points_changed_signal.emit(
                    [image_coords[0], image_coords[1], real_coords[0], real_coords[1]]
                )
            case "Region of Interest":
                current_index = int(self.__current_selected_point[REGION_OF_INTEREST])
                to_modulo_with = len(self.__configurator.region_of_interest_points) + 1
                next_index = (current_index + 1 if direction == "right" else current_index - 1) % to_modulo_with
                self.__current_selected_point[REGION_OF_INTEREST] = next_index
                point_text = str(next_index)
                if next_index == to_modulo_with - 1:
                    point_text = "new"
                    image_coords, real_coords = (0, 0), (0.0, 0.0)
                else:
                    image_coords = self.__configurator.region_of_interest_points[
                        int(self.__current_selected_point[REGION_OF_INTEREST])
                    ]
                    real_coords = self.__configurator.get_real_world_point((image_coords[0], image_coords[1]))
                self.region_of_interest_point_chosen_signal.emit(point_text)
                self.region_of_interest_points_changed_signal.emit(
                    [image_coords[0], image_coords[1], real_coords[0], real_coords[1]]
                )

    @Slot(str)  # type: ignore[arg-type]
    def color_chooser_button_clicked(self, button_color: str) -> None:
        color: tuple[int, int, int, int] | None = None
        match button_color.lower():
            case "white":
                color = (255, 255, 255, 255)
            case "gray":
                color = (64, 64, 64, 192)
            case "black":
                color = (0, 0, 0, 255)
        if color:
            self.__configurator.roi_color = color
            self.color_text_changed_signal.emit([str(clr) for clr in color])

    @Slot(int, int, int, int)  # type: ignore[arg-type]
    def points_drawer_clicked(self, x: int, y: int, video_width: int, video_height: int) -> None:
        width_factor = 1332 / video_width
        height_factor = 990 / video_height
        x, y = int((x * width_factor)), int((y * height_factor))
        self.__configurator.configure_points((x, y))

    @Slot(int, int, int, int)  # type: ignore[arg-type]
    def points_shower_clicked(self, x: int, y: int, video_width: int, video_height: int) -> None:
        width_factor = 1332 / video_width
        height_factor = 990 / video_height
        x, y = int((x * width_factor)), int((y * height_factor))
        real_world = self.__configurator.get_real_world_point((x, y))
        self.real_world_points_changed_signal.emit([str(i) for i in [x, y, real_world[0], real_world[1]]])
