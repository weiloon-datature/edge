#!/bin/bash
## Datature Edge Raspberry Pi 4b Environment Setup

ARCH=$2
OS_NAME=$3
OS_VERSION=$4
OS_VERSION_CODENAME=$5
DEVICE=$6

ROOT_DIR=`pwd`
CURRENT_DIR=`dirname ${BASH_SOURCE:-$0}`

## Enable the camera (will require reboot for settings to take effect)
sudo raspi-config nonint do_camera 0
sudo raspi-config nonint do_boot_behaviour B4
echo ""
echo "Raspberry Pi Configuration:"
echo "---------------------------"
echo Camera: `sudo raspi-config nonint get_camera`
echo CLI Autologin: `sudo raspi-config nonint get_boot_cli`
echo GUI Autologin: `sudo raspi-config nonint get_autologin`
echo "---------------------------"
echo ""

sudo apt update
sudo apt upgrade -y

## Install common packages
sudo apt install -y build-essential cmake ffmpeg gcc g++ git shc
sudo apt install -y libssl-dev pkg-config software-properties-common python-scipy

## Install packages that enable OpenCV to use different formats for both images and videos
sudo apt install -y libjpeg-dev libtiff-dev libjasper-dev libpng-dev libwebp-dev libopenexr-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libdc1394-22-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
sudo apt install -y libgtk-3-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5

## Install packages to speed up OpenCV
sudo apt install -y libatlas-base-dev liblapacke-dev gfortran

## Install HDF5 packages for OpenCV to manage data
sudo apt install -y libhdf5-dev libhdf5-103

## Install Python 3.7 support packages
sudo apt install -y python3.7 python3.7-dev python3-pip python3.7-venv

## Setup Python 3.7 virtual environment
/usr/bin/python3.7 -m pip install virtualenv

if [ ! -d $ROOT_DIR/datature-edge-env ]; then
    /usr/bin/python3.7 -m virtualenv datature-edge-env
fi

PYTHON_EXECUTABLE="$ROOT_DIR/datature-edge-env/bin/python3.7"

## Install wheel version of Tensorflow, onnxruntime, Pytorch, and other pip packages
if [ ! -d $ROOT_DIR/packages ]; then
    mkdir $ROOT_DIR/packages
fi
wget -nc -nv -O $ROOT_DIR/packages/tensorflow-2.4.0-cp37-none-linux_armv7l.whl https://github.com/lhelontra/tensorflow-on-arm/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl
wget -nc -nv -O $ROOT_DIR/packages/onnxruntime-1.9.1-cp37-none-linux_armv7l.whl https://github.com/PINTO0309/onnxruntime4raspberrypi/releases/download/v1.9.1/onnxruntime-1.9.1-cp37-none-linux_armv7l.whl_np1195
wget -nc -nv -O $ROOT_DIR/packages/torch-1.7.0a0-cp37-cp37m-linux_armv7l.whl https://github.com/Kashu7100/pytorch-armv7l/raw/main/torch-1.7.0a0-cp37-cp37m-linux_armv7l.whl
wget -nc -nv -O $ROOT_DIR/packages/torchvision-0.8.0a0-cp37-cp37m-linux_armv7l.whl https://github.com/Kashu7100/pytorch-armv7l/raw/main/torchvision-0.8.0a0%2B45f960c-cp37-cp37m-linux_armv7l.whl
$PYTHON_EXECUTABLE -m pip install --upgrade pip
$PYTHON_EXECUTABLE -m pip install -r $CURRENT_DIR/requirements.txt

## Clone and install Datature Hub
if [ ! -d $ROOT_DIR/packages/hub ]; then
    cd packages
    git clone https://github.com/datature/hub.git
    cd hub
    git checkout add-model-formats
    $PYTHON_EXECUTABLE setup.py install
    cd ../..
fi

## Create log directories
if [ ! -d $ROOT_DIR/logs/debug ]; then
    mkdir -p $ROOT_DIR/logs/debug
fi
if [ ! -d $ROOT_DIR/logs/profiling ]; then
    mkdir -p $ROOT_DIR/logs/profiling
fi

if [ "$NO_SYSTEM_SCRIPT" == "false" ]; then
    ## Compile Datature Edge executable
    sudo chmod u+x $CURRENT_DIR/system/datature-edge.sh
    sudo shc -U -f $CURRENT_DIR/system/datature-edge.sh -o /usr/bin/datature-edge
    
    ## Copy system-level files
    sudo cp $CURRENT_DIR/system/datature-edge-run.sh $ROOT_DIR
    sudo chmod u+x $ROOT_DIR/datature-edge-run.sh
    sudo cp $CURRENT_DIR/system/datature-edge.conf /etc
    sudo sed -i "s@DATATURE_EDGE_ROOT_DIR=$PARTITION_COLUMN.*@DATATURE_EDGE_ROOT_DIR=$ROOT_DIR@g" /etc/datature-edge.conf
    sudo sed -i "s@DATATURE_EDGE_PYTHON_EXECUTABLE=$PARTITION_COLUMN.*@DATATURE_EDGE_PYTHON_EXECUTABLE=$PYTHON_EXECUTABLE@g" /etc/datature-edge.conf
    sudo sed -i "s@DATATURE_EDGE_ENV_CONFIG_DIR=$PARTITION_COLUMN.*@DATATURE_EDGE_ENV_CONFIG_DIR=$ROOT_DIR/src/edge/python/common/samples/env_config@g" /etc/datature-edge.conf
    sudo cp $CURRENT_DIR/system/datature-edge.service /etc/systemd/system
    
    if [ ! -f $ROOT_DIR/datature-edge-pid.conf ]; then
        touch $ROOT_DIR/datature-edge-pid.conf
    fi
    
    mkdir -p $ROOT_DIR/logs/debug
    touch $ROOT_DIR/logs/debug/debug.log
    touch $ROOT_DIR/logs/debug/config.log
    mkdir -p $ROOT_DIR/logs/profiling
    touch $ROOT_DIR/logs/profiling/profiling.log
    
    sudo systemctl daemon-reload
    sudo systemctl enable datature-edge.service
fi

sudo xhost +
export $(cat $CURRENT_DIR/system/datature-edge.conf | xargs)
export PYTHONPATH=$(printf "%s:" `find $ROOT_DIR/src/edge/python -type d -not -name __pycache__`)

## Build OpenCV from source
OPENCV_EXISTS=`$PYTHON_EXECUTABLE -c 'import pkgutil; print(1 if pkgutil.find_loader("cv2") else 0)'`
if [ $OPENCV_EXISTS -eq 0 ]; then
    sudo chmod u+x $CURRENT_DIR/build-opencv.sh
    . $CURRENT_DIR/build-opencv.sh
fi

echo ""
echo "Datature Edge successfully installed!"

if [ "$NO_SYSTEM_SCRIPT" == "false" ]; then
    ## Reboot
    echo "Rebooting in 5 seconds..."
    sleep 5
    sudo reboot -f
fi
