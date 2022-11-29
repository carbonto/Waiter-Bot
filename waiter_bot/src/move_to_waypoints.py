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
from std_msgs.msg import String, UInt8
from pickle_commons import read_pickle_file
import actionlib
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from save_waypoint import SaveWaypointClass
from actionlib_msgs.msg import GoalStatus
from actionlib.msg import TestFeedback, TestResult, TestAction


class MoveBaristaManager(object):

    def __init__(self, barista_feedback_obj,move_max_time=60.0):

        """
        :param barista_feedback_obj:
        :param loadsensor_calibration_obj:
        """

        self._move_max_time = move_max_time
        
        # We do this to allow to have the most updated TableWaypoints
        self._table_waypoints_object = SaveWaypointClass(init_check_for_waypoints=False)
        rospy.logdebug(str(self._table_waypoints_object.get_waypoint_dict()))

        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")

        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))

        self.init_move_to_table_action_server()

        rospy.loginfo("Connected to move base server")

    def get_waypoints_list(self):
        waypoints_dict = self._table_waypoints_object.get_waypoint_dict()
        return list(waypoints_dict.keys())


    def init_move_to_table_action_server(self):
        """
        Initialises the action server and all its variables
        :return:
        """
        self.reset_as_vars()
        self._as_move_ok = True
        self._as_move_msg = ""

        self._feedback = TestFeedback()
        self._result = TestResult()
        self._as = actionlib.SimpleActionServer("/move_to_table_as", TestAction, self.move_to_table_goal_callback, False)
        self._as.start()

    def reset_as_vars(self):
        self._as_flag_check_load_ok = True
        self._as_flag_talk = False
        self._NOTABLE = "NO-TABLE"
        self.table_to_go = self._NOTABLE


    def move_to_table_goal_callback(self, move_to_table_goal):

        """
        This method will wait for commands from the action server
        /move_to_table_as
        :return:
        """
        flag_check_load_ok = self._as_flag_check_load_ok
        flag_talk = self._as_flag_talk

        waypoints_list = self.get_waypoints_list()
        table_name = "T" + str(move_to_table_goal.goal)

        if table_name in waypoints_list:
            self.table_to_go = table_name
            rospy.loginfo("Recieved Table Command to=" + str(self.table_to_go))

            # We retrieve waypoint of the table_name given
            table_waypoint_dict = self._table_waypoints_object.get_waypoint_dict()
            rospy.loginfo("Found " + table_name + "table Waypoint")
            table_waypoint = table_waypoint_dict.get(table_name, "none")
            rospy.logdebug("Table " + str(table_name) + ",P=" + str(table_waypoint))

            # Intialize the waypoint goal
            goal = MoveBaseGoal()

            goal.target_pose.header.frame_id = 'map'
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.pose = table_waypoint.pose

            percentage_path_done = 0
            # build and publish the feedback message
            self._feedback.feedback = percentage_path_done
            self._as.publish_feedback(self._feedback)

            # Send the goal pose to the MoveBaseAction server
            self.move_base.send_goal(goal)

            # Allow 1 minute to get there
            # finished_within_time = self.move_base.wait_for_result(rospy.Duration(60))
            state_result = self.move_base.get_state()
            move_rate = rospy.Rate(20)
            rospy.loginfo("state_result: " + str(state_result))
            init_time = rospy.get_time()
            time_moving = 0


            while state_result <= GoalStatus.ACTIVE and time_moving <= self._move_max_time:
                rospy.logdebug("Moving...Checking Load and Talking....")

                if self._as.is_preempt_requested() or rospy.is_shutdown():
                    rospy.loginfo('The goal has been cancelled/preempted')
                    # the following line, sets the client in preempted state (goal cancelled)
                    self._as.set_preempted()
                    break
                percentage_path_done = int((time_moving / self._move_max_time) * 100)
                self._feedback.feedback = percentage_path_done
                self._as.publish_feedback(self._feedback)

                move_rate.sleep()
                state_result = self.move_base.get_state()
                rospy.logdebug("state_result: " + str(state_result))
                now_time = rospy.get_time()
                time_moving = now_time - init_time

            # If we don't get there in time, abort the goal
            finished_within_time = time_moving < self._move_max_time


            if not finished_within_time:
                self.move_base.cancel_goal()
                msg = "Timed out achieving goal"
                rospy.loginfo(msg)
                self._as.set_preempted()
                self._as_move_ok = False
                self._as_move_msg = msg
            else:
                # We made it! But Ok, or something happened?
                if state_result == GoalStatus.SUCCEEDED:
                    self._result.result = 100
                    msg = 'Goal succeeded!, Percentage Path Done' + str(self._result.result)
                    rospy.loginfo(msg)
                    self._as.set_succeeded(self._result)
                    self._as_move_ok = True
                    self._as_move_msg = msg
                else:
                    msg = "Move DIDN'T succeed..."
                    rospy.logerr(msg)
                    self.move_base.cancel_goal()
                    self._as.set_preempted()
                    self._as_move_ok = False
                    self._as_move_msg = msg
        else:
            msg = "TABLE=" + str(table_name) + ", NOT FOUND in ==>>" + str(waypoints_list)
            rospy.logerr(msg)
            self.table_to_go = self._NOTABLE
            self._as.set_preempted()
            self._as_move_ok = False
            self._as_move_msg = msg

        self.reset_as_vars()


    def wait_for_waypoint_from_as(self, flag_check_load_ok=True, flag_talk=False):
        """
        This methos will wait for commands from the action server
        /move_to_table_as
        :return:
        """
        self._as_flag_check_load_ok = flag_check_load_ok

        self._as_move_ok = True
        self._as_move_msg = ""

        rospy.logwarn("Start Wait for Waypoint Action Server command...")

        wait_rate = rospy.Rate(5)
        rospy.logwarn("Table="+str(self.table_to_go))
        while not rospy.is_shutdown() and self.table_to_go == self._NOTABLE :
            rospy.loginfo("Waiting for Table Order...")
            rospy.logwarn("Table=" + str(self.table_to_go))
            wait_rate.sleep()

        # Now we wait until it returns to its NO-Table state
        rospy.logwarn("Table=" + str(self.table_to_go))
        while not rospy.is_shutdown() and self.table_to_go != self._NOTABLE :
            rospy.loginfo("Waiting for robot to get to table...")
            rospy.logwarn("Table=" + str(self.table_to_go))
            wait_rate.sleep()

        rospy.logwarn("Wait for Waypoint Action Server command Finished...")

        return self._as_move_ok, self._as_move_msg


    def move_to_random_waypoint(self, flag_check_load_ok=True, flag_talk=False):
        """
        Moves to random waypoint form the list
        :return:
        """
        waypoints_list = self.get_waypoints_list()
        random_index = random.randint(0,len(waypoints_list)-1)
        random_name = waypoints_list[random_index]
        rospy.logwarn("Moving to Random Waypoint=====>>>>>>"+str(random_name))
        move_final_result, msg = self.move_to_waypoint(table_name=random_name,
                              flag_check_load_ok=flag_check_load_ok,
                              flag_talk=flag_talk)

        return move_final_result, msg


    def move_to_waypoint(self, table_name, flag_check_load_ok=True, flag_talk=False, flag_as=False):

        # We retrieve waypoint of the table_name given
        table_waypoint_dict = self._table_waypoints_object.get_waypoint_dict()
        if table_name in table_waypoint_dict.keys():
            rospy.loginfo("Found "+table_name+"table Waypoint")
            table_waypoint = table_waypoint_dict.get(table_name, "none")
            rospy.logdebug("Table "+str(table_name)+",P="+str(table_waypoint))
        else:
            error_msgs = "Table "+str(table_name)+" is NOT in Database =>"+str(self._table_waypoints_object)
            rospy.logerr(error_msgs)
            return False, error_msgs

        # Intialize the waypoint goal
        goal = MoveBaseGoal()

        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = table_waypoint.pose
        move_final_result, msg = self.move(goal, flag_check_load_ok, flag_talk)

        return move_final_result, msg



    def move(self, goal, flag_check_load_ok, flag_talk):

        # Send the goal pose to the MoveBaseAction server
        self.move_base.send_goal(goal)

        # Allow 1 minute to get there
        #finished_within_time = self.move_base.wait_for_result(rospy.Duration(60))
        state_result = self.move_base.get_state()
        move_rate = rospy.Rate(20)
        rospy.loginfo("state_result: " + str(state_result))
        init_time = rospy.get_time()
        time_moving = 0
        while state_result <= GoalStatus.ACTIVE and time_moving <= self._move_max_time:
            rospy.logdebug("Moving...Checking Load and Talking....")
            if flag_check_load_ok:
                load_ok, load_msg = self._loadsensor_calibration_obj.check_load_ok()
                if not load_ok:
                    msg = "CHECK LOAD WHILE MOVING ERROR..." + load_msg
                    rospy.logerr(msg)
                    self.move_base.cancel_goal()
                    break

            move_rate.sleep()
            state_result = self.move_base.get_state()
            rospy.logdebug("state_result: " + str(state_result))
            now_time = rospy.get_time()
            time_moving = now_time - init_time

        # If we don't get there in time, abort the goal
        finished_within_time = time_moving < self._move_max_time

        move_final_result = True
        if not finished_within_time:
            self.move_base.cancel_goal()
            move_final_result = False
            msg = "Timed out achieving goal"
            rospy.loginfo(msg)
        else:
            # We made it! But Ok, or something happened?
            if state_result == GoalStatus.SUCCEEDED:
                msg = "Goal succeeded!"
                rospy.loginfo(msg)
            else:
                msg = "Move DIDN'T succeed..."
                rospy.logerr(msg)
                self.move_base.cancel_goal()
                move_final_result = False

        return move_final_result, msg
