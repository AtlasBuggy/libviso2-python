
from atlasbuggy.opencv import OpenCVPipeline

from .viso2 import Viso2Mono


class Viso2MonoPipeline(OpenCVPipeline):
    def __init__(self, f, cu, cv, width=None, height=None, enabled=True, logger=None):
        super(Viso2MonoPipeline, self).__init__(enabled, logger=logger)
        self.viso2 = Viso2Mono(f, cu, cv, width, height)

        self.pose_service = "pose"
        self.define_service(self.pose_service, message_type=tuple)

    def pipeline(self, image):
        if self.viso2.update(image):
            self.broadcast_nowait((self.viso2.x, self.viso2.y, self.viso2.z), self.pose_service)
        return image
