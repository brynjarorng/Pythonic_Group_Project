import pygame as pg
from .Entity import Entity

class Player(Entity):
    def __init__(self, img, char, beneath, pos, moveDir, moveCount, speed):
        super().__init__(img, char, beneath, pos, moveDir, moveCount, speed)
        self.nextDir = (0, 0)
        self.points = 0
        self.lives = 3
        self.diedThisGame = False