#!/bin/bash

set -e

cd ../yolov5
python train.py --img 1280 --batch 8 --epochs 30 \
       --data ../training/statues.yaml --cfg ./models/yolov5m.yaml --weights yolov5m.pt \
       --name yolov5m_statues --cache disk

# Validating runs/train/yolov5m_statues/weights/best.pt...
# Fusing layers...
# Model Summary: 290 layers, 20856975 parameters, 0 gradients, 48.0 GFLOPs
# Class     Images     Labels          P          R     mAP@.5 mAP@.5:.95: 
# all          732       1187      0.961      0.986      0.986      0.851
# other        732        830      0.955      0.992      0.982      0.817
# lenin        732        357      0.967       0.98       0.99      0.884
