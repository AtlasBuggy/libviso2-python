import cv2

from atlasbuggy import Orchestrator, run
from atlasbuggy.opencv import OpenCVViewer, OpenCVVideo

from pylibviso2.viso2_node import Viso2MonoPipeline

class MyOrchestrator(Orchestrator):
    def __init__(self, event_loop):
        self.set_default(level=30)
        super(MyOrchestrator, self).__init__(event_loop)

        self.video = OpenCVVideo(file_name="/Users/Woz4tetra/Google Drive/Atlas Docs/Media/Videos/cia_buggy_videos/Ascension 10-17 roll 3-2.mp4", bind_to_playback_node=False)
        self.viewer = OpenCVViewer()
        self.pipeline = Viso2MonoPipeline(100, 100, 100)

        self.add_nodes(self.video, self.viewer, self.pipeline)

        self.subscribe(self.pipeline, self.viewer, self.viewer.capture_tag)
        self.subscribe(self.video, self.pipeline, self.pipeline.capture_tag)

run(MyOrchestrator)
