#!/bin/bash
"""
Adapted from: https://raw.githubusercontent.com/Qengineering/Install-OpenCV-Raspberry-Pi-32-bits/main/OpenCV-4-5-1.sh
Full tutorial: https://qengineering.eu/install-opencv-4.5-on-raspberry-pi-4.html
"""

set -e
echo "Installing OpenCV 4.5.1"
cd /home/pi
if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    VER=$VERSION_ID
fi

# Install apt dependencies
sudo apt-get install -y build-essential cmake git unzip pkg-config
sudo apt-get install -y libjpeg-dev libtiff-dev libpng-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install -y libgtk2.0-dev libcanberra-gtk* libgtk-3-dev
sudo apt-get install -y libgstreamer1.0-dev gstreamer1.0-gtk3
sudo apt-get install -y libgstreamer-plugins-base1.0-dev gstreamer1.0-gl
sudo apt-get install -y libxvidcore-dev libx264-dev

if [ $VER == '11' ]; then
    echo "Detected Bullseye OS"
else
    sudo apt-get install -y python-dev python-numpy python-pip
fi

sudo apt-get install -y python3-dev python3-numpy python3-pip
sudo apt-get install -y libtbb2 libtbb-dev libdc1394-22-dev
sudo apt-get install -y libv4l-dev v4l-utils
sudo apt-get install -y libopenblas-dev libatlas-base-dev libblas-dev
sudo apt-get install -y liblapack-dev gfortran libhdf5-dev
sudo apt-get install -y libprotobuf-dev libgoogle-glog-dev libgflags-dev
sudo apt-get install -y protobuf-compiler

# Retrieve OpenCV files
sudo rm -rf opencv*
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.1.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.1.zip

unzip opencv.zip
unzip opencv_contrib.zip
mv opencv-4.5.1 /home/pi/opencv
mv opencv_contrib-4.5.1 /home/pi/opencv_contrib
rm opencv.zip
rm opencv_contrib.zip

cd /home/pi/opencv
mkdir build
cd build

# Run CMake
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-D ENABLE_NEON=ON \
-D ENABLE_VFPV3=ON \
-D WITH_OPENMP=ON \
-D WITH_OPENCL=OFF \
-D BUILD_ZLIB=ON \
-D BUILD_TIFF=ON \
-D WITH_FFMPEG=ON \
-D WITH_TBB=ON \
-D BUILD_TBB=ON \
-D BUILD_TESTS=OFF \
-D WITH_EIGEN=OFF \
-D WITH_GSTREAMER=ON \
-D WITH_V4L=ON \
-D WITH_LIBV4L=ON \
-D WITH_VTK=OFF \
-D WITH_QT=OFF \
-D OPENCV_ENABLE_NONFREE=ON \
-D INSTALL_C_EXAMPLES=OFF \
-D INSTALL_PYTHON_EXAMPLES=OFF \
-D BUILD_NEW_PYTHON_SUPPORT=ON \
-D BUILD_opencv_python3=TRUE \
-D OPENCV_GENERATE_PKGCONFIG=ON \
-D PYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages \
-D BUILD_EXAMPLES=OFF ..

# Build OpenCV
make -j4
sudo make install
sudo ldconfig
sudo apt-get update

echo "OpenCV 4.5.1 successfully installed!"
