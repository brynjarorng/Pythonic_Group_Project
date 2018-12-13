import whackman as w

def validateMove(MAZE, PLAYER):
    newPOS = (PLAYER.pos[0] + PLAYER.nextDir[0], PLAYER.pos[1] + PLAYER.nextDir[1])
    if newPOS == (28, 14):
        return True
    return MAZE[newPOS[1]][newPOS[0]] != '|' 

def makeMove(MAZE, PLAYER):
    newPOS = (PLAYER.pos[0] + PLAYER.moveDir[0], PLAYER.pos[1] + PLAYER.moveDir[1])
    if newPOS == (28, 14):
        newPOS = (0, 14)
        MAZE[PLAYER.pos[1]][PLAYER.pos[0]] = 'N'
        MAZE[newPOS[1]][newPOS[0]] = PLAYER.char
        return newPOS
        
    if MAZE[newPOS[1]][newPOS[0]] != '|':
        MAZE[PLAYER.pos[1]][PLAYER.pos[0]] = 'N'
        MAZE[newPOS[1]][newPOS[0]] = PLAYER.char
        return newPOS
    return PLAYER.pos