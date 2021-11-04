
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

    @staticmethod
    def from_yolo_string(line, img_height, img_width):
        """
        Parse a string as it is produced by yolov5 and covert it to a
        LabelledBox instance

        """

        items = line.split()
        clas = int(items[0])
        # Yolo uses relative coords, hence scale by image dimensions
        box_center_x = float(items[1])*img_width
        box_center_y = float(items[2])*img_height
        box_width = float(items[3])*img_width
        box_height = float(items[4])*img_height
        
        # Round to integer as we are converting to absolute pixel coords
        x0 = round(box_center_x - 0.5*box_width)
        x1 = round(box_center_x + 0.5*box_width)
        y0 = round(box_center_y - 0.5*box_height)
        y1 = round(box_center_y + 0.5*box_height)

        return LabelledBox(x0, x1, y0, y1, label)

