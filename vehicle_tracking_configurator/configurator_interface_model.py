from PySide6.QtCore import QObject, Signal, Property
from typing import List
from time import sleep
import pynng
import pynng.exceptions
import json

class ModelVehicleTrackingConfigurator(QObject):
    def __init__(self) -> None:
        QObject.__init__(self)

    @Signal
    def reloadImage(self) -> None:
        pass
