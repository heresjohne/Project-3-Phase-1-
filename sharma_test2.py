# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 22:45:09 2021

@author: sharm
"""

import cv2, math
import numpy as np
from datetime import datetime


# Defining the map
robot_world = np.zeros((300,400), dtype= np.uint8)

# Plotting the obstacles in the map
cv2.circle(robot_world, (90, 229), 35, 255, -1)

cv2.ellipse(robot_world, (246, 154), (60,30), 0, 0, 360, 255, -1)

pts_rect = np.array([[48, 191], [171, 105], [160, 90], [37, 175]], np.int32)
pts_rect = pts_rect.reshape((-1, 1, 2))
cv2.fillPoly(robot_world, [pts_rect], (255, 255, 255), 1)

pts_fig = np.array([[200,20], [200, 70], [230, 70], [230, 60], [210, 60], 
                    [210, 30], [230, 30], [230, 20]], np.int32)
pts_fig = pts_fig.reshape((-1, 1, 2))
cv2.fillPoly(robot_world, [pts_fig], (255, 255, 255), 1)

# Start and end point
initial_coordinate = [30, 30]
final_coordinate = [250, 200]
print('The Initial location of the (center of the) robot is:', initial_coordinate)
print('The Goal location of the (center of the) robot is:', final_coordinate)

initial_center = (initial_coordinate[0], initial_coordinate[1])
final_center = (final_coordinate[0], final_coordinate[1])
radius = 10.0
clearance = 5.0
circlePoints = []


start_time = datetime.now() # To calculate time

# to Calculate Distances
def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

# to get the points at the circumference
def getPoints():
    for i in range(0, 300):
        for j in range(0, 400):
            d = dist((i, j), initial_center)
            if d <= radius + clearance and d > radius + clearance - 2:
                circlePoints.append((i, j))
                
# To check if the move should be made
def isSafe(new_center):
    for point in circlePoints:
        nx = point[0] + (new_center[0] - initial_center[0])
        ny = point[1] + (new_center[1] - initial_center[1])
        if nx < 0 or ny < 0 or nx >= 300 or ny >= 400:
            return False
        if robot_world[nx][ny] == 255:
            return False
    return True

    
# Functions for movements    
def move_up(cc):
    i=cc[0]
    j=cc[1] 
    if i > 0 and i <= 299:
        temp1 = i-1
        temp2 = j
        new_c = (temp1,temp2)
        return new_c
    return None

def move_down(cc):
    i=cc[0]
    j=cc[1]
    if i >= 0 and i < 299:
        temp1 = i+1
        temp2 = j
        new_c = (temp1, temp2)
        return new_c
    return None

def move_left(cc):
    i=cc[0]
    j=cc[1]
    if j > 0 and j <= 399:
        temp1 = i
        temp2 = j-1
        new_c = (temp1, temp2)
        return new_c
    return None

def move_right(cc):
    i=cc[0]
    j=cc[1]
    if j >= 0 and j < 399:
        temp1= i
        temp2= j+1
        new_c = (temp1,temp2)
        return new_c
    return None

def move_up_left(cc):
    i=cc[0]
    j=cc[1]
    if i > 0 and i <=299 and j > 0 and j <=399:
        temp1= i-1
        temp2= j-1
        new_c = (temp1,temp2)
        return new_c
    return None

def move_up_right(cc):
    i=cc[0]
    j=cc[1]
    if i > 0 and i <=299 and j >= 0 and j < 399:
        temp1= i-1
        temp2= j+1
        new_c = (temp1,temp2)
        return new_c
    return None

def move_down_left(cc):
    i=cc[0]
    j=cc[1]
    if i >= 0 and i < 299 and  j > 0 and j <= 399:
        temp1= i+1
        temp2= j-1
        new_c = (temp1,temp2)
        return new_c
    return None

def move_down_right(cc):
    i=cc[0]
    j=cc[1]
    if i >= 0 and i < 299 and j >= 0 and j < 399 :        
        temp1= i+1
        temp2= j+1
        new_c = (temp1,temp2)
        return new_c
    return None


# main function 
nextNode = []
def end_game(start_coordinate):
    startNode = Node(start_coordinate)
    dij = {(start_coordinate[0], start_coordinate[1]) : 0.0}
    visited = set()
    getNode = {(start_coordinate[0], start_coordinate[1]) : startNode}

    print('The movement is possible: ',isSafe(start_coordinate))

    def isGoal(loc): # sub-function to check for the goal
        if loc[0] == final_coordinate[0] and loc[1] == final_coordinate[1]:
            print("\nReached the Goal!")
            print('Cost-to-come:', currentCost)
            return True
        else:
            return False


    while len(dij) > 0:
        currentNode = list(dij.keys())[0]
        currentCost = list(dij.values())[0]
        del dij[currentNode]
        visited.add(currentNode)

        if isGoal(currentNode):
            return getNode[currentNode]
        
        # check if movement is possible and then proceed
        nextNode = move_up(currentNode)
        if nextNode != None and nextNode not in visited:
            if isSafe(nextNode) and nextNode not in dij: # first time
                getNode[nextNode] = Node(nextNode)
                dij[nextNode] = currentCost + 1.0
                getNode[nextNode].parent = getNode[currentNode]
                robot_world[nextNode[0]][nextNode[1]] = 150
                cv2.imshow('Visual', robot_world)
                cv2.waitKey(1)
            elif nextNode in dij:                        # visited
                if currentCost + 1.0 < dij[nextNode]:
                    dij[nextNode] = currentCost + 1.0
                    getNode[nextNode].parent = getNode[currentNode]
        
        nextNode = move_down(currentNode)
        if nextNode != None and nextNode not in visited:
            if isSafe(nextNode) and nextNode not in dij: # first time
                getNode[nextNode] = Node(nextNode)
                dij[nextNode] = currentCost + 1.0
                getNode[nextNode].parent = getNode[currentNode]
                robot_world[nextNode[0]][nextNode[1]] = 150
                cv2.imshow('Visual', robot_world)
                cv2.waitKey(1)
            elif nextNode in dij:
                if currentCost + 1.0 < dij[nextNode]:
                    dij[nextNode] = currentCost + 1.0
                    getNode[nextNode].parent = getNode[currentNode]

        nextNode = move_right(currentNode)
        if nextNode != None and nextNode not in visited:
            if isSafe(nextNode) and nextNode not in dij: # first time
                getNode[nextNode] = Node(nextNode)
                dij[nextNode] = currentCost + 1.0
                getNode[nextNode].parent = getNode[currentNode]
                robot_world[nextNode[0]][nextNode[1]] = 150
                cv2.imshow('Visual', robot_world)
                cv2.waitKey(1)
            elif nextNode in dij:
                if currentCost + 1.0 < dij[nextNode]:
                    dij[nextNode] = currentCost + 1.0
                    getNode[nextNode].parent = getNode[currentNode]
        
        nextNode = move_left(currentNode)
        if nextNode != None and nextNode not in visited:
            if isSafe(nextNode) and nextNode not in dij: # first time
                getNode[nextNode] = Node(nextNode)
                dij[nextNode] = currentCost + 1.0
                getNode[nextNode].parent = getNode[currentNode]
                robot_world[nextNode[0]][nextNode[1]] = 150
                cv2.imshow('Visual', robot_world)
                cv2.waitKey(1)
            elif nextNode in dij:
                if currentCost + 1.0 < dij[nextNode]:
                    dij[nextNode] = currentCost + 1.0
                    getNode[nextNode].parent = getNode[currentNode]
        
        nextNode = move_up_right(currentNode)
        if nextNode != None and nextNode not in visited:
            if isSafe(nextNode) and nextNode not in dij: # first time
                getNode[nextNode] = Node(nextNode)
                dij[nextNode] = currentCost + 1.41
                getNode[nextNode].parent = getNode[currentNode]
                robot_world[nextNode[0]][nextNode[1]] = 150
                cv2.imshow('Visual', robot_world)
                cv2.waitKey(1)
            elif nextNode in dij:
                if currentCost + 1.41 < dij[nextNode]:
                    dij[nextNode] = currentCost + 1.41
                    getNode[nextNode].parent = getNode[currentNode]
        
        nextNode = move_down_right(currentNode)
        if nextNode != None and nextNode not in visited:
            if isSafe(nextNode) and nextNode not in dij: # first time
                getNode[nextNode] = Node(nextNode)
                dij[nextNode] = currentCost + 1.41
                getNode[nextNode].parent = getNode[currentNode]
                robot_world[nextNode[0]][nextNode[1]] = 150
                cv2.imshow('Visual', robot_world)
                cv2.waitKey(1)
            elif nextNode in dij:
                if currentCost + 1.41 < dij[nextNode]:
                    dij[nextNode] = currentCost + 1.41
                    getNode[nextNode].parent = getNode[currentNode]
        
        nextNode = move_up_left(currentNode)
        if nextNode != None and nextNode not in visited:
            if isSafe(nextNode) and nextNode not in dij: # first time
                getNode[nextNode] = Node(nextNode)
                dij[nextNode] = currentCost + 1.41
                visited.add(nextNode)
                getNode[nextNode].parent = getNode[currentNode]
                robot_world[nextNode[0]][nextNode[1]] = 150
                cv2.imshow('Visual', robot_world)
                cv2.waitKey(1)
            elif nextNode in dij:
                if currentCost + 1.41 < dij[nextNode]:
                    dij[nextNode] = currentCost + 1.41
                    getNode[nextNode].parent = getNode[currentNode]
        
        nextNode = move_down_left(currentNode)
        if nextNode != None and nextNode not in visited:
            if isSafe(nextNode) and nextNode not in dij: # first time
                getNode[nextNode] = Node(nextNode)
                dij[nextNode] = currentCost + 1.41
                visited.add(nextNode)
                getNode[nextNode].parent = getNode[currentNode]
                robot_world[nextNode[0]][nextNode[1]] = 150
                cv2.imshow('Visual', robot_world)
                cv2.waitKey(1)
            elif nextNode in dij:
                if currentCost + 1.41 < dij[nextNode]:
                    dij[nextNode] = currentCost + 1.41
                    getNode[nextNode].parent = getNode[currentNode]
        
        dij = dict(sorted(dij.items(), key = lambda item: item[1]))

    return None

# Saving the parent-child details         
class Node(object):
    def __init__(self, coordinate):
        self.config = coordinate
        self.children = []
        self.parent = None

    def add_child(self, obj):
        self.children.append(obj)
        obj.parent = self


getPoints()
goal_node = None

# To check if the Start point and the End point are not in obstacle space
if isSafe(initial_center) == False or isSafe(final_center) == False:
    print("Try again: The robot location is not possible")
else:
    # main function call        
    goal_node = end_game(initial_coordinate)


# Show the optimal path
# Traverse the parents one by one from goal_node till dummy is hit
temp_goal = goal_node
try:
    print('The optimum path from the Goal to Start:')
    while temp_goal.config != initial_coordinate:
        robot_world[temp_goal.config[0]][temp_goal.config[1]] = 50
        temp_goal = temp_goal.parent
        print(temp_goal.config)
        cv2.imshow('Visual', robot_world)
        cv2.waitKey(1)
    robot_world[initial_coordinate[0]][initial_coordinate[1]] = 50
    cv2.destroyAllWindows()
except:
    print("error occured")


end_time = datetime.now()
time_taken = end_time - start_time
print("Time taken to reach the Goal: ", time_taken) 
  

cv2.imshow('Image', robot_world)
cv2.waitKey(0)
cv2.destroyAllWindows()
