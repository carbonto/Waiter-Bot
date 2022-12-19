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
from kivymd.app import MDApp
from kivy.lang import Builder
import webbrowser


def process_table(data):
    global mesa
    mesa = data.data
    rospy.loginfo("Mesa: " + str(mesa))
    Interfaz().screen.ids.estado.text = "Yendo a mesa " + str(mesa)
def process_estado(data):
    global estado
    estado = data.status
def proccess_load_food(data):
    global load_food
    load_food = data.data
class Interfaz(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.screen = Builder.load_file('ros_gui.kv') # load the kv file
        
    def build(self):
        return self.screen

    def load_food(self,*args):
        rospy.loginfo("Loading food")
        msg = 1
        pub_bumper.publish(msg)
        self.screen.ids.load_food.text = "Food loaded"
        rospy.loginfo("Food loaded")
    def unload_food(self,*args):
        rospy.loginfo("Unloading food")
        msg = 0
        pub_bumper.publish(msg)
        self.screen.ids.load_food.text = "Load food"
        rospy.loginfo("Food unloaded")
    def home(self,*args):
        rospy.loginfo("Going home")
        msg = 0
        pub_mesa.publish(msg)
    def table1(self,*args):
        rospy.loginfo("Going to table 1")
        msg = 1
        pub_mesa.publish(msg)
    def table2(self,*args):
        rospy.loginfo("Going to table 2")
        msg = 2
        pub_mesa.publish(msg)
    def table3(self,*args):
        rospy.loginfo("Going to table 3")
        msg = 3
        pub_mesa.publish(msg)
    def table4(self,*args):
        rospy.loginfo("Going to table 4")
        msg = 4
        pub_mesa.publish(msg)
    def table5(self,*args):
        rospy.loginfo("Going to table 5")
        msg = 5
        pub_mesa.publish(msg)
    def table6(self,*args):
        rospy.loginfo("Going to table 6")
        msg = 6
        pub_mesa.publish(msg)
    def cancel(self,*args):
        rospy.loginfo("Cancelado movimiento")
        pub_cancel2.cancel_all_goals()
    def camara(self,*args):
        url = 'http://localhost:8080/stream?topic=/camera/rgb/image_raw&type=ros_compressed'
        webbrowser.open(url)
    #     #App().get_running_app().stop()
    def estado(self,*args):
        global mesa, estado,load_food
        if estado == 1 and load_food == 1:
            self.screen.ids.estado.text = "Yendo a mesa " + str(mesa)
        elif estado == 3:
            self.screen.ids.estado.text = "Llegado a mesa"
            if load_food == 0:
                self.screen.ids.estado.text = "Bebidas retiradas"
        elif estado == 4:
            self.screen.ids.estado.text = "Cancelado"
        elif estado == 1 and mesa == 0:
            self.screen.ids.estado.text = "Yendo a home"

    #status 1 es yendo mesa y estatus 3 es que ha llegado a la mesa
    #En cada funcion de mesa se publica el numero de mesa a la que se va
    #En cancelar tambien publica que se ha cancelado el movimiento 
    #Con funcion aparte se dice si ha llegado o no 
#main



if __name__ == '__main__':

    pub_bumper = rospy.Publisher('/bumpsi', UInt8, queue_size=1)
    sub_bumper = rospy.Subscriber('/bumpsi', UInt8,proccess_load_food)
    sub_mesa = rospy.Subscriber('/mesa', UInt8,process_table)
    pub_mesa = rospy.Publisher('/mesa', UInt8, queue_size=1)
    pub_cancel = rospy.Publisher('/move_base/cancel',GoalID,queue_size=1)
    pub_cancel2 = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    sub_estado = rospy.Subscriber('/move_base/status',GoalStatus,process_estado)
    rospy.init_node('Interfaz',anonymous=True)
    # url = 'http://google.com'
    # webbrowser.open(url)
    Interfaz().run()
