#!/bin/bash

python3 -m pylint src/edge/python/ && \
python3 -m flake8 src/edge/python/ && \
python3 -m pydocstyle \
--add-select=D203,D200 \
--add-ignore=D205,D211,D212,D400 \
--match='(?!__init__).*\.py' \
src/edge/python/
