from atlasbuggy import Orchestrator, run
from atlasbuggy.opencv import OpenCVViewer, OpenCVVideo

from pylibviso2.node import Viso2MonoPipeline


class MyOrchestrator(Orchestrator):
    def __init__(self, event_loop):
        self.set_default(level=30)
        super(MyOrchestrator, self).__init__(event_loop)

        self.video = OpenCVVideo(
            # file_name="/Users/Woz4tetra/Google Drive/Atlas Docs/Media/Videos/naboris/2017_Jul_31/16_34_21-3.mp4",
            # file_name="/Users/Woz4tetra/Google Drive/Atlas Docs/Media/Videos/naboris/2017_May_28/16_23_21.mp4",
            file_name="/Users/Woz4tetra/Google Drive/Atlas Docs/Media/Videos/naboris/2017_Jul_31/16_34_21-1.mp4",
            bind_to_playback_node=False)
        self.viewer = OpenCVViewer()

        # image area: 3673.6um, 2738.4um
        # pixel size: 1.4um
        f_pix = 743.28794629  # 0.004491024012320632
        cu = 239.16868139  # 0.0014450823486090525
        cv = 216.06257926  # 0.0013054728473183158
        distored_w = 608
        distored_h = 441
        self.pipeline = Viso2MonoPipeline(f_pix, cu, cv, distored_w, distored_h)

        self.add_nodes(self.video, self.viewer, self.pipeline)

        self.subscribe(self.pipeline, self.viewer, self.viewer.capture_tag)
        self.subscribe(self.video, self.pipeline, self.pipeline.capture_tag)


run(MyOrchestrator)
