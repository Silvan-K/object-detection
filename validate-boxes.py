if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("image_path")
    parser.add_argument("label_path")
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

            color = (0,0,255) if clas == 0 else (255,0,0)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    from os import path
    cv2.imshow(path.basename(args.image_path), img)
