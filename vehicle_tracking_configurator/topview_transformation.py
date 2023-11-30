"""This module contains the TopViewTransformation class which is used to transform a point from the camera image to coordinates in meters in the real world.ye"""
# Copyright (C) 2023, NG:ITL
from typing import NamedTuple
import numpy as np
import cv2


class TransformationPoint(NamedTuple):
    """A point in the camera image and the corresponding point in the world coordinate system.

    Args:
        camera_image_point (tuple[int, int]): The point in the camera image.
        world_coordinate_point (tuple[float, float]): The corresponding point in the real world.
    """

    camera_image_point: tuple[int, int]
    world_coordinate_point: tuple[float, float]


class TopViewTransformation:
    """A class that transforms a point from the camera image to coordinates in meters in the real world."""

    def __init__(
        self,
        transformation_points: dict[str, TransformationPoint],
    ) -> None:
        """Constructor for the TopViewTransformation class.

        Args:
            transformation_points (dict[str, TransformationPoint]): The points used to define the transformation.
        """
        self.define_transformation_points(transformation_points)

    def define_transformation_points(self, transformation_points: dict[str, TransformationPoint]) -> None:
        """Defines the points used to define the transformation.

        Args:
            transformation_points (dict[str, TransformationPoint]): The points used to define the transformation.
        """
        camera_image_pts = np.array(
            [
                list(transformation_points["top_left"].camera_image_point),
                list(transformation_points["bottom_left"].camera_image_point),
                list(transformation_points["top_right"].camera_image_point),
                list(transformation_points["bottom_right"].camera_image_point),
            ],
            dtype=np.float32,
        )

        world_coordinate_system_pts = np.array(
            [
                list(transformation_points["top_left"].world_coordinate_point),
                list(transformation_points["bottom_left"].world_coordinate_point),
                list(transformation_points["top_right"].world_coordinate_point),
                list(transformation_points["bottom_right"].world_coordinate_point),
            ],
            dtype=np.float32,
        )

        self.camera_to_world_transformation_matrix = cv2.getPerspectiveTransform(
            camera_image_pts, world_coordinate_system_pts
        )

    def transform_camera_point_to_world_coordinate(self, camera_point: tuple[int, int]) -> tuple[float, float]:
        """Transforms a point from the camera image to coordinates in meters in the real world."""
        point = np.array([list(camera_point)], dtype=np.float32)
        return cv2.perspectiveTransform(point[None, :, :], self.camera_to_world_transformation_matrix)

    # TODO: To be tested
    # !: Untested and should not be used in Production
    def transform_world_coordinate_to_camera_point(self, world_coordinate: tuple[float, float]) -> tuple[int, int]:
        """Transforms a point from coordinates in meters in the real world to the camera image."""
        point = np.array([list(world_coordinate)], dtype=np.float32)
        return cv2.perspectiveTransform(point[None, :, :], self.camera_to_world_transformation_matrix)[0][0]
