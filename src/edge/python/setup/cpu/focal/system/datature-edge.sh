#!/bin/bash
## Datature Edge Run Script

VERSION="0.1.0"
POSITIONAL_ARGS=()

function kill_processes() {
    DATATURE_EDGE_ROOT_DIR=`sudo sed -n 's/^DATATURE_EDGE_ROOT_DIR=\(.*\)/\1/p' < /etc/datature-edge.conf`
    IFS=''
    while read -r line; do
        PID=$(echo $line | cut -d "=" -f 1)
        CMD=$(echo $line | cut -d "=" -f 2-)
        if ps -p $PID > /dev/null; then
            echo "Killing process $PID:"
            echo "$CMD"
            kill "$PID"
            echo ""
        fi
    done < "$DATATURE_EDGE_ROOT_DIR/datature-edge-pid.conf"
}

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            echo "Datature Edge help page"
            echo "Usage: datature-edge [OPTIONS] [VALUES]"
            printf "\t%s\t%-20s %s\n" "-c" "--config" "Restart Datature Edge with new environment configuration folder, specified with a YAML file path."
            printf "\t%s\t%-20s %s\n" "--start" "Start Datature Edge with current configuration."
            printf "\t%s\t%-20s %s\n" "--restart" "Restart Datature Edge with current configuration."
            printf "\t%s\t%-20s %s\n" "--stop" "Stop Datature Edge."
            printf "\t%s\t%-20s %s\n" "--enable" "Enable Datature Edge daemon service."
            printf "\t%s\t%-20s %s\n" "--disable" "Disable Datature Edge daemon service."
            printf "\t%s\t%-20s %s\n" "--status" "Check the status of Datature Edge daemon service."
            printf "\t%s\t%-20s %s\n" "-v" "--version" "Show the version of Datature Edge."
            printf "\t%s\t%-20s %s\n" "-h" "--help" "Show this help page."
            exit 0
        ;;
        -c|--config)
            CONFIG="$2"
            shift
            shift
        ;;
        --start)
            sudo xhost +
            echo "Starting Datature Edge..."
            sudo systemctl start datature-edge.service
            echo "Datature Edge started!"
            echo "Please wait..."
            exit 0
        ;;
        --restart)
            sudo xhost +
            echo "Restarting Datature Edge..."
            kill_processes
            sudo systemctl stop datature-edge.service
            sleep 5
            sudo systemctl start datature-edge.service
            echo "Datature Edge restarted!"
            echo "Please wait..."
            exit 0
        ;;
        --stop)
            echo "Stopping Datature Edge..."
            kill_processes
            sudo systemctl stop datature-edge.service
            sleep 5
            echo "Datature Edge stopped!"
            exit 0
        ;;
        --enable)
            sudo systemctl enable datature-edge.service
            echo "Datature Edge daemon service enabled!"
            exit 0
        ;;
        --disable)
            sudo systemctl disable datature-edge.service
            echo "Datature Edge daemon service disabled!"
            exit 0
        ;;
        --status)
            echo "Checking the status of Datature Edge daemon service..."
            sudo systemctl status datature-edge.service
            exit 0
        ;;
        -v|--version)
            echo "Datature Edge version: $VERSION"
            exit 0
        ;;
        *|-*|--*)
            echo "Unknown option '$1'"
            echo "Use 'datature-edge --help' to see the help page."
            exit 1
        ;;
    esac
done

## Restore positional parameters
set -- "${POSITIONAL_ARGS[@]}"

OLD_CONFIG=`sudo sed -n 's/^DATATURE_EDGE_ENV_CONFIG_DIR=\(.*\)/\1/p' < /etc/datature-edge.conf`
sudo sed -i "s@DATATURE_EDGE_ENV_CONFIG_DIR=$PARTITION_COLUMN.*@DATATURE_EDGE_ENV_CONFIG_DIR=$CONFIG@g" /etc/datature-edge.conf
echo "Environment Config Folder: $OLD_CONFIG > $CONFIG"

sudo xhost +
echo "Restarting Datature Edge..."
kill_processes
sudo systemctl stop datature-edge.service
sleep 5
sudo systemctl start datature-edge.service
echo "Datature Edge restarted!"
echo "Please wait..."
