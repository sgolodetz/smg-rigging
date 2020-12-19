import numpy as np

from ...rigging.cameras import Camera, SimpleCamera


class CameraPoseConverter:
    """Helper functions to convert between cameras, pose matrices and model-view matrices."""

    # PUBLIC STATIC METHODS

    @staticmethod
    def camera_to_pose(camera: Camera) -> np.ndarray:
        """
        Convert a camera to a pose matrix.

        :param camera:  The camera.
        :return:        The pose matrix of the camera.
        """
        # See the corresponding function in SemanticPaint for an explanation, if one is needed.
        n, p, u, v = camera.n(), camera.p(), camera.u(), camera.v()
        pose: np.ndarray = np.eye(4)
        pose[0:3, 0:3] = np.vstack((-u, -v, n))
        pose[0:3, 3] = [p.dot(u), p.dot(v), -p.dot(n)]
        return pose

    @staticmethod
    def pose_to_camera(pose: np.ndarray) -> SimpleCamera:
        """
        Convert a pose matrix to a camera.

        :param pose:    The pose matrix.
        :return:        A camera with the specified pose.
        """
        # See the corresponding function in SemanticPaint for an explanation, if one is needed.
        inv_pose: np.ndarray = np.linalg.inv(pose)
        return SimpleCamera(inv_pose[0:3, 3], inv_pose[0:3, 2], inv_pose[0:3, 1])

    @staticmethod
    def pose_to_modelview(pose: np.ndarray) -> np.ndarray:
        """
        Convert a pose matrix to a model-view matrix.

        :param pose:    The pose matrix.
        :return:        The model-view matrix.
        """
        m: np.ndarray = pose.copy()
        m[1:3, :] *= -1
        return m
