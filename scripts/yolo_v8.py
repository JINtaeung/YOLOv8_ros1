#!/usr/bin/env python3

import cv2
import torch
import rospy
import numpy as np

from ultralytics import YOLO
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point32


rospy.init_node('Yolov8_ros')

def read_cam():
    cap = cv2.VideoCapture(0)
    
    if cap.isOpened():
        cap.set(3, 640) # set width
        cap.set(4, 480) # set height

        while not rospy.core.is_shutdown():
            ref, image = cap.read()
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            
            color_image = np.frombuffer(image.data, dtype=np.uint8).reshape(height, width, -1)
            results = model(color_image, show=False, conf=confidence)

            detect_show(results, height, width)
    else:
        rospy.logerr("Cannot open camera")

def image_callback(image):
    color_image = np.frombuffer(image.data, dtype=np.uint8).reshape(image.height, image.width, -1)
    color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
    results = model(color_image, show=False, conf=confidence)

    detect_show(results, image.height, image.width)

def detect_show(results, height, width):
    frame = results[0].plot()
    fps = 1000.0 / results[0].speed['inference']
    cv2.putText(frame, f'FPS: {int(fps)}', (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
    cen = Point32()
    log = "============================"
    for result in results[0].boxes:
        id = results[0].names[result.cls.item()]
        cen.x = round(result.xywh[0][0].item())
        cen.y = round(result.xywh[0][1].item())
        cen_pub.publish(cen)
        
        log += "\n" + 'class_id: "' + id + '"\n'
        log += "center x: " + str(cen.x) + "\n"
        log += "center y: " + str(cen.y)
    print(log)

    cv2.imshow('YOLOv8', frame)
    cv2.waitKey(3)

    if result_pub:
        publish_image(results[0].plot(), height, width)

def publish_image(frame_raw, height, width):
    image_temp = Image()
    image_temp.height = height
    image_temp.width = width
    image_temp.encoding = 'bgr8'
    image_temp.data = np.array(frame_raw).tobytes()
    image_pub.publish(image_temp)


# load parameters
img_data = rospy.get_param('~img_data', 'usb_cam')
weight_path = rospy.get_param('~weight_path', '')
image_topic = rospy.get_param('~image_topic', '/typhoon_h480/usb_cam/image_raw')
cen_topic = rospy.get_param('~cen_topic', '/yolo/center')
result_pub = rospy.get_param('~result_pub', 'false')
confidence = rospy.get_param('~conf', '0.5')

# Publish
cen_pub = rospy.Publisher(cen_topic, Point32, queue_size=1)
image_pub = rospy.Publisher('/yolo/detection_image', Image, queue_size=1)

# YOLO settings
model = YOLO(weight_path)
if torch.cuda.is_available():
    model.to(0)
else:
    device = "cpu"
color_image = Image()

# use image data
if img_data == 'usb_cam':
    read_cam()
elif img_data == 'gazebo':
    rospy.Subscriber(image_topic, Image, image_callback, queue_size=1, buff_size=52428800)
else:
    rospy.logerr('Wrong img_data parameters, edit yolo_v8.launch')

rospy.spin()