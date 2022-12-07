#!/usr/bin/env python3

import os
import sys
import time
import rospy
import numpy
import random
from geometry_msgs.msg import Pose
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest, SpawnModelResponse
from gazebo_msgs.srv import GetModelState, GetModelStateRequest, GetModelStateResponse
from std_srvs.srv import SetBool, SetBoolRequest
from std_msgs.msg import String, UInt8 , Bool
from pickle_commons import read_pickle_file
import actionlib
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from save_waypoint import SaveWaypointClass
from actionlib_msgs.msg import GoalStatus
from actionlib.msg import TestFeedback, TestResult, TestAction
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from visualization_msgs.msg import Marker, MarkerArray

#subcribe to the topic  /saved_waypoints_marker

x = 0
y = 0
theta = 0

def newOdom(msg):
    global x
    global y
    global theta
    global sub
    global homex,homey,mesa1x,mesa1y,mesa2x,mesa2y,mesa3x,mesa3y,mesa4x,mesa4y,mesa5x,mesa5y,mesa6x,mesa6y

    rate = rospy.Rate(10)
    #Posicion Home
    homex = msg.markers[0].pose.position.x
    homey = msg.markers[0].pose.position.y
    #T1
    mesa1x = msg.markers[1].pose.position.x
    mesa1y = msg.markers[1].pose.position.y
    #T2
    mesa2x = msg.markers[2].pose.position.x
    mesa2y = msg.markers[2].pose.position.y
    #T3
    mesa3x = msg.markers[3].pose.position.x
    mesa3y = msg.markers[3].pose.position.y
    #T4
    mesa4x = msg.markers[4].pose.position.x
    mesa4y = msg.markers[4].pose.position.y
    #T5
    mesa5x = msg.markers[5].pose.position.x
    mesa5y = msg.markers[5].pose.position.y
    #T6
    mesa6x = msg.markers[6].pose.position.x
    mesa6y = msg.markers[6].pose.position.y


    #print(x)
    rate.sleep()
    # rot_q = msg.markers[1].pose.orientation
    # (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
#To process theb bumper sensor for simulation load sensor
def processBump(data):
    global bump
    global mesa
    if data.data == 1:
        bump = True
        rospy.loginfo("Bebidas puestas en la mesa")
        rospy.loginfo("Moviendo a destino")
        cliente = ClienteMoveBase()
        if mesa == 0:
            cliente.moveTo(homex,homey)
        elif mesa == 1:
            cliente.moveTo(mesa1x, mesa1y)
        elif mesa == 2:
            cliente.moveTo(mesa2x, mesa2y)
        elif mesa == 3:
            cliente.moveTo(mesa3x, mesa3y)
        elif mesa == 4:
            cliente.moveTo(mesa4x, mesa4y)
        elif mesa == 5:
            cliente.moveTo(mesa5x, mesa5y)
        elif mesa == 6:
            cliente.moveTo(mesa6x, mesa6y)
    else:
        bump = False 
 
def processTable(data):
    global mesa
    mesa = data.data
    rospy.loginfo("Mesa: " + str(mesa))
    rospy.loginfo("Esperando bebidas")
    


class ClienteMoveBase:
    def __init__(self):
        #creamos un cliente ROS para la acción, necesitamos el nombre del nodo 
        #y la clase Python que implementan la acción
        #Para mover al robot, estos valores son "move_base" y MoveBaseAction
        self.client =  actionlib.SimpleActionClient('move_base',MoveBaseAction)
        #esperamos hasta que el nodo 'move_base' esté activo`
        self.client.wait_for_server()

    def moveTo(self, x, y):
        #un MoveBaseGoal es un punto objetivo al que nos queremos mover
        goal = MoveBaseGoal()
        #sistema de referencia que estamos usando
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.pose.position.x = x   
        goal.target_pose.pose.position.y = y
        #La orientación es un quaternion. Tenemos que fijar alguno de sus componentes
        goal.target_pose.pose.orientation.w = 1.0

        #enviamos el goal 
        self.client.send_goal(goal)
        #vamos a comprobar cada cierto tiempo si se ha cumplido el goal
        #get_state obtiene el resultado de la acción 
        state = self.client.get_state()
        #ACTIVE es que está en ejecución, PENDING que todavía no ha empezado
        while state==GoalStatus.ACTIVE or state==GoalStatus.PENDING:
            rospy.Rate(10)   #esto nos da la oportunidad de escuchar mensajes de ROS
            state = self.client.get_state()
        return self.client.get_result()

if __name__ == '__main__':
    global sub
    rospy.init_node("move_waiter")
    #wait for the subscriber to be ready
    sub = rospy.Subscriber("saved_waypoint_markers",MarkerArray, newOdom)
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    pub_bumper = rospy.Publisher('/bumpsi', UInt8, queue_size=1)
    sub_bumper = rospy.Subscriber("/bumpsi",UInt8, processBump)
 
    #To Do: Publicar mesa a través de un topic
    pub_mesa = rospy.Publisher('/mesa', UInt8, queue_size=1)
    sub_mesa = rospy.Subscriber("/mesa",UInt8, processTable)
    cliente = ClienteMoveBase()
    #To Do: Cancelar el movimiento 
    
    
     
        
    rospy.spin()



