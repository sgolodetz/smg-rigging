import numpy as np


from .camera_pose_converter import CameraPoseConverter
from ..cameras.camera import Camera


class CameraUtil:
    """Utility functions related to cameras."""

    # PUBLIC STATIC METHODS

    @staticmethod
    def compute_look_rotation_c(cam1: Camera, cam2: Camera) -> float:
        """
        Compute the rotation (in degrees) between the look vectors of the two specified cameras.

        :param cam1:    The first camera.
        :param cam2:    The second camera.
        :return:        The rotation between the look vectors of the two cameras.
        """
        d: float = np.clip(np.dot(cam1.n(), cam2.n()), -1.0, 1.0)
        return np.rad2deg(np.arccos(d))

    @staticmethod
    def compute_look_rotation_p(pose1: np.ndarray, pose2: np.ndarray) -> float:
        """
        Compute the rotation (in degrees) between the look vectors of the two specified camera poses.

        :param pose1:   The first pose.
        :param pose2:   The second pose.
        :return:        The rotation between the look vectors of the two camera poses.
        """
        return CameraUtil.compute_look_rotation_c(
            CameraPoseConverter.pose_to_camera(pose1),
            CameraPoseConverter.pose_to_camera(pose2)
        )

    @staticmethod
    def compute_translation_c(cam1: Camera, cam2: Camera) -> float:
        """
        Compute the translation between the two specified cameras (i.e. the distance between their positions).

        :param cam1:    The first camera.
        :param cam2:    The second camera.
        :return:        The translation between the two cameras.
        """
        return np.linalg.norm(cam1.p() - cam2.p())

    @staticmethod
    def compute_translation_p(pose1: np.ndarray, pose2: np.ndarray) -> float:
        """
        Compute the translation between the two specified camera poses (i.e. the distance between their positions).

        :param pose1:   The first pose.
        :param pose2:   The second pose.
        :return:        The translation between the two camera poses.
        """
        return CameraUtil.compute_translation_c(
            CameraPoseConverter.pose_to_camera(pose1),
            CameraPoseConverter.pose_to_camera(pose2)
        )
