import numpy as np

from pylibviso2.pylibviso2 import *

video_stablizer = VideoStabKalman()
video_stablizer.process(np.zeros(300))
