#!/usr/bin/env python3
import rospy
import time
from geometry_msgs.msg import Twist

#Starts a new node
rospy.init_node('vector_controller', anonymous=True)
velocity_publisher = rospy.Publisher('/vector/cmd_vel', Twist, queue_size=3)
vel_msg = Twist()

time.sleep(5)


def move(speed_input , distance_input, isForward_input):
    speed = int(speed_input)
    distance = int(distance_input)
    isForward = int(isForward_input)
    #Checking if the movement is forward or backwards
    if(isForward):
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)
    #Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    

    #Setting the current time for distance calculus
    tm0 = rospy.Time.now().to_sec()
    current_distance = 0

    #Loop to move the turtle in an specified distance
    while(current_distance < distance):
        #Publish the velocity
        velocity_publisher.publish(vel_msg)
        #Takes actual time to velocity calculus
        tm1=rospy.Time.now().to_sec()
        #Calculates distancePoseStamped
        current_distance= speed*(tm1-tm0)
        
    #After the loop, stops the robot
    vel_msg.linear.x = 0
    #Force the robot to stop
    velocity_publisher.publish(vel_msg)
        

PI = 3.1415926535897

def rotate(speedr_intput, angle_input, clockwise_input): #speedr,angle,clockwise):
    
    # Receiveing the user's input
    #  print("Let's rotate your robot")
    speedr = int(speedr_intput)
    angle = int(angle_input)
    clockwise = int(clockwise_input) #True or false
    
    #Converting from angles to radians
    angular_speed = speedr*2*PI/360
    relative_angle = angle*2*PI/360

    #We wont use linear components
    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    # Checking if our movement is CW or CCW
    if clockwise:
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)
    # Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while(current_angle < relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)
        #print('current_angle: ', current_angle, 't1: ', t1, 't0: ', t0)


    #Forcing our robot to stop
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    #rospy.spin()
 

if __name__ == '__main__':
    try:

        with open('instructions.txt', 'r') as _file:
            raw = _file.read()
        rows = raw.split('\n')
        for inst in rows:
            temp = inst.split(',')
            if temp[0] == 'move':
                move(int(temp[1]),int(temp[2]),int(temp[3]))
                print(temp)
            elif temp[0] == 'rot':
                rotate(int(temp[1]),int(temp[2]),int(temp[3]))
                print(temp)
    except rospy.ROSInterruptException:
        pass


    

