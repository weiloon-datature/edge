#!/bin/bash

VERSION="0.1.0"
POSITIONAL_ARGS=()
NO_SYSTEM_SCRIPT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            echo "Datature Edge help page"
            echo "Usage: datature-edge [OPTIONS] [VALUES]"
            # printf "\t%s\t%-20s %s\n" "--no-system-script" "Skip building system files for daemon service."
            printf "\t%s\t%-20s %s\n" "--clean" "Clean system build files."
            printf "\t%s\t%-20s %s\n" "-v" "--version" "Show the version of Datature Edge."
            printf "\t%s\t%-20s %s\n" "-h" "--help" "Show this help page."
            exit 0
        ;;
        # --no-system-script)
        #     echo "Skipping building system files..."
        #     NO_SYSTEM_SCRIPT=true
        # ;;
        --clean)
            echo "Cleaning Datature Edge system build files..."
            chmod u+x clean.sh
            . clean.sh
            exit 0
        ;;
        -v|--version)
            echo "Datature Edge build version: $VERSION"
            exit 0
        ;;
        *|-*|--*)
            echo "Unknown option '$1'"
            exit 1
        ;;
    esac
done

ARCH=`uname -m`
OS_NAME=`sudo sed -n 's/^NAME=\(.*\)/\1/p' < /etc/os-release | sed 's/"//g' | tr '[:upper:]' '[:lower:]'`
OS_VERSION=`sudo sed -n 's/^VERSION_ID=\(.*\)/\1/p' < /etc/os-release | sed 's/"//g' | tr '[:upper:]' '[:lower:]'`
OS_VERSION_CODENAME=`sudo sed -n 's/^VERSION_CODENAME=\(.*\)/\1/p' < /etc/os-release | sed 's/"//g' | tr '[:upper:]' '[:lower:]'`

if [[ $ARCH == "x86_64" ]];
then
    DEVICE="cpu"
elif [[ $ARCH == "armv7l" ]];
then
    DEVICE="rpi"
elif [[ $ARCH == "aarch64" ]];
then
    if [[ $OS_VERSION_CODENAME == "bullseye" ]];
    then
        DEVICE="rpi"
    elif [[ $OS_VERSION_CODENAME == "linux4tegra" ]];
    then
        DEVICE="jetson"
    else
        echo "Unsupported OS version: $OS_VERSION_CODENAME"
        exit 1
    fi
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

echo "Installing Datature Edge v$VERSION..."
echo ""
echo "Detected Specifications"
echo "-----------------------"
echo "Device: $DEVICE"
echo "System architecture: $ARCH"
echo "OS name: $OS_NAME"
echo "OS version: $OS_VERSION"
echo "OS version codename: $OS_VERSION_CODENAME"
echo "-----------------------"
echo ""

if [ -d "src/edge/python/setup/$DEVICE/$OS_VERSION_CODENAME" ];
then
    chmod u+x src/edge/python/setup/$DEVICE/$OS_VERSION_CODENAME/setup.sh
    . src/edge/python/setup/$DEVICE/$OS_VERSION_CODENAME/setup.sh $NO_SYSTEM_SCRIPT $ARCH $OS_NAME $OS_VERSION $OS_VERSION_CODENAME $DEVICE
else
    echo "Unsupported device $DEVICE and OS version $OS_VERSION_CODENAME"
    exit 1
fi
