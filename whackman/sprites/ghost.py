import pygame as pg
from BaseCharacter import BaseCharacter

class ghost(BaseCharacter):
    def __init__(imgPath, startPos, size, speed):
        super().__init__(imgPath, startPos, size, speed)
        self.personality = 0
        self.mode = 0
        self.path = []