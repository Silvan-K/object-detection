#!/usr/bin/env python

from subprocess import check_output
from os import path, makedirs
from glob import glob
from shutil import copyfile, rmtree
import csv

# Download/unzip data using the links provided in email
# print(check_output("gdown --id 18idZeW3IS1aUqXMypltL_WpZxa0C5opf".split()).decode("utf-8"))
# print(check_output("gdown --id 1NpTPzQvkAyh9YPS8v_i7z_EZjRy9lYGs".split()).decode("utf-8"))
# print(check_output("unzip -o statues-train.zip".split()).decode("utf-8"))

# Move images into directories as required by YoloV5. Note: need to
# prefix image names with tag becaues file names are not unique.
makedirs("./datasets/statues/images/train/", exist_ok=True)
lenin_paths = glob("statues-train/statues-lenin/*")
other_paths = glob("statues-train/statues-other/*")
lenin_names = [path.basename(p) for p in lenin_paths]
other_names = [path.basename(p) for p in other_paths]

# Check duplicates. Saw that identical filename may appear both in
# lenin and in other directory, sometimes corresponding to identical
# pictures, sometimes not. Hence, make filenames unique below by
# prepending annotation tag.
duplicates = [name for name in lenin_names if name in other_names]
print("Duplicate file names:", duplicates)

new_lenin_paths = ["./datasets/statues/images/train/lenin-"+
                   name for name in lenin_names]
new_other_paths = ["./datasets/statues/images/train/other-"+
                   name for name in other_names]
for old_path, new_path in zip(lenin_paths, new_lenin_paths):
    copyfile(old_path, new_path)
for old_path, new_path in zip(other_paths, new_other_paths):
    copyfile(old_path, new_path)

# Save annotations in YoloV5 format
rmtree("./datasets/statues/labels/train/")
makedirs("./datasets/statues/labels/train/", exist_ok=True)
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
        clas_num = "0" # {"other":"0", "lenin":"1"}[clas]

        # Convert box coordinates to YoloV5 format
        box_width  = (xmax - xmin)/width
        box_height = (ymax - ymin)/height
        box_center_x = (xmax + xmin)/2.0/width
        box_center_y = (ymax + ymin)/2.0/height

        # Set up file for annotation. Note that we need to append to
        # file, as several labels may refer to the same file
        fname = "./datasets/statues/labels/train/"+clas+"-"+fname
        fname = fname.replace("JPG", "txt")
        fname = fname.replace("jpg", "txt")
        with open(fname, "a") as ofile:
            ofile.write("{} {:.3f} {:.3f} {:.3f} {:.3f}\n".
                        format(clas_num, box_center_x, box_center_y, box_width, box_height))

print(check_output("wc -l statues_labels.csv".split()).decode("utf-8"))
print("Number of images containing Lenin:", len(lenin_names))
print("Number of images containing other:", len(other_names))
