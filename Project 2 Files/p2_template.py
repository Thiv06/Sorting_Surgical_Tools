## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)


## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------
## Example to rotate the base: arm.rotateBase(90)

# Functions

threshold = 0.55

def iden_pos_func(containter_id, position_list):
    position = position_list[cont_id - 1]
    return position

def move_arm_func(position):
    while True:
        if threshold < arm.emg_left() and threshold < arm.emg_right():
            arm.move_arm(position[0], position[1], position[2])
            break

def control_gripper_func():
    while True:
        if threshold < arm.emg_left() and threshold > arm.emg_right() and arm.effector_position()[1] == 0:
            arm.control_gripper(45)
            # The y coordinate of the arm at the pick up position is 0, so we know to close the gripper at the pick up position.
            break
        
        elif threshold < arm.emg_left() and threshold > arm.emg_right() and arm.effector_position()[1] != 0:
            arm.control_gripper(-45)
            # The y coordinate of the arm at the drop off position is not 0, so we know to open the gripper at the drop off position.
            break

def control_autoclave_func(containter_id):
    while True:
        if threshold > arm.emg_left() and threshold < arm.emg_right() and arm.effector_position()[1] != 0:
            # The y coordinate of the arm at the drop off position is not 0, so we know to open the autoclave drawer.
            if containter_id == 4:
                arm.open_red_autoclave(True)
                break
            
            elif containter_id == 5:
                arm.open_green_autoclave(True)
                break
            
            elif containter_id == 6:
                arm.open_blue_autoclave(True)
                break
        
        elif threshold > arm.emg_left() and threshold < arm.emg_right() and arm.effector_position()[1] == 0:
            # The y coordinate of the arm at the home position is 0, so we know to close the autoclave drawer.
            if containter_id == 4:
                arm.open_red_autoclave(False)
                break
            
            elif containter_id == 5:
                arm.open_green_autoclave(False)
                break
            
            elif containter_id == 6:
                arm.open_blue_autoclave(False)
                break

# Pick up, drop off and home positions

pick_up_pos = [0.5336, 0, 0.0443]
home_pos = [0.4064, 0, 0.4826]

small_red_pos = [-0.63, 0.25, 0.4]
small_green_pos = [0, -0.67, 0.4]
small_blue_pos = [0, 0.67, 0.4]
big_red_pos = [-0.378, 0.1575, 0.3125]
big_green_pos = [0, -0.413, 0.3124]
big_blue_pos = [0, 0.4, 0.3124]

pos_list = [small_red_pos, small_green_pos, small_blue_pos, big_red_pos, big_green_pos, big_blue_pos]

# Random ID generator as a list

import random

cont_id_list = list(range(1, 7))
random.shuffle(cont_id_list)

for cont_id in cont_id_list:
    print("Container ID is:", cont_id)
    arm.spawn_cage(cont_id)
    time.sleep(2)
    
    # Finding drop off position
    drop_off_pos = iden_pos_func(cont_id, pos_list)
    time.sleep(2)

    # Pick up
    move_arm_func(pick_up_pos)
    time.sleep(2)
    control_gripper_func()
    time.sleep(2)
    move_arm_func(home_pos)
    time.sleep(2)

    # Drop off
    move_arm_func(drop_off_pos)
    time.sleep(2)

    # Opening autoclaves for large containers
    if cont_id > 3:
        control_autoclave_func(cont_id)
        time.sleep(2)
    control_gripper_func()
    time.sleep(2)
    arm.home()
    time.sleep(2)

    # Closing autoclaves for large containers
    if cont_id > 3:
        control_autoclave_func(cont_id)
        time.sleep(2)

