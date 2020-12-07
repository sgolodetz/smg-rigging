import numpy as np

from abc import ABC, abstractmethod


class Camera(ABC):
    """
    A camera in 3D space.

    Cameras are defined with a position and three mutually-orthogonal axes, namely n (points in the direction
    faced by the camera), u (points to the left of the camera) and v (points to the top of the camera).
    """

    # PUBLIC ABSTRACT METHODS

    @abstractmethod
    def n(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing in the direction faced by the camera.

        :return:    A (normalised) vector pointing in the direction faced by the camera.
        """
        pass

    @abstractmethod
    def p(self) -> np.ndarray:
        """
        Get the position of the camera.

        :return:    The position of the camera.
        """
        pass

    @abstractmethod
    def u(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing to the left of the camera.

        :return:    A (normalised) vector pointing to the left of the camera.
        """
        pass

    @abstractmethod
    def v(self) -> np.ndarray:
        """
        Get a (normalised) vector pointing to the top of the camera.

        :return:    A (normalised) vector pointing to the top of the camera.
        """
        pass
