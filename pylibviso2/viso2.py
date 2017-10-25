import cv2
import numpy as np

from .pylibviso2 import *


class Viso2Mono:
    def __init__(self, f, cu, cv, width=None, height=None):
        param = mono_parameters()
        param.calib.f = f
        param.calib.cu = cu
        param.calib.cv = cv
        self.visual_odom_mono = VisualOdometryMono(param)

        self.width = width
        self.height = height

        self.pose = None
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        self.prev_x = 0.0
        self.prev_y = 0.0
        self.prev_z = 0.0

    def update(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.width is None or self.height is None:
            height, width = image.shape[0:2]
        else:
            image = cv2.resize(image, (self.width, self.height))
            width = self.width
            height = self.height
        status = self.visual_odom_mono.process(image, width, height)

        if status:
            self.pose = np.array(self.visual_odom_mono.getPose())

            self.x = self.pose[0, 3]
            self.y = self.pose[1, 3]
            self.z = self.pose[2, 3]

            # delta_x = self.x - self.prev_x
            # delta_y = self.y - self.prev_y
            # delta_z = self.z - self.prev_z
            # print("%0.5f\t%0.5f\t%0.5f" % (delta_x, delta_y, delta_z))
            # self.prev_x = self.x
            # self.prev_y = self.y
            # self.prev_z = self.z

            print("%0.5f\t%0.5f\t%0.5f" % (self.x, self.y, self.z))

        return status
