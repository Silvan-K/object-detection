#!/bin/bash

set -e

# The best model checkpoint saved to `weights/best_yolov5x_statues.pt`.

cd yolov5
python train.py --img 1280 --batch 8 --epochs 100 \
       --data ../statues.yaml --cfg ./models/yolov5m.yaml --weights yolov5m.pt \
       --name yolov5m_statues --cache disk


# python train.py --img 640 --batch 2 --epochs 3 \
#        --data ../statues.yaml \
#        --cfg ./models/yolov5s.yaml \
#        --weights yolov5s.pt \
#        --device cpu \
#        --name yolov5s_statues --cache disk
# Model Summary: 213 layers, 7012822 parameters, 0 gradients, 15.8 GFLOPs
# Class     Images     Labels          P          R     mAP@.5 mAP@.5:.95: 100%|██████████████████████████████████████████████| 183/183 [01:20<00:00,  2.28it/s]
# all        732        830      0.396      0.604      0.465      0.207


# Best model checkpoint saved to weights/best_yolov5x_statues.pt
    
