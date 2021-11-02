
if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("image_paths", nargs="+")
    paths = parser.parse_args().image_paths

    heights = []
    widths = []
    import cv2
    for path in paths:
        img = cv2.imread(path)
        heights.append(img.shape[0])
        widths.append(img.shape[1])

    from matplotlib import pyplot as plt
    plt.hist(heights, bins=50, label="Height")
    plt.hist(widths, bins=50, label="Width")
    plt.xlabel("Image size in pixels")
    plt.ylabel("Frequency")
    plt.legend()
    plt.savefig("image-sizes.png")
    
