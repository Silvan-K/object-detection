#!/bin/bash

set -e

# The best model checkpoint saved to `weights/best_yolov5x_statues.pt`.

cd yolov5
python train.py --img 640 --batch 8 --epochs 3 \
       --data ../statues.yaml --cfg ./models/yolov5m.yaml --weights yolov5m.pt \
       --name yolov5m_statues --cache disk
