import pygame as pg
from .BaseCharacter import BaseCharacter

class WhackmanChar(BaseCharacter):
    def __init__(self, img, char, beneath, startPos, moveDir, speed, moveCount):
        super().__init__(img, char, beneath, startPos, moveDir, speed, moveCount)
        self.nextDir = (0, 0)
        self.points = 0