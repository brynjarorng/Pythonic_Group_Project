import pygame as pg
import sprites.BaseCharacter as BC
import random

# 'random' path 
def randomPath(POS, MAZE, numPaths):
    currPath = POS
    selectedPath = [POS]
    for i in range(numPaths):
        availPaths = availablePaths(currPath, MAZE)
        # select path
        oldPath = selectedPath[len(selectedPath) - 2]
        if oldPath in availPaths and len(availPaths) > 1:
            availPaths.remove(oldPath)
        currPath = availPaths[random.randint(0, len(availPaths) - 1)]
        selectedPath.append(currPath)

    return selectedPath[::-1]

def availablePaths(POS, MAZE):
    newPos = []
    if POS[0] - 1 > 0 and MAZE[POS[1] - 1][POS[0]] != '|':
        newPos.append((POS[0], POS[1] - 1))
    if POS[0] + 1 < len(MAZE) and MAZE[POS[1] + 1][POS[0]] != '|':
        newPos.append((POS[0], POS[1] + 1))
    if POS[1] - 1 > 0 and MAZE[POS[1]][POS[0] - 1] != '|':
        newPos.append((POS[0] - 1, POS[1]))
    if POS[1] + 1 < len(MAZE[0]) and MAZE[POS[1]][POS[0] + 1] != '|':
        newPos.append((POS[0] + 1, POS[1]))
    return newPos

# find shortest path to player