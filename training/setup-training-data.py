#!/usr/bin/env python3

from subprocess import check_output
from os import path, makedirs
from glob import glob
from shutil import copyfile, rmtree
import csv
import gdown
from random import Random

def download_unzip_images():

    # Only re-download and unzip if extracted folder is absent present
    if not path.exists("statues-train"):
        if not path.exists("statues-train.zip"):
            gdown.download(id="1NpTPzQvkAyh9YPS8v_i7z_EZjRy9lYGs")
        check_output("unzip -o statues-train.zip".split()).decode("utf-8")

    # Return paths to extracted images
    lenin_paths = glob("statues-train/statues-lenin/*")
    other_paths = glob("statues-train/statues-other/*")
    return other_paths, lenin_paths

def download_convert_labels():

    # Return value of this function: dictionary mapping file names to
    # label strings in yolo format, each line in string corresponding
    # to one label
    img_label_dict = {}
    
    if not path.exists("statues_labels.csv"):
        gdown.download(id="18idZeW3IS1aUqXMypltL_WpZxa0C5opf")
        
    with open("statues_labels.csv", "r") as infile:
        reader = csv.reader(infile)
        content = next(reader)
        assert content == ["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"]

        while True:
            try: fname, width, height, clas, xmin, ymin, xmax, ymax = next(reader)
            except StopIteration: break

            # Convert numeric items to float
            width, height, xmin, ymin, xmax, ymax = float(width), float(height), float(xmin), float(ymin), float(xmax), float(ymax)
            
            # Label to numeric tag, YoloV5 format
            clas_num = {"other":0, "lenin":1}[clas]

            # Convert box coordinates to YoloV5 format
            box_width  = (xmax - xmin)/width
            box_height = (ymax - ymin)/height
            box_center_x = (xmax + xmin)/2.0/width
            box_center_y = (ymax + ymin)/2.0/height

            yolo_label_string = img_label_dict.get(fname, "")
            yolo_label_string += "{} {:.3f} {:.3f} {:.3f} {:.3f}\n".format(clas_num, box_center_x, box_center_y, box_width, box_height)
            
            # If we have a statue of lenin, also label it as a 'other'
            if clas_num == 1 :
                yolo_label_string+=("{} {:.3f} {:.3f} {:.3f} {:.3f}\n".format(0, box_center_x, box_center_y, box_width, box_height))

            img_label_dict[fname] = yolo_label_string

    return img_label_dict

def split_data(data, fraction, seed):
    # Partition input data randomly into two subsets, the first of
    # which is as long as the specified fraction relative to input.
    rng = Random(seed)
    rng.shuffle(data)
    num_head = int(fraction*len(data))
    head = data[:num_head]
    tail = data[num_head:]
    return head, tail

def remove_unlabelled(image_paths, label_dict):
    ret = []
    for pth in image_paths:
        basename = path.basename(pth)
        if basename not in label_dict:
            print("Skipping unlabelled image", basename)
        else:
            ret.append(pth)
    return ret

if __name__ == "__main__":

    # Get image paths and image labels
    other_paths, lenin_paths = download_unzip_images()
    fname_label_dict = download_convert_labels()

    # Some images are unlabelled even though they all contain
    # statues. Remove them for labelling consistency
    other_paths = remove_unlabelled(other_paths, fname_label_dict)
    lenin_paths = remove_unlabelled(lenin_paths, fname_label_dict)

    # Split data set into training/validation subsets
    train_fraction = 0.9
    other_train_paths, other_valid_paths = split_data(other_paths, train_fraction, 0)
    lenin_train_paths, lenin_valid_paths = split_data(lenin_paths, train_fraction, 1)

    # Set up directory structure as expected by yolov5
    rmtree("./images/train/", ignore_errors=True)
    rmtree("./labels/train/", ignore_errors=True)
    rmtree("./images/val/", ignore_errors=True)
    rmtree("./labels/val/", ignore_errors=True)
    makedirs("./images/train/", exist_ok=True)
    makedirs("./labels/train/", exist_ok=True)
    makedirs("./images/val/", exist_ok=True)
    makedirs("./labels/val/", exist_ok=True)
    
    # Move training data to './datasets' as expected by yolov5. 
    for pth in other_train_paths+lenin_train_paths:

        basename = path.basename(pth)
        tag = "lenin" if "lenin" in pth else "other"
        image_path = f"./images/train/{tag}-"+basename
        copyfile(pth, image_path)

        # Set up file path for annotation.
        label_path = image_path
        label_path = label_path.replace("JPG", "txt")
        label_path = label_path.replace("jpg", "txt")
        label_path = label_path.replace("images", "labels")
        with open(label_path, "w") as ofile:
            ofile.write(fname_label_dict[basename])

    # Move validation data to './datasets' as expected by yolov5. 
    for pth in other_valid_paths+lenin_valid_paths:
        basename = path.basename(pth)
        tag = "lenin" if "lenin" in pth else "other"
        image_path = f"./images/val/{tag}-"+basename
        copyfile(pth, image_path)

        # Set up file path for annotation.
        label_path = image_path
        label_path = label_path.replace("JPG", "txt")
        label_path = label_path.replace("jpg", "txt")
        label_path = label_path.replace("images", "labels")
        with open(label_path, "w") as ofile:
            ofile.write(fname_label_dict[basename])
