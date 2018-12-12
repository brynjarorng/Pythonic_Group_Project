import whackman as w

def valDown(POS, MAZE):
    return MAZE[POS[1] + 1][POS[0]] == 'N' or MAZE[POS[1] + 1][POS[0]] == 'O' or MAZE[POS[1] + 1][POS[0]] == 'G' or MAZE[POS[1] + 1][POS[0]] == 'Q'
def valUp(POS, MAZE):
    return MAZE[POS[1] - 1][POS[0]] == 'N' or MAZE[POS[1] - 1][POS[0]] == 'O' or MAZE[POS[1] - 1][POS[0]] == 'G' or MAZE[POS[1] - 1][POS[0]] == 'Q'
def valLeft(POS, MAZE):
    return MAZE[POS[1]][POS[0] + 1] == 'N' or MAZE[POS[1]][POS[0] + 1] == 'O' or MAZE[POS[1]][POS[0] + 1] == 'G' or MAZE[POS[1]][POS[0] + 1] == 'Q'
def valRight(POS, MAZE):
    return MAZE[POS[1]][POS[0] - 1] == 'N' or MAZE[POS[1]][POS[0] - 1] == 'O' or MAZE[POS[1]][POS[0] - 1] == 'G' or MAZE[POS[1]][POS[0] - 1] == 'Q'
