# project
cmake_minimum_required(VERSION 3.0)
project (libviso2-python)

# directories
set (LIBVISO2_SRC_DIR src/libviso2)

# include directory
include (FindPkgConfig)
include_directories("${LIBVISO2_SRC_DIR}")

# use sse3 instruction set
SET(CMAKE_CXX_FLAGS "-msse3")
add_definitions(-msse3)

# sources
FILE(GLOB LIBVISO2_SRC_FILES "src/libviso2/*.cpp")

# make release version
set(CMAKE_BUILD_TYPE Release)

include_directories(src/libviso2)
add_library(viso2
  src/libviso2/filter.cpp
  src/libviso2/matcher.cpp
  src/libviso2/matrix.cpp
  src/libviso2/reconstruction.cpp
  src/libviso2/triangle.cpp
  src/libviso2/viso.cpp
  src/libviso2/viso_mono.cpp
  src/libviso2/viso_stereo.cpp)

# add_executable(viso2 ${LIBVISO2_SRC_FILES})

find_package(PythonInterp 3 REQUIRED)
find_package(PythonLibs 3 REQUIRED)

find_package(Boost COMPONENTS python3 REQUIRED)
IF (Boost_FOUND)
    include_directories("${Boost_INCLUDE_DIR}")
    add_definitions( "-DHAS_BOOST" )
ENDIF()

include_directories(${CMAKE_BINARY_DIR}/include ${PYTHON_INCLUDE_DIRS})
link_libraries(${Boost_LIBRARIES} ${PYTHON_LIBRARIES} viso2)
link_directories("${Boost_LIBRARY_DIRS}")

python_add_module(pylibviso2 src/pylibviso2/pylibviso2.cpp)
