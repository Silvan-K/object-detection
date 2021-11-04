"""Visualize bounding boxes stored in yolov5 text form"""

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("image_path", help="Input image path")
    parser.add_argument("label_path", help="Path to text file containing bounding boxes in yolov5 format")
    args = parser.parse_args()

    import cv2
    img = cv2.imread(args.image_path)
    img_height = img.shape[0]
    img_width  = img.shape[1]

    with open(args.label_path, "r") as infile:
        for line in infile:

            items = line.split()
            clas = int(items[0])
            box_center_x = float(items[1])*img_width
            box_center_y = float(items[2])*img_height
            box_width = float(items[3])*img_width
            box_height = float(items[4])*img_height

            x1 = int(box_center_x - box_width/2.0)
            x2 = int(box_center_x + box_width/2.0)
            y1 = int(box_center_y - box_height/2.0)
            y2 = int(box_center_y + box_height/2.0)

            color = (255,0,0) if clas == 0 else (0,0,255)
            width = 2 if clas == 0 else 6
            cv2.rectangle(img, (x1, y1), (x2, y2), color, width)

    from os import path
    win_name = path.basename(args.image_path)
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.imshow(win_name, img)
    cv2.resizeWindow(win_name, 1280, 800)
    cv2.waitKey()
