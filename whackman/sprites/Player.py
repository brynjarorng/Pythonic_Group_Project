import pygame as pg
from .Entity import Entity

class Player(Entity):
    def __init__(self, img, char, beneath, startPos, moveDir, speed, moveCount):
        super().__init__(img, char, beneath, startPos, moveDir, speed, moveCount)
        self.nextDir = (0, 0)
        self.points = 0
        self.lives = 3
        self.diedThisGame = False