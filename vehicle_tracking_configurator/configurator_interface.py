"""Starting the QT application."""
# Copyright (C) 2023, NG:ITL

from pathlib import Path
from json import load
import sys

from PySide6.QtGui import QGuiApplication, QImage
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Qt, QSize, QSocketNotifier
from PySide6.QtQuick import QQuickImageProvider
from pathlib import Path
from json import load
import pynng

from vehicle_tracking_configurator.configurator_interface_model import ModelVehicleTrackingConfigurator


def find_base_directory() -> Path:
    """Find the base directory of the project."""
    search_paths = {
        Path().cwd(),
        Path().cwd().parent,
        Path(__file__).parent.parent
    }
    for directory in search_paths:
        if (directory / "vehicle_tracking_configurator_config.json").exists():
            return directory
    sys.exit(1)


class StreamImageProvider(QQuickImageProvider):
    def __init__(self, width: int, height: int) -> None:
        super(StreamImageProvider, self).__init__(QQuickImageProvider.Image) # type: ignore
        self.img = QImage(width, height, QImage.Format_RGB888) # type: ignore

    def requestImage(self, id: str, size: QSize, requested_size: QSize) -> QImage:
        if requested_size.width() > 0 and requested_size.height() > 0:
            return self.img.scaled(requested_size, Qt.KeepAspectRatio) # type: ignore
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

        self.vehicle_tracking_configurator_model = ModelVehicleTrackingConfigurator()

        self.frames_receiver = pynng.Sub0(dial=self.__recv_frames_address)
        self.frames_receiver.subscribe("")

        self.point_drawer_image_provider = StreamImageProvider(1332, 990)

        self.__engine.addImageProvider("point_drawer", self.point_drawer_image_provider)

        self.__engine.rootContext().setContextProperty("configurator_interface", self)
        self.__engine.rootContext().setContextProperty("vehicle_tracking_configurator_model", self.vehicle_tracking_configurator_model)

        self.__engine.load(str(base_dir / "frontend/qml/main.qml"))

        self.__point_drawer_socket_notifier = QSocketNotifier(self.frames_receiver.recv_fd, QSocketNotifier.Read) # type: ignore
        self.__point_drawer_socket_notifier.activated.connect(self.image_receiver_callback)

        self.image_count = 0


    def image_receiver_callback(self) -> None:
        data = self.frames_receiver.recv()
        self.point_drawer_image_provider.img = QImage(data, 1332, 990, QImage.Format_BGR888) # type: ignore
        self.vehicle_tracking_configurator_model.reloadImage.emit()

    def run(self) -> None:
        """Run the QT application."""
        self.__app.exec_()
