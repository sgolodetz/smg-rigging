import numpy as np
import vg

from scipy.spatial.transform import Rotation

from .camera import Camera
from .moveable_camera import MoveableCamera


class SimpleCamera(MoveableCamera):
    """A simple, moveable camera in 3D space."""

    # CONSTRUCTOR

    def __init__(self, position, look, up):
        """
        Construct a simple camera.

        :param position:    The position of the camera.
        :param look:        A vector pointing in the direction faced by the camera.
        :param up:          The "up" direction for the camera.
        """
        self.__position: np.ndarray = np.array(position, dtype=np.float64)
        self.__n: np.ndarray = vg.normalize(np.array(look, dtype=np.float64))
        self.__v: np.ndarray = vg.normalize(np.array(up, dtype=np.float64))

        # Compute the camera's u axis from the up vector that was passed in and its n axis.
        self.__u: np.ndarray = vg.normalize(np.cross(self.__v, self.__n))

        # Compute the camera's v axis from its n and u axes.
        self.__v = vg.normalize(np.cross(self.__n, self.__u))

    # PUBLIC METHODS

    def move(self, direction: np.ndarray, delta: float) -> "SimpleCamera":
        """
        Move the camera by the specified displacement in the specified direction.

        :param direction:   The direction in which to move.
        :param delta:       The displacement by which to move.
        :return:            This camera, after it has been moved.
        """
        self.__position += delta * direction
        return self

    def move_n(self, delta: float) -> "SimpleCamera":
        """
        Move the camera by the specified displacement in the n direction.

        :param delta:   The displacement by which to move.
        :return:        This camera, after it has been moved.
        """
        self.__position += delta * self.__n
        return self

    def move_u(self, delta: float) -> "SimpleCamera":
        """
        Move the camera by the specified displacement in the u direction.

        :param delta:   The displacement by which to move.
        :return:        This camera, after it has been moved.
        """
        self.__position += delta * self.__u
        return self

    def move_v(self, delta: float) -> "SimpleCamera":
        """
        Move the camera by the specified displacement in the v direction.

        :param delta:   The displacement by which to move.
        :return:        This camera, after it has been moved.
        """
        self.__position += delta * self.__v
        return self

    def n(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing in the direction faced by the camera.

        :return:    A (normalised) vector pointing in the direction faced by the camera.
        """
        return self.__n

    def p(self) -> np.ndarray:
        """
        Get the position of the camera.

        :return:    The position of the camera.
        """
        return self.__position

    def rotate(self, axis, angle: float) -> "SimpleCamera":
        """
        Rotate the camera anti-clockwise by the specified angle about the specified axis.

        :param axis:    The axis about which to rotate.
        :param angle:   The angle by which to rotate (in radians).
        :return:        This camera, after it has been rotated.
        """
        r: np.ndarray = Rotation.from_rotvec(np.array(axis, dtype=np.float64) * angle).as_matrix()
        self.__n = r @ self.__n
        self.__u = r @ self.__u
        self.__v = r @ self.__v
        return self

    def set_from(self, rhs: Camera) -> "SimpleCamera":
        """
        Set the position and orientation of this camera to match those of another camera.

        :param rhs: The other camera.
        :return:    This camera, after it has been moved.
        """
        self.__position = rhs.p().copy()
        self.__n = rhs.n().copy()
        self.__u = rhs.u().copy()
        self.__v = rhs.v().copy()
        return self

    def u(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing to the left of the camera.

        :return:    A (normalised) vector pointing to the left of the camera.
        """
        return self.__u

    def v(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing to the top of the camera.

        :return:    A (normalised) vector pointing to the top of the camera.
        """
        return self.__v
