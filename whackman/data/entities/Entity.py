import pygame as pg

class Entity:
    def __init__(self, img, char, beneath, pos, moveDir, moveCount, speed):
        self.img = img
        self.char = char
        self.beneath = beneath
        self.pos = pos
        self.moveDir = moveDir
        self.speed = speed
        self.moveCount = moveCount