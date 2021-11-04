# Setting up your environment

### Checking out the code

This project relies on [yolov5](https://github.com/ultralytics/yolov5) to perform object detection. The yolov5 source code is included as a git submodule. Please make sure to clone this repository via the following command to make sure the yolov5 code is fetched along with the project code:

```
git clone --recurse-submodules git@git.toptal.com:felipe.batista/silvan-kuttimalai.git
```

### Setting up your python environment

We recommend using [virtualenv](https://pypi.org/project/virtualenv/) to set up an isolated virtual python environment. For convenience, a [script](https://git.toptal.com/felipe.batista/silvan-kuttimalai/-/blob/yolo/setup-env.sh) is provided that setups up a virtual environment, activates it, and installs all python dependencies within it. To use it, please run

```
source setup-env.sh
```

# Running the statue detection model

The statue detection model can be run using the main python script [detect-statues.py](https://git.toptal.com/felipe.batista/silvan-kuttimalai/-/blob/yolo/setup-env.sh):

```
python detect-images.py <PATH-TO-IMAGE> <RESULTS-FILE>
```

It accepts as the first command line argument the path to the directory that contains the images to be processed. An optional second argument can be used to specify the path for the result text file (defaults to "results.csv"). The results file will contain one line per detected object in the format `image name;x1;y1;x2;y2;class`, where `(x1,y1)` and `(x2,y2)` are the coordinates of the upper left and lower right corners of the bounding box, respectively. The `class` tag is `1` if the object is identified as Lenin and `0` otherwise. 
