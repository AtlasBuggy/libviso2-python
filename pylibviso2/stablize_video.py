import cv2
import numpy as np

lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict(maxCorners=100,
                      qualityLevel=0.01,
                      minDistance=7,
                      blockSize=7)


class Stablizer:
    def __init__(self):
        self.good_features_p0 = None
        self.prev_image = None

        self.reset()

        self.image_num = 0

    def reset(self):
        self.x = 0.0
        self.y = 0.0
        self.a = 0.0

        self.estimate = np.array([self.x, self.y, self.a])
        self.error_variance = np.ones_like(self.estimate)
        self.ones = np.ones_like(self.estimate)

        pstd = 4e-3
        cstd = 0.25
        self.Q = np.array([pstd, pstd, pstd])
        self.R = np.array([cstd, cstd, cstd])

    def compute_transform(self, prev_corners, current_corners):
        transform = cv2.estimateRigidTransform(prev_corners, current_corners, False)

        dx = transform[0, 2]
        dy = transform[1, 2]
        da = np.arctan2(transform[1, 0], transform[0, 0])

        return transform, dx, dy, da

    def filter_transform(self, x, y, a):
        measurement = np.array([self.x, self.y, self.a])

        prev_estimate = self.estimate
        prev_error_variance = self.error_variance + self.Q
        kalman_gain = prev_error_variance / (prev_error_variance + self.R)
        self.estimate = prev_estimate + kalman_gain * (measurement - prev_estimate)
        self.error_variance = (self.ones - kalman_gain) * prev_error_variance

        return self.estimate

    def compute_good_features(self, image):
        return cv2.goodFeaturesToTrack(image, mask=None, **feature_params)

    def first_iteration(self, image):
        self.good_features_p0 = self.compute_good_features(image)
        self.prev_image = image

    def process(self, image):
        if self.image_num == 0:
            self.first_iteration(image)
        else:
            self.good_features_p1, st, err = \
                cv2.calcOpticalFlowPyrLK(self.prev_image, image, self.good_features_p0, None, **lk_params)

            if st is None or len(self.good_features_p1) < 20:
                self.first_iteration(image)
                self.reset()
                return image

            good_new = self.good_features_p1[st == 1]
            good_old = self.good_features_p0[st == 1]

            self.good_features_p0 = good_new.reshape(-1, 1, 2)

            self.prev_image = image

            transform, dx, dy, da = self.compute_transform(good_old, good_new)
            self.x += dx
            self.y += dy
            self.a += da

            estimate = self.filter_transform(self.x, self.y, self.a)

            error_x = estimate[0] - self.x
            error_y = estimate[1] - self.y
            error_a = estimate[2] - self.a

            dx += error_x
            dy += error_y
            da += error_a

            transform[0, 0] = np.cos(da)
            transform[0, 1] = -np.sin(da)
            transform[1, 0] = np.sin(da)
            transform[1, 1] = np.cos(da)

            transform[0, 2] = dx
            transform[1, 2] = dy

            height, width = image.shape[0:2]
            image = cv2.warpAffine(image, transform, (width, height))

            for point in good_new:
                x, y = point.ravel()
                cv2.circle(image, (x, y), 2, (255, 255, 255))

        self.image_num += 1

        return image
