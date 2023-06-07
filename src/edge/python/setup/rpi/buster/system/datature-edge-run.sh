#!/bin/bash

sudo xhost +
export $(cat /etc/datature-edge.conf | xargs)
export PYTHONPATH=$(printf "%s:" `find $DATATURE_EDGE_ROOT_DIR/src/edge/python -type d -not -name __pycache__`)

cat /dev/null > $DATATURE_EDGE_ROOT_DIR/datature-edge-pid.conf

for ENV_FILE in $DATATURE_EDGE_ENV_CONFIG_DIR/*; do
    echo "Starting Datature Edge with $ENV_FILE"
    CMD="env \$(cat $ENV_FILE | tr '\n' ' ' ) $DATATURE_EDGE_PYTHON_EXECUTABLE $DATATURE_EDGE_ROOT_DIR/src/edge/python/main.py"
    /bin/bash -c "$CMD" &
    PID=$!
    echo "$PID=$CMD" >> $DATATURE_EDGE_ROOT_DIR/datature-edge-pid.conf
done
