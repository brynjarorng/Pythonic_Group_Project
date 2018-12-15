import pygame as pg
from .Entity import Entity

class Ghost(Entity):
    def __init__(self, img, char, eType, pos, moveDir, moveCount, speed, chasing):
        super().__init__(img, char, eType, pos, moveDir, moveCount, speed)
        self.path = []
        self.chasing = chasing