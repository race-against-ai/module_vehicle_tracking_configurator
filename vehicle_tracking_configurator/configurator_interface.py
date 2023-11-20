"""Starting the QT application."""
# Copyright (C) 2023, NG:ITL

from threading import Thread, Event
from pathlib import Path
from json import load
import sys

from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtGui import QGuiApplication, QImage
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickImageProvider
import pynng

from vehicle_tracking_configurator.configurator_interface_model import ModelVehicleTrackingConfigurator
from vehicle_tracking_configurator.configurator import ConfiguratorHandler


def find_base_directory() -> Path:
    """Find the base directory of the project."""
    search_paths = {Path().cwd(), Path().cwd().parent, Path(__file__).parent.parent}
    for directory in search_paths:
        if (directory / "vehicle_tracking_configurator_config.json").exists():
            return directory
    sys.exit(1)


class StreamImageProvider(QQuickImageProvider):
    def __init__(self, width: int, height: int) -> None:
        super(StreamImageProvider, self).__init__(QQuickImageProvider.Image)  # type: ignore[attr-defined]
        self.img = QImage(width, height, QImage.Format_RGB888)  # type: ignore[attr-defined]

    def requestImage(self, id: str, size: QSize, requested_size: QSize) -> QImage:
        if requested_size.width() > 0 and requested_size.height() > 0:
            return self.img.scaled(requested_size, Qt.KeepAspectRatio)  # type: ignore[attr-defined]
        else:
            return self.img


class ConfiguratorInterface:
    """A class for starting the QT application."""

    def __init__(self) -> None:
        base_dir = find_base_directory()

        with open(base_dir / "vehicle_tracking_configurator_config.json", "r") as config_file:
            conf = load(config_file)
            self.__recv_frames_address = conf["pynng"]["subscribers"]["camera_frame_receiver"]["address"]

        self.__app = QGuiApplication()
        self.__engine = QQmlApplicationEngine()
        self.__configuration_handler = ConfiguratorHandler()

        self.__vehicle_tracking_configurator_model = ModelVehicleTrackingConfigurator()

        self.__frames_receiver = pynng.Sub0(dial=self.__recv_frames_address, block_on_dial=False)
        self.__frames_receiver.subscribe("")

        self.__point_drawer_image_provider = StreamImageProvider(1332, 990)
        self.__point_shower_image_provider = StreamImageProvider(1332, 990)

        self.__engine.addImageProvider("point_drawer", self.__point_drawer_image_provider)
        self.__engine.addImageProvider("point_shower", self.__point_shower_image_provider)

        self.__engine.rootContext().setContextProperty("configurator_interface", self)
        self.__engine.rootContext().setContextProperty(
            "vehicle_tracking_configurator_model", self.__vehicle_tracking_configurator_model
        )

        self.__engine.load(str(base_dir / "frontend/qml/main.qml"))

        self.image_count = 0

        self.__stop_thread_event = Event()
        self.__send_next_images_thread = Thread(target=self.__send_next_images_worker)
        self.__send_next_images_thread.start()

    def __send_next_images_worker(self) -> None:
        """A function that constantly sends new images to the UI."""
        while not self.__stop_thread_event.is_set():
            drawer_frame = self.__configuration_handler.read_drawer_frame()
            shower_frame = self.__configuration_handler.read_shower_frame()

            self.__point_drawer_image_provider.img = QImage(drawer_frame, 1332, 990, QImage.Format_BGR888)  # type: ignore[attr-defined]
            self.__point_shower_image_provider.img = QImage(shower_frame, 1332, 990, QImage.Format_BGR888)  # type: ignore[attr-defined]

            self.__vehicle_tracking_configurator_model.reload_image.emit()

    @Slot(str)
    def on_text_changed(self, new_text):
        print(f"Text changed: {new_text}")

    def run(self) -> None:
        """Run the QT application."""
        self.__app.exec_()
        self.__stop_thread_event.set()
        self.__send_next_images_thread.join()
