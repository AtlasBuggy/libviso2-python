
#include "viso_mono_wrapper.h"


VisualOdometryMonoWrapper::VisualOdometryMonoWrapper(VisualOdometryMono::parameters param)
{
    this->viso_mono_instance = new VisualOdometryMono(param);
    this->pose = Matrix::eye(4);
}

bool VisualOdometryMonoWrapper::process(py::object image, int32_t image_width, int32_t image_height)
{
    PyObject* pimage = image.ptr();
    Py_buffer pybuf;
    if (PyObject_GetBuffer(pimage, &pybuf, PyBUF_SIMPLE) != -1)
    {
        void *buf = pybuf.buf;
        uint8_t *uint8_buffer = (uint8_t *)buf;
        PyBuffer_Release(&pybuf);
        int32_t dims[] = {image_width, image_height, image_width};

        return this->viso_mono_instance->process(uint8_buffer, dims);
    }
    else {
        PyErr_SetString(PyExc_ValueError, "Invalid image!! Couldn't retrieve a buffer.");
        return false;
    }
}

py::list VisualOdometryMonoWrapper::getPose()
{
    Matrix motion = this->viso_mono_instance->getMotion();
    this->pose = this->pose * Matrix::inv(motion);
    py::list l;
    for (int32_t i = 0; i < this->pose.m; i++) {
        py::list sub_l;
        l.append(sub_l);
        for (int32_t j = 0; j < this->pose.n; j++) {
            sub_l.append(this->pose.val[i][j]);
        }
    }
    return l;
}

double VisualOdometryMonoWrapper::getNumberOfMatches()
{
    return this->viso_mono_instance->getNumberOfMatches();
}

double VisualOdometryMonoWrapper::getNumberOfInliers()
{
    return this->viso_mono_instance->getNumberOfInliers();
}
