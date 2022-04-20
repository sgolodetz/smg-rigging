import numpy as np
import pygame

from typing import Optional, Sequence

from ..cameras.moveable_camera import MoveableCamera
from ..helpers.camera_pose_converter import CameraPoseConverter


class KeyboardCameraController:
    """A camera controller that moves the camera around based on keyboard input from the user."""

    # CONSTRUCTOR

    def __init__(self, camera: MoveableCamera, *, canonical_angular_speed: float = 0.03,
                 canonical_frame_time_ms: float = 16.0, canonical_linear_speed: float = 1.0, up=None):
        """
        Construct a keyboard camera controller.

        .. note::
            If the "up" direction is not explicitly specified, it will default to the up direction of the camera.

        :param camera:                  The camera to control.
        :param canonical_angular_speed: The desired angular speed (in radians) for the canonical frame time.
        :param canonical_frame_time_ms: The canonical frame time (in ms).
        :param canonical_linear_speed:  The desired linear speed for the canonical frame time.
        :param up:                      An optional "up" direction for rotations.
        """
        self.__camera = camera                                    # type: MoveableCamera
        self.__canonical_angular_speed = canonical_angular_speed  # type: float
        self.__canonical_frame_time_ms = canonical_frame_time_ms  # type: float
        self.__canonical_linear_speed = canonical_linear_speed    # type: float
        self.__prev_time_ms = None                                # type: Optional[float]

        if up is not None:
            self.__up = np.array(up, dtype=np.float64)            # type: np.ndarray
        else:
            self.__up = self.__camera.v()                         # type: np.ndarray

    # PUBLIC METHODS

    def get_camera(self) -> MoveableCamera:
        """
        Get the camera that is being controlled.

        :return:    The camera that is being controlled.
        """
        return self.__camera

    def get_pose(self) -> np.ndarray:
        """
        Get the pose of the camera that is being controlled.

        :return:    The pose of the camera that is being controlled.
        """
        return CameraPoseConverter.camera_to_pose(self.__camera)

    def update(self, pressed_keys: Sequence[bool], time_ms: float) -> None:
        """
        Move the camera around based on keyboard input from the user.

        :param pressed_keys:    The keys that are currently pressed.
        :param time_ms:         The current time (in ms).
        """
        # If this is the first occasion on which this function has been called, we can't calculate elapsed time yet,
        # so simply store the current time and return.
        if self.__prev_time_ms is None:
            self.__prev_time_ms = time_ms
            return

        # Calculate the time that has elapsed since this function was last called,
        # and scale the angular and linear speeds accordingly.
        scaling_factor = (time_ms - self.__prev_time_ms) / self.__canonical_frame_time_ms  # type: float
        angular_speed = self.__canonical_angular_speed * scaling_factor                    # type: float
        linear_speed = self.__canonical_linear_speed * scaling_factor                      # type: float
        self.__prev_time_ms = time_ms

        # Apply linear movements to the camera as needed.
        if pressed_keys[pygame.K_w]:
            self.__camera.move_n(linear_speed)
        if pressed_keys[pygame.K_s]:
            self.__camera.move_n(-linear_speed)
        if pressed_keys[pygame.K_d]:
            self.__camera.move_u(-linear_speed)
        if pressed_keys[pygame.K_a]:
            self.__camera.move_u(linear_speed)
        if pressed_keys[pygame.K_q] and not pressed_keys[pygame.K_LSHIFT]:
            self.__camera.move(self.__up, linear_speed)
        if pressed_keys[pygame.K_e] and not pressed_keys[pygame.K_LSHIFT]:
            self.__camera.move(self.__up, -linear_speed)

        # Apply angular movements to the camera as needed.
        if pressed_keys[pygame.K_RIGHT]:
            self.__camera.rotate(self.__up, -angular_speed)
        if pressed_keys[pygame.K_LEFT]:
            self.__camera.rotate(self.__up, angular_speed)
        if pressed_keys[pygame.K_UP]:
            self.__camera.rotate(self.__camera.u(), angular_speed)
        if pressed_keys[pygame.K_DOWN]:
            self.__camera.rotate(self.__camera.u(), -angular_speed)
        if pressed_keys[pygame.K_q] and pressed_keys[pygame.K_LSHIFT]:
            self.__camera.rotate(self.__camera.n(), -angular_speed)
        if pressed_keys[pygame.K_e] and pressed_keys[pygame.K_LSHIFT]:
            self.__camera.rotate(self.__camera.n(), angular_speed)

        # Allow the user to change the "up" direction used for rotations.
        if pressed_keys[pygame.K_g]:
            self.__up = self.__camera.v()
