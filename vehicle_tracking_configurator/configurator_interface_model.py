# Copyright (C) 2023, NG:ITL

from PySide6.QtCore import QObject, Signal, Property


class ModelVehicleTrackingConfigurator(QObject):
    def __init__(self) -> None:
        QObject.__init__(self)

    @Signal  # type: ignore
    def reloadImage(self) -> None:
        pass
