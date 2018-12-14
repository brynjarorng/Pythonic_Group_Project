import pygame as pg
import sprites.Entity as BC
import random
from graphAPI import GraphAPI
import math

# 'random' path 
def randomPath(POS, MAZE, pathLength):
    currPath = POS
    selectedPath = [POS]
    for i in range(pathLength):
        availPaths = availablePaths(currPath, MAZE)
        oldPath = selectedPath[len(selectedPath) - 2]
        if oldPath in availPaths and len(availPaths) > 1:
            availPaths.remove(oldPath)
        currPath = availPaths[random.randint(0, len(availPaths) - 1)]
        selectedPath.append(currPath)
    return selectedPath[::-1][:-1]

def availablePaths(POS, MAZE):
    newPos = []
    if POS[0] - 1 >= 0 and MAZE[POS[1] - 1][POS[0]] != '|' and MAZE[POS[1] - 1][POS[0]] != '-':
        newPos.append((POS[0], POS[1] - 1))
    if POS[0] + 1 < len(MAZE) and MAZE[POS[1] + 1][POS[0]] != '|' and MAZE[POS[1] + 1][POS[0]] != '-':
        newPos.append((POS[0], POS[1] + 1))
    if POS[1] - 1 >= 0 and MAZE[POS[1]][POS[0] - 1] != '|' and MAZE[POS[1]][POS[0] - 1] != '-':
        newPos.append((POS[0] - 1, POS[1]))
    if POS[1] + 1 < len(MAZE[0]) and MAZE[POS[1]][POS[0] + 1] != '|' and MAZE[POS[1]][POS[0] + 1] != '-':
        newPos.append((POS[0] + 1, POS[1]))
    return newPos

# distance based shortest path
def distShortPath(ghostPOS, playerPOS, MAZE, pathLength):
    currPath = ghostPOS
    selectedPath = [ghostPOS]
    dist = 0.0
    
    for i in range(pathLength):
        short = 99999999999999999999999999.0
        availPaths = availablePaths(currPath, MAZE)
        # select path
        oldPath = selectedPath[len(selectedPath) - 2]
        if oldPath in availPaths and len(availPaths) > 1:
            availPaths.remove(oldPath)
        for p in availPaths:
            dist = math.sqrt((p[0] - playerPOS[0])**2 + (p[1] - playerPOS[1])**2)
            if dist < short:
                short = dist
                currPath = p

        selectedPath.append(currPath)

    return selectedPath[::-1][:-1]
