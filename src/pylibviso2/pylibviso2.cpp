#include <iostream>
#include <string>
#include <vector>
#include <stdint.h>
#include <Python.h>
#include <cstdio>

#include <boost/python.hpp>

#include "viso_mono.h"

#include "viso_mono_wrapper.cpp"


namespace py = boost::python;
using namespace std;

BOOST_PYTHON_MODULE(pylibviso2)
{
    py::class_<VisualOdometryMono::parameters>("mono_parameters")
        .def_readwrite("calib", &VisualOdometryMono::parameters::calib)
        .def_readwrite("height", &VisualOdometryMono::parameters::height)
        .def_readwrite("pitch", &VisualOdometryMono::parameters::pitch)
        .def_readwrite("ransac_iters", &VisualOdometryMono::parameters::ransac_iters)
        .def_readwrite("inlier_threshold", &VisualOdometryMono::parameters::inlier_threshold)
        .def_readwrite("motion_threshold", &VisualOdometryMono::parameters::motion_threshold)
    ;

    py::class_<Matcher::parameters>("matcher_parameters")
        .def_readwrite("nms_n", &Matcher::parameters::nms_n)
        .def_readwrite("nms_tau", &Matcher::parameters::nms_tau)
        .def_readwrite("match_binsize", &Matcher::parameters::match_binsize)
        .def_readwrite("match_radius", &Matcher::parameters::match_radius)
        .def_readwrite("match_disp_tolerance", &Matcher::parameters::match_disp_tolerance)
        .def_readwrite("outlier_disp_tolerance", &Matcher::parameters::outlier_disp_tolerance)
        .def_readwrite("outlier_flow_tolerance", &Matcher::parameters::outlier_flow_tolerance)
        .def_readwrite("multi_stage", &Matcher::parameters::multi_stage)
        .def_readwrite("half_resolution", &Matcher::parameters::half_resolution)
        .def_readwrite("refinement", &Matcher::parameters::refinement)
    ;

    py::class_<VisualOdometry::bucketing>("bucketing_parameters")
        .def_readwrite("max_features", &VisualOdometry::bucketing::max_features)
        .def_readwrite("bucket_width", &VisualOdometry::bucketing::bucket_width)
        .def_readwrite("bucket_height", &VisualOdometry::bucketing::bucket_height)
    ;

    py::class_<VisualOdometry::calibration>("calibration_parameters")
        .def_readwrite("f", &VisualOdometry::calibration::f)
        .def_readwrite("cu", &VisualOdometry::calibration::cu)
        .def_readwrite("cv", &VisualOdometry::calibration::cv)
    ;

    py::class_<VisualOdometry::parameters>("parameters")
        .def_readwrite("match", &VisualOdometry::parameters::match)
        .def_readwrite("bucket", &VisualOdometry::parameters::bucket)
        .def_readwrite("calib", &VisualOdometry::parameters::calib)
    ;

    py::class_<VisualOdometryMonoWrapper>("VisualOdometryMono", py::init<VisualOdometryMono::parameters>())
        .def("process", &VisualOdometryMonoWrapper::process)
        .def("getPose", &VisualOdometryMonoWrapper::getPose)
        .def("getNumberOfMatches", &VisualOdometryMonoWrapper::getNumberOfMatches)
        .def("getNumberOfInliers", &VisualOdometryMonoWrapper::getNumberOfInliers)
    ;
}
