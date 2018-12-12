import whackman as w

def validateMove(MAZE, POS, nextDir):
    newPOS = (POS[0] + nextDir[0], POS[1] + nextDir[1])
    return MAZE[newPOS[1]][newPOS[0]] != '|' 

def makeMove(MAZE, POS, moveDir):
    newPOS = (POS[0] + moveDir[0], POS[1] + moveDir[1])
    if MAZE[newPOS[1]][newPOS[0]] != '|':
        MAZE[POS[1]][POS[0]] = 'N'
        MAZE[newPOS[1]][newPOS[0]] = 'P'
        return newPOS
    return POS