# Setting up your environment

## Checking out the code

This project relies on [yolov5](https://github.com/ultralytics/yolov5) to perform object detection. The yolov5 source code is included as a git submodule. Please make sure to clone this repository via the following command to make sure the yolov5 code is fetched along with the project code:

```
git clone --recurse-submodules git@git.toptal.com:felipe.batista/silvan-kuttimalai.git
```

## Setting up your python environment

We recommend using [virtualenv](https://pypi.org/project/virtualenv/) to set up an isolated virtual python environment. For convenience, a [script](https://git.toptal.com/felipe.batista/silvan-kuttimalai/-/blob/yolo/setup-env.sh) is provided that setups up a virtual environment, activates it, and installs all python dependencies within it. To use it, please run

```
source setup-env.sh
```

# Running the statue detection model

