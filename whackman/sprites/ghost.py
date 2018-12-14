import pygame as pg
from .Entity import Entity

class Ghost(Entity):
    def __init__(self, img, char, beneath, startPos, moveDir, speed, moveCount):
        super().__init__(img, char, beneath, startPos, moveDir, speed, moveCount)
        self.personality = 0
        self.mode = 0
        self.path = []