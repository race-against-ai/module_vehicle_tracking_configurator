"""Starting the QT application."""
# Copyright (C) 2023, NG:ITL

from threading import Thread, Event
from pathlib import Path
from json import load, dump

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QGuiApplication, QImage
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickImageProvider
from jsonschema import validate
import pynng

from vehicle_tracking_configurator.configurator_interface_model import ModelVehicleTrackingConfigurator
from vehicle_tracking_configurator.configurator import ConfiguratorHandler


FILE_DIR = Path(__file__).parent
BASE_DIR = FILE_DIR.parent
CONFIG_FILE_PATH = "./vehicle_tracking_configurator_config.json"


class StreamImageProvider(QQuickImageProvider):
    """A class for providing images to the UI.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.
    """

    def __init__(self, width: int, height: int) -> None:
        super().__init__(QQuickImageProvider.Image)  # type: ignore[attr-defined]
        self.img = QImage(width, height, QImage.Format_RGB888)  # type: ignore[attr-defined]

    def requestImage(self, frame_id: str, size: QSize, requested_size: QSize) -> QImage:
        """Scales image to the requested size.

        Args:
            frame_id (str): The frame number.
            size (QSize): The size of the image.
            requested_size (QSize): The requested size of the image.

        Returns:
            QImage: The scaled image.
        """
        del frame_id, size
        if requested_size.width() > 0 and requested_size.height() > 0:
            return self.img.scaled(requested_size, Qt.KeepAspectRatio)  # type: ignore[attr-defined]
        return self.img


class ConfiguratorInterface:
    """A class for starting the QT application."""

    def __init__(self) -> None:
        config_schema: dict = {}
        with open(FILE_DIR / "schemas/configurator_config.json", "r", encoding="utf-8") as schema_file:
            config_schema = load(schema_file)

        if not Path(CONFIG_FILE_PATH).exists():
            with open(CONFIG_FILE_PATH, "x", encoding="utf-8") as config_file, open(
                FILE_DIR / "templates/configurator_config.json", "r", encoding="utf-8"
            ) as template_file:
                dump(load(template_file), config_file, indent=4)

        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_file:
            conf = load(config_file)
            validate(instance=conf, schema=config_schema)
            self.__recv_frames_address = conf["pynng"]["subscribers"]["camera_frame_receiver"]["address"]

        self.__app = QGuiApplication()
        self.__engine = QQmlApplicationEngine()
        self.__configuration_handler = ConfiguratorHandler()

        self.__vehicle_tracking_configurator_model = ModelVehicleTrackingConfigurator(self.__configuration_handler)

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

        self.__engine.load(BASE_DIR / "vehicle_tracking_configurator/frontend/qml/main.qml")

        self.image_count = 0

        self.__stop_thread_event = Event()
        self.__send_next_images_thread = Thread(target=self.__transmit_images_from_backend_to_frontend_worker)
        self.__send_next_images_thread.start()

    def __transmit_images_from_backend_to_frontend_worker(self) -> None:
        """A function that constantly sends new images to the UI."""
        while not self.__stop_thread_event.is_set():
            drawer_frame = self.__configuration_handler.read_drawer_frame()
            shower_frame = self.__configuration_handler.read_shower_frame()

            self.__point_drawer_image_provider.img = QImage(drawer_frame, 1332, 990, QImage.Format_BGR888)  # type: ignore[attr-defined]
            self.__point_shower_image_provider.img = QImage(shower_frame, 1332, 990, QImage.Format_BGR888)  # type: ignore[attr-defined]

            self.__vehicle_tracking_configurator_model.reload_image.emit()

    def run(self) -> None:
        """Run the QT application."""
        self.__app.exec_()
        self.__stop_thread_event.set()
        self.__send_next_images_thread.join()
