#!/usr/bin/env python3

import csv
from glob import glob
import cv2
from os import path

from helpers import LabelledBox

def parse_result_boxes(path):
    """
    Parse the input file and return a dictionary mapping each image
    name to a list of LabelledBox instances, where each box
    corresponds to an object detected in the corrsponding image.

    """
    
    # Return value: dict mapping image file names to labelled boxes
    boxes_by_images =  dict()

    # Loop over infile, one box per line
    with open(path, "r") as infile:
        for items in csv.reader(infile, delimiter=";"):

            # Convert to numeric formats
            image_name, x0, y0, x1, y1, cls = items
            x0, x1 = int(x0), int(x1)
            y0, y1 = int(y0), int(y1)
            cls = int(cls)

            # Create box and append to appropriate list of boxes
            box = LabelledBox(x0, x1, y0, y1, cls)
            boxes_by_images.setdefault(image_name, []).append(box)
        
    return boxes_by_images

def show_image_boxes(path, boxes):
    """
    Open the image in the provided file path and show it along with
    the provided boxes.

    """
    
    img = cv2.imread(path)
    for box in boxes:
        color = (255,0,0) if box.label == 0 else (0,0,255)
        tag = "Lenin" if box.label == 1 else "Other"
        cv2.rectangle(img, (box.x0, box.y0),
                      (box.x1, box.y1), color, 6)
        cv2.putText(img, tag, (box.x0, box.y0-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 4)

    from os.path import basename
    win_name = basename(path)
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.imshow(win_name, img)
    cv2.resizeWindow(win_name, 1280, 800)
    cv2.waitKey()

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("image_path", help="Path to the directory containing the images")
    parser.add_argument("result_path", help="Path to result text file", nargs="?", default="./results.csv")
    args = parser.parse_args()

    boxes_by_image = parse_result_boxes(args.result_path)
    for image in boxes_by_image.keys():
        boxes = boxes_by_image[image]
        show_image_boxes(path.join(args.image_path, image), boxes)
