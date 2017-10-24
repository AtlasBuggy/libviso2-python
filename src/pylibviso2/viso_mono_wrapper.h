

namespace py = boost::python;

class VisualOdometryMonoWrapper {
public:
    VisualOdometryMonoWrapper(VisualOdometryMono::parameters param);

    bool process (py::object image, int32_t image_width, int32_t image_height);
    py::list getPose();
    double getNumberOfMatches();
    double getNumberOfInliers();

private:
    Matrix pose;
    VisualOdometryMono *viso_mono_instance;
};
