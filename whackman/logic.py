import whackman as w

def calcNewPos(pos, direction):
    newPos = (pos[0] + direction[0], pos[1] + direction[1])
    if newPos == (28, 14):
        newPos = (0, 14)
    return newPos

def validateNextDir(maze, player):
    newPos = calcNewPos(player.pos, player.nextDir)
    return maze[newPos[1]][newPos[0]] != '|' 

def movePlayer(maze, player):
    newPos = calcNewPos(player.pos, player.moveDir)
    beneath = maze[newPos[1]][newPos[0]] 
    if beneath == '|':
        return player
        
    player.beneath = beneath
    maze[player.pos[1]][player.pos[0]] = 'N'
    maze[newPos[1]][newPos[0]] = player.char
    player.pos = newPos
    return player

def updateScore(player):
    if player.beneath == 'O':
        player.points += 10
    elif player.beneath == 'Q':
        player.points += 100
    return player 

def moveGhost(maze, ghost):
    newPos = calcNewPos(ghost.pos, ghost.moveDir)
    beneath = maze[newPos[1]][newPos[0]] 
    maze[ghost.pos[1]][ghost.pos[0]] = ghost.beneath
    ghost.beneath = beneath
    maze[newPos[1]][newPos[0]] = ghost.char
    ghost.pos = newPos
    return ghost

