import numpy as np
import pygame

from typing import Optional

from smg.rigging.cameras.moveable_camera import MoveableCamera


class KeyboardCameraController:
    """A camera controller that moves the camera around based on keyboard input from the user."""

    def __init__(self, camera: MoveableCamera, up, *, canonical_angular_speed: float = 0.03,
                 canonical_frame_time_ms: float = 16.0, canonical_linear_speed: float = 1.0):
        """
        Construct a keyboard camera controller.

        :param camera:                  The camera to control.
        :param up:                      The "up" direction for the camera.
        :param canonical_angular_speed: The desired angular speed (in radians) for the canonical frame time.
        :param canonical_frame_time_ms: The canonical frame time (in ms).
        :param canonical_linear_speed:  The desired linear speed for the canonical frame time.
        """
        self.__camera: MoveableCamera = camera
        self.__canonical_angular_speed: float = canonical_angular_speed
        self.__canonical_frame_time_ms: float = canonical_frame_time_ms
        self.__canonical_linear_speed: float = canonical_linear_speed
        self.__prev_time_ms: Optional[float] = None
        self.__up: np.ndarray = np.array(up, dtype=np.float64)

    def __call__(self, pressed_keys, time_ms: float) -> None:
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
        scaling_factor: float = (time_ms - self.__prev_time_ms) / self.__canonical_frame_time_ms
        angular_speed: float = self.__canonical_angular_speed * scaling_factor
        linear_speed: float = self.__canonical_linear_speed * scaling_factor
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
        if pressed_keys[pygame.K_q]:
            self.__camera.move(self.__up, linear_speed)
        if pressed_keys[pygame.K_e]:
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
