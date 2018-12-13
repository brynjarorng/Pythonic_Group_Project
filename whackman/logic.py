import whackman as w

def validateMove(MAZE, POS, nextDir):
    newPOS = (POS[0] + nextDir[0], POS[1] + nextDir[1])
    # return false if pos is not inside the array
    if 0 <= newPOS[0] < len(MAZE[0]) and 0 <= newPOS[1] < len(MAZE):
        return MAZE[newPOS[1]][newPOS[0]] != '|' 
    return False

def makeMove(MAZE, POS, moveDir):
    newPOS = (POS[0] + moveDir[0], POS[1] + moveDir[1])
    if MAZE[newPOS[1]][newPOS[0]] != '|':
        MAZE[POS[1]][POS[0]] = 'N'
        MAZE[newPOS[1]][newPOS[0]] = 'P'
        return newPOS
    return POS

def makeMoveGHOST(MAZE, POS, moveDir):
    newPOS = (POS[0] + moveDir[0], POS[1] + moveDir[1])
    if MAZE[newPOS[1]][newPOS[0]] != '|':
        MAZE[POS[1]][POS[0]] = 'N'
        MAZE[newPOS[1]][newPOS[0]] = 'A'
        return newPOS
    return POS