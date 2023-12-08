"""The interface model for the configurator."""
# Copyright (C) 2023, NG:ITL

from PySide6.QtCore import QObject, Signal, Slot

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

        self.__active_mode: str = REGION_OF_INTEREST

    def update_ui_data(self, to_update: str) -> None:
        """Updates the data in the UI.

        Args:
            to_update (str): The name of the data to update.
        """
        current_point: int | str
        match to_update:
            case "Region of Interest":
                current_point = int(self.__configurator.current_selected_point[REGION_OF_INTEREST])
                current_data: tuple[int, int]
                real_points: tuple[float, float]
                if current_point == len(self.__configurator.region_of_interest_points):
                    current_data = (0, 0)
                    real_points = (0, 0)
                    self.region_of_interest_point_chosen_signal.emit("new")
                else:
                    current_data = self.__configurator.region_of_interest_points[current_point]
                    real_points = self.__configurator.get_real_world_point(current_data)
                data = [current_data[0], current_data[1], str(real_points[0]), str(real_points[1])]
                self.region_of_interest_points_changed_signal.emit(data)
            case "Transformation Points":
                current_point = str(self.__configurator.current_selected_point[TRANSFORMATION_POINTS])
                complete_data = self.__configurator.configured_transformation_points[current_point]
                image_coords = complete_data["image"]
                real_coords = complete_data["real"]
                data = [real_coords[0], real_coords[1], str(image_coords[0]), str(image_coords[1])]
                self.transformation_points_changed_signal.emit(data)

    @Slot(bool, bool, bool)  # type: ignore[arg-type]
    def updated_mode(self, roi_state: bool, t_point_state: bool, time_tracking_state: bool) -> None:
        """A function that is called from the frontend when the mode is changed.

        Args:
            roi_state (bool): Region of Interest active.
            t_point_state (bool): Transformation Points active.
            time_tracking_state (bool): Time Tracking active.
        """
        if roi_state:
            self.__active_mode = REGION_OF_INTEREST
        elif t_point_state:
            self.__active_mode = TRANSFORMATION_POINTS
        elif time_tracking_state:
            self.__active_mode = "Time Tracking"

    @Slot(str)  # type: ignore[arg-type]
    def config_button_pressed(self, button_text: str) -> None:
        """A function that is called from the frontend when a config button is pressed.

        Args:
            button_text (str): The text of the button that was pressed.
        """
        match button_text:
            case "Receive Config":
                self.__configurator.receive_config()
            case "Transmit Config":
                self.__configurator.send_config()

    @Slot(str, str, str)  # type: ignore[arg-type]
    def coordinate_text_changed(self, input_id: str, config_name: str, text: str) -> None:
        """A function that is called from the frontend when a coordinate text is changed.

        Args:
            input_id (str): The id of the input that was changed.
            config_name (str): The name of the config that was changed.
            text (str): The new text of the input.
        """
        is_image_coord = input_id.startswith("imagePoint")
        coord_index = 0 if input_id.endswith("XInput") else 1

        number = float(text) if len(text) > 0 else 0

        match config_name:
            case "Region of Interest":
                image_x, image_y, real_x, real_y = self.__configurator.roi_config_text_changed(
                    is_image_coord, coord_index, number
                )
                data = [real_x, real_y, str(image_x), str(image_y)]
                self.region_of_interest_points_changed_signal.emit(data)
            case "Transformation Points":
                self.__configurator.transformation_config_text_changed(is_image_coord, coord_index, number)

    @Slot(str, str)  # type: ignore[arg-type]
    def color_text_changed(self, input_id: str, text: str) -> None:
        """A function that is called from the frontend when a color text is changed.

        Args:
            input_id (str): The id of the input that was changed.
            text (str): The new text of the input.
        """
        color = self.__configurator.roi_color_changed(input_id, text)
        self.color_text_changed_signal.emit([int(i) for i in color])

    @Slot(str)  # type: ignore[arg-type]
    def delete_button_clicked(self, config_name: str) -> None:
        """A function that is called from the frontend when a delete button is clicked.

        Args:
            config_name (str): The name of the delete button that was pressed.
        """
        self.__configurator.delete_button_pressed(config_name)
        self.update_ui_data(config_name)

    @Slot(str, str)  # type: ignore[arg-type]
    def arrow_button_clicked(self, config_name: str, direction: str) -> None:
        """A function that is called from the frontend when an arrow button is clicked.

        Args:
            config_name (str): The name of the config that was changed.
            direction (str): The direction of the arrow button that was pressed.
        """
        if config_name == "button":
            config_name = self.__active_mode
        new_name, coords = self.__configurator.arrow_button_clicked(config_name, direction)
        match config_name:
            case "Region of Interest":
                self.region_of_interest_point_chosen_signal.emit(new_name)
                self.region_of_interest_points_changed_signal.emit(list(coords))
            case "Transformation Points":
                self.transformation_point_chosen_signal.emit(new_name)
                self.transformation_points_changed_signal.emit(list(coords))

    @Slot(str)  # type: ignore[arg-type]
    def color_chooser_button_clicked(self, button_color: str) -> None:
        """A function that is called from the frontend when a color chooser button is clicked.

        Args:
            button_color (str): The name of the color chooser button that was pressed.
        """
        color = self.__configurator.color_chooser_button(button_color)
        self.color_text_changed_signal.emit(list(color))

    @Slot(int, int, int, int, int, int)  # type: ignore[arg-type]
    def points_drawer_clicked(
        self, x: int, y: int, video_width: int, video_height: int, full_width: int, full_height: int
    ) -> None:
        """A function that is called from the frontend when the points drawer is clicked.

        Args:
            x (int): X coordinate of the click.
            y (int): Y coordinate of the click.
            video_width (int): The height of the displayed video.
            video_height (int): The width of the displayed video.
            full_width (int): The height of the video container.
            full_height (int): The width of the video container.
        """
        points = self.__configurator.points_drawer_clicked(
            self.__active_mode, (x, y), (video_width, video_height), (full_width, full_height)
        )
        match self.__active_mode:
            case "Region of Interest":
                self.region_of_interest_points_changed_signal.emit(list(points))
            case "Transformation Points":
                self.transformation_points_changed_signal.emit(list(points))

    @Slot(int, int, int, int, int, int)  # type: ignore[arg-type]
    def points_shower_clicked(
        self, x: int, y: int, video_width: int, video_height: int, full_width: int, full_height: int
    ) -> None:
        """A function that is called from the frontend when the points shower is clicked.

        Args:
            x (int): X coordinate of the click.
            y (int): Y coordinate of the click.
            video_width (int): The height of the displayed video.
            video_height (int): The width of the displayed video.
            full_width (int): The height of the video container.
            full_height (int): The width of the video container.
        """
        points = self.__configurator.points_shower_clicked(
            (x, y), (video_width, video_height), (full_width, full_height)
        )

        self.real_world_points_changed_signal.emit(list(points))
