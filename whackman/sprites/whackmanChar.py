import pygame as pg
from .BaseCharacter import BaseCharacter

class WhackmanChar(BaseCharacter):
    def __init__(self, img, char, startPos, size, speed):
        super().__init__(img, char, startPos, size, speed)
        self.moveDir = (0, 0)
        self.nextDir = (0, 0)
        self.points = 0