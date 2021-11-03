#!/bin/bash

set -e

# The best model checkpoint saved to `weights/best_yolov5x_statues.pt`.

cd yolov5
python train.py --img 1280 --batch 8 --epochs 30 \
       --data ../statues.yaml --cfg ./models/yolov5m.yaml --weights yolov5m.pt \
       --name yolov5m_statues --cache disk

# Validating runs/train/yolov5m_statues/weights/best.pt...
# Fusing layers...
# Model Summary: 290 layers, 20856975 parameters, 0 gradients, 48.0 GFLOPs
# Class     Images     Labels          P          R     mAP@.5 mAP@.5:.95: 100%|████████████████████████████████████████████████| 46/46 [00:06<00:00,  6.81it/s]
# all        732       1187      0.961      0.986      0.986      0.851
# other        732        830      0.955      0.992      0.982      0.817
# lenin        732        357      0.967       0.98       0.99      0.884



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
    
