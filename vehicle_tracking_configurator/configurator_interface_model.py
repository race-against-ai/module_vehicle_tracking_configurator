# Copyright (C) 2023, NG:ITL

from PySide6.QtCore import QObject, Signal, Property, Slot


class ModelVehicleTrackingConfigurator(QObject):
    def __init__(self) -> None:
        QObject.__init__(self)

    reload_image = Signal(name="reloadImage")

    @Slot(bool, bool, bool)  # type: ignore[arg-type]
    def updated_mode(self, roi_state: bool, t_point_state: bool, world_state: bool) -> None:
        print(f"roi_state: {roi_state}\n t_point_state: {t_point_state}\n world_state: {world_state}\n")

    @Slot(str)  # type: ignore[arg-type]
    def config_button_pressed(self, button_text: str) -> None:
        print("backend", button_text)

    @Slot(str, str, str)  # type: ignore[arg-type]
    def coordinate_text_changed(self, input_id: str, config_name: str, text: str) -> None:
        print("backend", input_id, config_name, text)

    @Slot(str, str)  # type: ignore[arg-type]
    def color_text_changed(self, input_id: str, text: str) -> None:
        print("backend", input_id, text)

    @Slot(str)  # type: ignore[arg-type]
    def delete_button_clicked(self, config_name: str) -> None:
        print("backend", config_name)

    @Slot(str, str)  # type: ignore[arg-type]
    def arrow_button_clicked(self, config_name: str, direction: str) -> None:
        print("backend", config_name, direction)

    @Slot(str)  # type: ignore[arg-type]
    def color_chooser_button_clicked(self, button_color: str) -> None:
        print("backend", button_color)

    @Slot(int, int)  # type: ignore[arg-type]
    def points_shower_clicked(self, x: int, y: int) -> None:
        print("backend", x, y)

    @Slot(int, int)  # type: ignore[arg-type]
    def points_drawer_clicked(self, x: int, y: int) -> None:
        print("backend", x, y)
