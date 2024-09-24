import rospy
from clover import srv
from std_srvs.srv import Trigger
import cv2
import math
from pyzbar import pyzbar
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from clover import long_callback
from clover.srv import SetLEDEffect
import numpy as np


rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)  # define proxy to ROS-service
image_pub = rospy.Publisher('~debug', Image,  queue_size=1)
bridge = CvBridge()

color = {}

def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

def draw_contour(img, mask, color, name):
    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        box_contor = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(box_contor)
        cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
        cv2.putText(img,name,(x-15,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2)
        return True
    return False

x1=x2=x3=x4=x5=y1=y2=y3=y4=y5=0    
    
def point(name):
    global get_telemetry, x1, x2, x3, x4, x5, y1, y2, y3, y4, y5, color
    telemetry = get_telemetry(frame_id='aruco_map')

    if name == 'stone 1':
        color[name] == 'Brown'
        x1= round(telemetry.x,1)
        y1= round(telemetry.y,1)
        print(x1, y1)

    if name == 'tree 1':
        if x2 == 0 and y2 == 0:
            color[name] == 'Green'
            x2= round(telemetry.x,1)
            y2= round(telemetry.y,1)
            print(name, x2, y2, color)
    
        else:
            color[name] == 'Green'
            x3= round(telemetry.x,1)
            y3= round(telemetry.y,1)
            print(name, x3, y3, color)

    if name == 'tree 2':
        if x2 == 0 and y2 == 0:
            color[name] == 'Green'
            x2= round(telemetry.x,1)
            y2= round(telemetry.y,1)
            print(name, x2, y2, color)

    
        else:
            color[name] == 'Green'
            x3= round(telemetry.x,1)
            y3= round(telemetry.y,1)
            print(name, x3, y3, color)

    if name == 'human':
        color[name] == 'Violet'
        x4= round(telemetry.x,1)
        y4= round(telemetry.y,1)
        print(name, x4, y4, color)

    if name == 'rover':
        color[name] == 'Yellow'
        x5= round(telemetry.x,1)
        y5= round(telemetry.y,1)
        print(name, x5, y5, color)

    


    


def image_callback(msg):
    global color
    img = bridge.imgmsg_to_cv2(msg, 'bgr8')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
    
    stone = cv2.inRange(img_hsv, (1, 120, 150), (97, 180, 230))
    tree1 = cv2.inRange(img_hsv, (160, 220, 180),(190, 255, 255))
    tree2 = cv2.inRange(img_hsv, (160, 220, 180),(190, 255, 255))
    human = cv2.inRange(img_hsv, (125, 100, 100),(175, 150, 180))
    rover = cv2.inRange(img_hsv, (20, 150, 150),(40, 255, 250))
    contours = [
    {'contour': stone, 'color': (255, 0, 0), 'name': 'stone', 'effect': (0, 0, 255)},
    {'contour': tree1, 'color': (19, 69, 139), 'name': 'tree1', 'effect': (139, 69, 19)},
    {'contour': tree2, 'color': (19, 69, 139), 'name': 'tree2', 'effect': (139, 69, 19)},
    {'contour': human, 'color': (0, 128, 0), 'name': 'human', 'effect': (0, 128, 0)},
    {'contour': rover, 'color': (0, 255, 255), 'name': 'rover', 'effect': (255, 255, 0)}
    ]

    for item in contours:
        if draw_contour(img, item['contour'], item['color'], name=item['name']):
            set_effect(r=item['effect'][0], g=item['effect'][1], b=item['effect'][2])
            rospy.sleep(0.2)

            if item['contour'][119][159] == 255:
                # print('1')
                point(name=item['name'])

    
    


    image_pub.publish(bridge.cv2_to_imgmsg(img, 'bgr8'))

image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback, queue_size=1)


set_effect(r=0, g=255, b=0)
navigate_wait(z=0.5, x=1, frame_id='body', auto_arm=True)
set_effect(r=220, g=20, b=60)
navigate_wait(frame_id='aruco_3', x=0, y=0, z=1.5)
rospy.sleep(2)


navigate_wait(x=2, y=0, z=1.5, frame_id='aruco_map')
navigate_wait(x=2, y=5, z=1, frame_id='aruco_map')
navigate_wait(x=4, y=5, z=1, frame_id='aruco_map')
navigate_wait(x=4 , y=0, z=1, frame_id='aruco_map')
navigate_wait(x=6, y=0, z=1, frame_id='aruco_map')
navigate_wait(x=6 , y=5, z=1, frame_id='aruco_map')
navigate_wait(x=3 , y=0, z=1, frame_id='aruco_map')

navigate_wait(frame_id='aruco_3', x=0, y=0, z=1.8)
rospy.sleep(2)
navigate_wait(frame_id='aruco_108', x=0, y=0.5, z=1)
set_effect(r=128, g=0, b=128)
land()



f = open('detect.txt', 'w')
f.write('stone '+str(x1)+' '+str(y1)+' '+str(color.get('stone'))+'\n')
f.write('tree 1 '+str(x2)+' '+str(y2)+' '+str(color.get('tree 1'))+'\n')
f.write('tree 2 '+str(x3)+' '+str(y3)+' '+str(color.get('tree 2'))+'\n')
f.write('human '+str(x4)+' '+str(y4)+' '+str(color.get('human'))+'\n')
f.write('rover '+str(x5)+' '+str(y5)+' '+str(color.get('rover'))+'\n')
f.close()

rospy.spin()





