import numpy as np

from typing import Dict, Optional

from .camera import Camera
from .moveable_camera import MoveableCamera
from .simple_camera import SimpleCamera


class CompositeCamera(MoveableCamera):
    """
    A 'composite' camera (i.e. a camera rig) consisting of several other cameras.

    A composite camera consists of a single primary camera that controls the position and orientation of the composite,
    and a number of secondary cameras that are generally directly or indirectly based on that camera.
    """

    # CONSTRUCTOR

    def __init__(self, position, look, up):
        """
        Construct a composite camera.

        :param position:    The position of the camera.
        :param look:        A vector pointing in the direction faced by the camera.
        :param up:          The "up" direction for the camera.
        """
        self.__primary_camera = SimpleCamera(position, look, up)  # type: SimpleCamera
        self.__secondary_cameras = {}  # type: Dict[str, Camera]

    # PUBLIC METHODS

    def add_secondary_camera(self, name: str, camera: Camera) -> None:
        """
        Add a secondary camera to the composite.

        :param name:            The name to give the secondary camera.
        :param camera:          The secondary camera.
        :raises RuntimeError:   If the composite already contains a camera with the specified name.
        """
        if self.__secondary_cameras.get(name) is None:
            self.__secondary_cameras[name] = camera
        else:
            # raise RuntimeError(f"The composite already contains a camera named '{name}'")
            raise RuntimeError("The composite already contains a camera named '{}'".format(name))

    def get_secondary_camera(self, name: str) -> Camera:
        """
        Get the secondary camera with the specified name.

        :param name:            The name of the secondary camera to get.
        :return:                The secondary camera with the specified name, if it exists.
        :raises RuntimeError:   If the composite does not contain a camera with the specified name.
        """
        camera = self.__secondary_cameras.get(name)  # type: Optional[Camera]
        if camera is not None:
            return camera
        else:
            raise RuntimeError("The composite does not contain a camera named '{}'".format(name))

    def get_secondary_cameras(self) -> Dict[str, Camera]:
        """
        Get all the secondary cameras in the composite.

        :return:    The secondary cameras in the composite.
        """
        return self.__secondary_cameras

    # noinspection PyUnresolvedReferences
    def move(self, direction: np.ndarray, delta: float) -> "CompositeCamera":
        """
        Move the camera by the specified displacement in the specified direction.

        :param direction:   The direction in which to move.
        :param delta:       The displacement by which to move.
        :return:            This camera, after it has been moved.
        """
        self.__primary_camera.move(direction, delta)
        return self

    # noinspection PyUnresolvedReferences
    def move_n(self, delta: float) -> "CompositeCamera":
        """
        Move the camera by the specified displacement in the n direction.

        :param delta:   The displacement by which to move.
        :return:        This camera, after it has been moved.
        """
        self.__primary_camera.move_n(delta)
        return self

    # noinspection PyUnresolvedReferences
    def move_u(self, delta: float) -> "CompositeCamera":
        """
        Move the camera by the specified displacement in the u direction.

        :param delta:   The displacement by which to move.
        :return:        This camera, after it has been moved.
        """
        self.__primary_camera.move_u(delta)
        return self

    # noinspection PyUnresolvedReferences
    def move_v(self, delta: float) -> "CompositeCamera":
        """
        Move the camera by the specified displacement in the v direction.

        :param delta:   The displacement by which to move.
        :return:        This camera, after it has been moved.
        """
        self.__primary_camera.move_v(delta)
        return self

    def n(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing in the direction faced by the camera.

        :return:    A (normalised) vector pointing in the direction faced by the camera.
        """
        return self.__primary_camera.n()

    def p(self) -> np.ndarray:
        """
        Get the position of the camera.

        :return:    The position of the camera.
        """
        return self.__primary_camera.p()

    def remove_secondary_camera(self, name: str) -> None:
        """
        Remove the secondary camera with the specified name from the composite.

        :param name:            The name of the camera to remove.
        :raises RuntimeError:   If the composite does not contain a camera with the specified name.
        """
        if self.__secondary_cameras.get(name) is not None:
            del self.__secondary_cameras[name]
        else:
            raise RuntimeError("The composite does not contain a camera named '{}'".format(name))

    # noinspection PyUnresolvedReferences
    def rotate(self, axis, angle: float) -> "CompositeCamera":
        """
        Rotate the camera anti-clockwise by the specified angle about the specified axis.

        :param axis:    The axis about which to rotate.
        :param angle:   The angle by which to rotate (in radians).
        :return:        This camera, after it has been rotated.
        """
        self.__primary_camera.rotate(axis, angle)
        return self

    # noinspection PyUnresolvedReferences
    def set_from(self, rhs: Camera) -> "CompositeCamera":
        """
        Set the position and orientation of this camera to match those of another camera.

        :param rhs: The other camera.
        :return:    This camera, after it has been moved.
        """
        self.__primary_camera.set_from(rhs)
        return self

    def u(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing to the left of the camera.

        :return:    A (normalised) vector pointing to the left of the camera.
        """
        return self.__primary_camera.u()

    def v(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing to the top of the camera.

        :return:    A (normalised) vector pointing to the top of the camera.
        """
        return self.__primary_camera.v()
