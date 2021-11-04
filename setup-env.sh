#!/bin/bash

# Create virtual environment if it doesn't exist yet
[ -d "./venv" ] || virtualenv venv

# Activate virtual env
source venv/bin/activate

# Add yolov5 root directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(git rev-parse --show-toplevel)/yolov5/

# Install dependencies
pip install -r $(git rev-parse --show-toplevel)/yolov5/requirements.txt

# Bug in opencv, need to downgrade
pip install --upgrade opencv-python==4.3.0.38
