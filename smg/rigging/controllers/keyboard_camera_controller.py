import numpy as np
import pygame

from typing import Optional

from smg.rigging.cameras.moveable_camera import MoveableCamera


class KeyboardCameraController:
    """TODO"""

    def __init__(self, camera: MoveableCamera, up, *, angular_speed: float = 0.03,
                 canonical_frame_time_ms: float = 16.0, linear_speed: float = 1.0):
        """
        Construct a camera controller.

        :param camera:                  The camera to control.
        :param up:                      TODO
        :param angular_speed:           TODO
        :param canonical_frame_time_ms: TODO
        :param linear_speed:            TODO
        """
        self.__angular_speed: float = angular_speed
        self.__camera: MoveableCamera = camera
        self.__canonical_frame_time_ms: float = canonical_frame_time_ms
        self.__linear_speed: float = linear_speed
        self.__prev_time_ms: Optional[float] = None
        self.__up: np.ndarray = np.array(up, dtype=np.float64)

    def __call__(self, pressed_keys, time_ms: float) -> None:
        # TODO
        if self.__prev_time_ms is None:
            self.__prev_time_ms = time_ms
            return

        # TODO
        scaling_factor: float = (time_ms - self.__prev_time_ms) / self.__canonical_frame_time_ms
        self.__prev_time_ms = time_ms

        # TODO
        angular_speed: float = self.__angular_speed * scaling_factor
        linear_speed: float = self.__linear_speed * scaling_factor

        # TODO
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

        # TODO
        if pressed_keys[pygame.K_RIGHT]:
            self.__camera.rotate(self.__up, -angular_speed)
        if pressed_keys[pygame.K_LEFT]:
            self.__camera.rotate(self.__up, angular_speed)
        if pressed_keys[pygame.K_UP]:
            self.__camera.rotate(self.__camera.u(), angular_speed)
        if pressed_keys[pygame.K_DOWN]:
            self.__camera.rotate(self.__camera.u(), -angular_speed)
