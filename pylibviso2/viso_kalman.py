import numpy as np


class VisoKalman:
    def __init__(self):

        self.estimate = np.array([0.0, 0.0, 0.0])

        self.error_variance = np.ones_like(self.estimate)
        self.ones = np.ones_like(self.estimate)

        pstd = 4e-3
        cstd = 0.25
        self.Q = np.array([pstd, pstd, pstd])
        self.R = np.array([cstd, cstd, cstd])

    def process(self, x, y, z):
        measurement = np.array([x, y, z])

        prev_estimate = self.estimate
        prev_error_variance = self.error_variance + self.Q
        kalman_gain = prev_error_variance / (prev_error_variance + self.R)
        self.estimate = prev_estimate + kalman_gain * (measurement - prev_estimate)
        self.error_variance = (self.ones - kalman_gain) * prev_error_variance

        x, y, z = self.estimate.tolist()

        return x, y, z
