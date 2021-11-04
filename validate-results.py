import csv
from glob import glob
import cv2

class LabelledBox():

    def __init__(self, x0, x1, y0, y1, label):

        if (x0 > x1) or (y0 > y1):
            raise ValueError(f"Inconsistent coordinates: {x0},{x1},{y0},{y1}")

        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.label = label
 
    def area(self):
        return (self.x1 - self.x0)*(self.y1 - self.y0)

    @staticmethod
    def IOU(A, B):

        # Boxes with different labels are intepreted as
        # non-overlapping
        if A.label != B.label:
            return 0

        # Coordinates of intersection rectangle
        xi0 = max(A.x0, B.x0)
        xi1 = min(A.x1, B.x1)
        yi0 = max(A.y0, B.y0)
        yi1 = min(A.y1, B.y1)

        # Area of intersection rectangle
        dxi = max(0, xi1-xi0)
        dyi = max(0, yi1-yi0)
        inter = dxi*dyi
        assert(inter >= 0)

        # Area of union
        union = A.area()+B.area()-inter

        # Return intersection over union
        iou = float(inter)/float(union)
        assert (0 <= iou <= 1), iou
        return iou

# def parse_result_boxes(path):

#     # Return value: dict mapping image file names to labelled boxes
#     boxes_by_images =  dict()
    
#     from glob import glob
#     from os.path import basename
#     result_paths = glob(path+"*.txt")
#     for pth in result_paths:
#         img_name = basename(pth).replace("lenin-", "").replace("other-", "")
#         with open(pth, "r") as infile:
#             for line in infile:
#                 items = line.split()
#                 clas = int(items[0])
#                 box_center_x = float(items[1])
#                 box_center_y = float(items[2])
#                 box_width = float(items[3])
#                 box_height = float(items[4])
#                 x0 = int(box_center_x - box_width/2.0)
#                 x1 = int(box_center_x + box_width/2.0)
#                 y0 = int(box_center_y - box_height/2.0)
#                 y1 = int(box_center_y + box_height/2.0)
#                 box = LabelledBox(x0, x1, y0, y1, clas)
#                 boxes_by_images.setdefault(img_name, []).append(box)

def parse_result_boxes(path):
    
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
    
def parse_oracle_boxes(path):

    # Return value: dict mapping image file names to labelled boxes
    boxes_by_images =  dict()

    with open(path, "r") as infile:
        reader = csv.reader(infile)

        # Check first line for correct format
        content = next(reader)
        assert content == ["filename", "width", 
                           "height", "class",
                           "xmin", "ymin",
                           "xmax", "ymax"]

        # Loop over remaining lines and gather one box per line
        while True:
            try: fname, width, height, cls, xmin, ymin, xmax, ymax = next(reader)
            except StopIteration: break

            # Convert to numeric formats
            width, height = float(width), float(height)
            xmin, xmax = float(xmin), float(xmax),
            ymin, ymax = float(ymin), float(ymax)
            cls = {"lenin":1, "other":0}[cls]

            # Need actual image dimensions since box coordinates in
            # oracle file are sometimes for re-sized image
            actual_height, actual_width, _ = \
                cv2.imread(glob(f"datasets/statues/images/*/*-{fname}")[0]).shape
            xmin *= actual_width/width
            xmax *= actual_width/width
            ymin *= actual_height/height
            ymax *= actual_height/height

            # Create box and append to appropriate list of boxes
            box = LabelledBox(int(xmin), int(xmax), int(ymin), int(ymax), cls)
            boxes_by_images.setdefault(fname, []).append(box)
        
    return boxes_by_images


def find_match(result_box, oracle_boxes):
    for o_box in oracle_boxes:
        if(LabelledBox.IOU(r_box, o_box) >= 0.5):
            return o_box
    return None

def show_image(path, boxes):
    
    img = cv2.imread(path)
    for box in boxes:
        color = (255,0,0) if box.label == 0 else (0,0,255)
        width = 2 if box.label == 0 else 6
        cv2.rectangle(img, (box.x0, box.y0),
                      (box.x1, box.y1), color, width)

    from os.path import basename
    win_name = basename(path)
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.imshow(win_name, img)
    cv2.resizeWindow(win_name, 1280, 800)
    cv2.waitKey()

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--result-path", help="Path to result text file", nargs="*", default="./results.csv")
    parser.add_argument("--oracle-path", help="Path to oracle text file", nargs="*", default="./statues_labels.csv")
    args = parser.parse_args()

    oracle_boxes_by_image = parse_oracle_boxes(args.oracle_path)
    result_boxes_by_image = parse_result_boxes(args.result_path)

    FP = 0
    FN = 0
    TP = 0
    
    for image in result_boxes_by_image.keys():

        oracle_boxes = oracle_boxes_by_image[image.replace("lenin-", "").replace("other-", "")]
        result_boxes = result_boxes_by_image[image]

        show_image("datasets/statues/images/val/"+image, oracle_boxes)

        matched_boxes = set()
        for r_box in result_boxes:
            matched_box = find_match(r_box, oracle_boxes)
            if matched_box is not None:
                TP += 1
                matched_boxes.add(matched_box)
            else:
                FP += 1

        # Number of matched boxes is number of oracle boxes to which
        # we have found a match within our detected boxes. Remaining
        # boxes in oracle set are undetected boxes, i.e. false
        # negatives
        FN += len(oracle_boxes) - len(matched_boxes)

    num_oracle_boxes = sum([len(boxes) for boxes in oracle_boxes_by_image.values()])
    #assert(TP+FN == num_oracle_boxes)
        
    R = float(TP)/float(TP+FN)
    P = float(TP)/float(TP+FP)
    
    print("Precision: ", P)
    print("Recall:    ", R)
