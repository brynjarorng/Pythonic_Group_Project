import pygame as pg
from .BaseCharacter import BaseCharacter

class Ghost(BaseCharacter):
    def __init__(self, img, char, beneath, startPos, moveDir, size, speed, moveCount):
        super().__init__(img, char, beneath, startPos, moveDir, size, speed, moveCount)
        self.personality = 0
        self.mode = 0
        self.path = []