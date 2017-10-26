import asyncio

from atlasbuggy import Node, Orchestrator, run
from atlasbuggy.opencv import OpenCVViewer, OpenCVVideo
from atlasbuggy.plotters import LivePlotter

from pylibviso2.node import Viso2MonoPipeline


class VisoPlotterNode(Node):
    def __init__(self, enabled=True):
        super(VisoPlotterNode, self).__init__(enabled)

        self.plotter_tag = "plotter"
        self.plotter_sub = self.define_subscription(self.plotter_tag)
        self.plotter = None

        self.viso_tag = "viso"
        self.viso_sub = self.define_subscription(self.viso_tag, service="pose")
        self.viso_queue = None

    def take(self):
        self.plotter = self.plotter_sub.get_producer()
        self.viso_queue = self.viso_sub.get_queue()

    async def setup(self):
        self.plotter.add_plot(self.name)

    async def loop(self):
        xs = []
        zs = []
        while True:
            x, y, z = await self.viso_queue.get()
            xs.append(x)
            zs.append(z)
            # x = np.random.normal(size=length)
            # y = np.random.normal(size=length)
            self.plotter.plot(self.name, xs, zs)
            await asyncio.sleep(0.01)


class VisoOrchestrator(Orchestrator):
    def __init__(self, event_loop):
        self.set_default(level=30)
        super(VisoOrchestrator, self).__init__(event_loop)

        self.video = OpenCVVideo(
            # file_name="naboris/2017_Jul_31/16_34_21-3.mp4",
            # file_name="naboris/2017_May_28/16_23_21.mp4",
            file_name="naboris/2017_Jul_31/16_34_21-1.mp4",
            # file_name="rolls/2017_Oct_07/07_39_40.mp4",
            # file_name="rolls/2017_Oct_01/06_35_25.mp4",
            # file_name="rolls/2017_Oct_07/06_57_05.mp4",
            # file_name="naboris/2017_Aug_28/12_11_41-1.mp4",
            # file_name="naboris/2017_Aug_01/22_09_43-1.mp4",
            directory="/Users/Woz4tetra/Google Drive/Atlas Docs/Media/Videos/",
            bind_to_playback_node=False)
        self.viewer = OpenCVViewer(enabled=True)

        plotting_enabled = False
        self.viso_plotter_node = VisoPlotterNode(plotting_enabled)
        self.plotter = LivePlotter(
            enabled=plotting_enabled,
            title='PLOTS',
            size=(800, 800),
            ncols=2,
            frequency=0
        )

        # image area: 3673.6um, 2738.4um
        # pixel size: 1.4um
        f_pix = 743.28794629
        cu = 239.16868139
        cv = 216.06257926
        distored_w = 639  # 608
        distored_h = 479  # 441
        self.pipeline = Viso2MonoPipeline(f_pix, cu, cv, distored_w, distored_h)

        self.add_nodes(self.viso_plotter_node, self.plotter, self.video, self.viewer, self.pipeline)

        self.subscribe(self.pipeline, self.viewer, self.viewer.capture_tag)
        self.subscribe(self.video, self.pipeline, self.pipeline.capture_tag)
        self.subscribe(self.pipeline, self.viso_plotter_node, self.viso_plotter_node.viso_tag)
        self.subscribe(self.plotter, self.viso_plotter_node, self.viso_plotter_node.plotter_tag)


run(VisoOrchestrator)
