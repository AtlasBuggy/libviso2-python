import cv2
import numpy as np

from pylibviso2.pylibviso2 import *

class Viso2Mono:
    def __init__(self, f, cu, cv, width=None, height=None):
        param = mono_parameters()
        param.calib.f  = 645.24;
        param.calib.cu = 635.96;
        param.calib.cv = 194.13;
        self.visual_odom_mono = VisualOdometryMono(param)

        self.width = width
        self.height = height

        self.pose = None
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def update(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.width is None or self.height is None:
            height, width = image.shape[0:2]
        else:
            image = cv2.resize(image, (self.width, self.height))
            width = self.width
            height = self.height
        status = self.visual_odom_mono.process(image, width, height)

        self.pose = np.array(self.visual_odom_mono.getPose())

        self.x = self.pose[0, 3]
        self.y = self.pose[1, 3]
        self.z = self.pose[2, 3]

        # print(status, self.x, self.z, self.visual_odom_mono.getNumberOfMatches())
        print("%0.5f\t%0.5f" % (self.x, self.z))

        return status
