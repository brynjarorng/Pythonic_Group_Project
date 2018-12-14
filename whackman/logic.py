import whackman as w

def calcNewPos(pos, direction, maze):
    newPos = (pos[0] + direction[0], pos[1] + direction[1])
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

def validateNextDir(maze, player):
    newPos = calcNewPos(player.pos, player.nextDir, maze)
    return maze[newPos[1]][newPos[0]] != '|' 

def movePlayer(maze, player):
    newPos = calcNewPos(player.pos, player.moveDir, maze)
    beneath = maze[newPos[1]][newPos[0]] 
    if beneath == '|':
        return player
        
    player.beneath = beneath
    maze[player.pos[1]][player.pos[0]] = '_'
    maze[newPos[1]][newPos[0]] = player.char
    player.pos = newPos
    return player

def updateScore(player):
    if player.beneath == '0':
        player.points += 10
    elif player.beneath == '1':
        player.points += 100
    return player 

def moveGhost(maze, ghost):
    newPos = calcNewPos(ghost.pos, ghost.moveDir, maze)
    beneath = maze[newPos[1]][newPos[0]] 
    
    maze[ghost.pos[1]][ghost.pos[0]] = ghost.beneath
    
    if not beneath.isalpha():
        ghost.beneath = beneath

    maze[newPos[1]][newPos[0]] = ghost.char
    ghost.pos = newPos
    return ghost
