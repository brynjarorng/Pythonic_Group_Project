def validateNextDir(maze, player):
    newPos = calcNewPos(maze, player.pos, player.nextDir)
    return maze[newPos[1]][newPos[0]] != '|'

def calcNewPos(maze, pos, moveDir):
    newPos = (pos[0] + moveDir[0], pos[1] + moveDir[1])
    # if trying to index out of the maze go to the other side
    # x
    if newPos[0] >= len(maze[0]):
        newPos = (0, pos[1])
    elif newPos[0] < 0:
        newPos = (len(maze[0]) - 1, pos[1])
    # y
    if newPos[1] >= len(maze):
        newPos = (pos[0], 0)
    elif newPos[1] < 0:
        newPos = (pos[0], len(maze[1]) - 1)
    return newPos

def updateScore(points, beneath):
    if beneath == '0':
        points += 10
    else:
        points += 100
    return points

def moveEntity(maze, entity):
    # Get next postition from ghosts path
    if entity.eType == 'G':
        newPos = entity.path.pop()
    # Player specific actions
    else:
        newPos = calcNewPos(maze, entity.pos, entity.moveDir)
        beneath = maze[newPos[1]][newPos[0]]
        if beneath == '|':          # Dont move into wall
            return
        elif beneath.isdigit():     # Digits are points in maze
            entity.points =  updateScore(entity.points, beneath)
            maze[newPos[1]][newPos[0]] = '_'
        entity.oldPos = entity.pos
    # perform actual movement
    entity.pos = newPos
    entity.moveCount = 0
    return

def checkIfDead(maze, entity, enemies):
    for enemy in enemies:
        if entity.eType == 'P':
            # Player goes head on into ghost
            if entity.pos == enemy.pos and entity.oldPos == enemy.path[-1]:
                entity.lives -= 1
                entity.diedThisGame = True
                entity.pos = (0, 0)
        else:
            # Ghost catches player
            if entity.pos == enemy.pos:
                enemy.lives -= 1
                enemy.diedThisGame = True
                enemy.pos = (0, 0)
    return
