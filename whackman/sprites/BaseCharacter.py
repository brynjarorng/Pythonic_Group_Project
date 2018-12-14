import pygame as pg

class BaseCharacter:
    def __init__(self, img, char, beneath, startPos, moveDir, speed, moveCount):
        self.img = img
        self.char = char
        self.beneath = beneath
        self.pos = startPos
        self.moveDir = moveDir
        self.speed = speed
        self.moveCount = moveCount