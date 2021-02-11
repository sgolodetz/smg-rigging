import numpy as np

from abc import ABC, abstractmethod

from .camera import Camera


class MoveableCamera(Camera, ABC):
    """A moveable camera in 3D space."""

    # PUBLIC ABSTRACT METHODS

    @abstractmethod
    def move(self, direction: np.ndarray, delta: float) -> "MoveableCamera":
        """
        Move the camera by the specified displacement in the specified direction.
        :param direction:   The direction in which to move.
        :param delta:       The displacement by which to move.
        :return:            This camera, after it has been moved.
        """
        pass

    @abstractmethod
    def move_n(self, delta: float) -> "MoveableCamera":
        """
        Move the camera by the specified displacement in the n direction.

        :param delta:   The displacement by which to move.
        :return:        This camera, after it has been moved.
        """
        pass

    @abstractmethod
    def move_u(self, delta: float) -> "MoveableCamera":
        """
        Move the camera by the specified displacement in the u direction.

        :param delta:   The displacement by which to move.
        :return:        This camera, after it has been moved.
        """
        pass

    @abstractmethod
    def move_v(self, delta: float) -> "MoveableCamera":
        """
        Move the camera by the specified displacement in the v direction.

        :param delta:   The displacement by which to move.
        :return:        This camera, after it has been moved.
        """
        pass

    @abstractmethod
    def rotate(self, axis, angle: float) -> "MoveableCamera":
        """
        Rotate the camera anti-clockwise by the specified angle about the specified axis.

        :param axis:    The axis about which to rotate.
        :param angle:   The angle by which to rotate (in radians).
        :return:        This camera, after it has been rotated.
        """
        pass

    @abstractmethod
    def set_from(self, rhs: Camera) -> "MoveableCamera":
        """
        Set the position and orientation of this camera to match those of another camera.

        :param rhs: The other camera.
        :return:    This camera, after it has been moved.
        """
        pass
