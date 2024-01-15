<div align="center">

# YOLOv8 with ROS1

![Ubuntu 20.04](https://img.shields.io/badge/Ubuntu-20.04-blue?style=flat-square&logo=Ubuntu&logoColor=FFFFFF)
![Ros noetic](https://img.shields.io/badge/Ros-noetic-blue?style=flat-square&logo=ROS)
![Python 3.8](https://img.shields.io/badge/Python-3.8-blue?style=flat-square&logo=Python&logoColor=FFFFFF)

</div>

<font size=2>

> **Note** <br>
> This project if forked from <br>
> [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) <br>

</font>

<font size=2>

## :rocket: install
Install the required library:
```shell
sudo apt install python3-pip
pip install ultralytics
pip install rospkg
```

Clone the repo into your catkin workspace and build the package:
```shell
mkdir -p yolov8_ws/src && cd yolov8_ws/src
git clone https://github.com/JINtaeung/yolov8_ros1.git
cd ../ && catkin build
echo "source ~/yolov8_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## :clipboard: Usage
Before you launch the node, adjust the parameters in the [launch file](https://github.com/JINtaeung/yolov8_ros1/blob/main/launch/yolo_v8.launch).

- [launch/yolo_v8.launch](https://github.com/JINtaeung/yolov8_ros1/blob/main/launch/yolo_v8.launch) for developer

|params|value|
|-----------------|-----------------------------------------------|
|"img_data"       |"usb_cam or gazebo"                            |
|"weight_path"    |"weight file path"                             |
|"image_topic"    |"탐지할 이미지 rostopic" (usb_cam인 경우 필요X)   |
|"cen_topic"      |"중심점 출력 rostopic"                           |
|"conf"           |"해당 값 이하의 confidence이면  탐지X"            |
|"result_pub"     |"true: 탐지 영상 /yolo/detection_image로 publish"|


## :white_check_mark: Test
- YOLOv8 실행
```shell
roslaunch yolov8_ros yolo_v8.launch
```

## :satellite: Output Rostopic
- Center pose of Bounding box
```shell
rostopic echo /yolo/center
```

