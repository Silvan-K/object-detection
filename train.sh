#!/bin/bash

set -e

# The best model checkpoint saved to `weights/best_yolov5x_statues.pt`.

cd yolov5
python train.py --img 1280 --batch 16 --epochs 3 \
       --data ../statues.yaml --cfg ./models/yolov5x.yaml --weights yolov5x.pt \
       --name yolov5x_statues --cache
