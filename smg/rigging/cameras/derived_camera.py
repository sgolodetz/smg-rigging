import numpy as np

from .camera import Camera


class DerivedCamera(Camera):
    """A camera whose position and orientation are based on those of another camera."""

    # CONSTRUCTOR

    def __init__(self, base_camera: Camera, rot: np.ndarray, trans):
        """
        Construct a derived camera.

        :param base_camera: The camera on which this derived camera is based.
        :param rot:         The *camera-space* (u-v-n) rotation from the base camera's axes to those of the
                            derived camera.
        :param trans:       The *camera-space* (u-v-n) translation from the base camera's axes to those of the
                            derived camera.
        """
        self.__base_camera = base_camera                  # type: Camera
        self.__rot = rot                                  # type: np.ndarray
        self.__trans = np.array(trans, dtype=np.float64)  # type: np.ndarray

    # PUBLIC METHODS

    def n(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing in the direction faced by the camera.

        :return:    A (normalised) vector pointing in the direction faced by the camera.
        """
        return self.__make_world_space_rotation() @ self.__base_camera.n()

    def p(self) -> np.ndarray:
        """
        Get the position of the camera.

        :return:    The position of the camera.
        """
        return self.__base_camera.p() + \
            self.__trans[0] * self.__base_camera.u() + \
            self.__trans[1] * self.__base_camera.v() + \
            self.__trans[2] * self.__base_camera.n()

    def u(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing to the left of the camera.

        :return:    A (normalised) vector pointing to the left of the camera.
        """
        return self.__make_world_space_rotation() @ self.__base_camera.u()

    def v(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing to the top of the camera.

        :return:    A (normalised) vector pointing to the top of the camera.
        """
        return self.__make_world_space_rotation() @ self.__base_camera.v()

    # PRIVATE METHODS

    def __make_world_space_rotation(self) -> np.ndarray:
        """
        Make the world-space rotation corresponding to the camera-space rotation we're using.

        :return:    The world-space rotation corresponding to the camera-space rotation we're using.
        """
        # Construct a matrix that can transform (free) vectors from camera space into world space.
        # For example, m * (1,0,0)^T = u.
        m = np.column_stack(
            (self.__base_camera.u(), self.__base_camera.v(), self.__base_camera.n())
        )  # type: np.ndarray

        # Use it to turn our camera-space rotation matrix into a world-space one.
        return m @ self.__rot @ np.linalg.inv(m)
