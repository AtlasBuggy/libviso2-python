import cv2
import numpy as np
from pylibviso2.pylibviso2 import *

# print(mono_parameters())
# print(matcher_parameters())
# print(bucketing_parameters())
# print(calibration_parameters())
# print(parameters())

window_name = "visual odometry"
cv2.namedWindow(window_name)

param = mono_parameters()
param.calib.f  = 645.24;
param.calib.cu = 635.96;
param.calib.cv = 194.13;

v = VisualOdometryMono(param)

def load_image(path):
    global pose
    image = cv2.imread(path)
    image = cv2.resize(image, (1300, 520))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape[0:2]
    v.process(image, width, height)

    pose = np.array(v.getPose())
    x = pose[0, 3]
    y = pose[1, 3]
    z = pose[2, 3]
    print(x, y, z)

    # print(v.getNumberOfMatches())
    # print(v.getNumberOfInliers())
    return image


# load_image("/Users/Woz4tetra/Google Drive/Atlas Docs/Media/Photos/Sharing/20170422_090847.jpg")
# load_image("/Users/Woz4tetra/Google Drive/Atlas Docs/Media/Photos/Sharing/20170422_091100.jpg")
# load_image("/Users/Woz4tetra/Google Drive/Atlas Docs/Media/Photos/Sharing/20170422_091115.jpg")
for i in range(114):
    image = load_image("2011_09_26/2011_09_26_drive_0001_extract/image_03/data/%.10d.png" % i)
    cv2.imshow(window_name, image)
    if cv2.waitKey(1) > -1:
        break
