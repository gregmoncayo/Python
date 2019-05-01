import pygame
import GameBase
import Drawing

class Islander(GameBase.Character):
    def __init__(self, room):
    super.__init__(room)

self.girl = Drawing.sprite(pygame.image.load("res/characters/islandgirl.png"))


#if click on her, she will promptly say something clever to help you
