import pygame as pg
import sprites.BaseCharacter as BC
import random

# random path 
def randomPath(POS, MAZE, numPaths):
    prevPos = POS
    newPos = availablePaths(POS, MAZE)
    posList = [POS]
    for i in range(numPaths):
        selectedNewPos = newPos[random.randint(0, len(newPos) - 1)]
        if len(newPos) == 1:
            posList.append(selectedNewPos)
            newPos = availablePaths(posList[len(posList) - 1], MAZE)
            prevPos = posList[len(posList) - 1]
        else:
            if prevPos in newPos:
                newPos.remove(prevPos)
            newPos[random.randint(0, len(newPos) - 1)]
            posList.append(selectedNewPos)
            newPos = availablePaths(posList[len(posList) - 1], MAZE)
            prevPos = posList[len(posList) - 1]        
    return posList[1:]



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