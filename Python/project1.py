#!/usr/bin/env python 

import pygame

# Created by Gregory Moncayo
class ItemDropoff(Dropoff)

# Constructor
def __init__(self, room, item, pos):
    super().__init__(room)

    self.Dropoff = item
    self.pos = pos
    self.collision = pygame.Rect(8, 8, 16, 16)

def update(self):
    spr.pos = Drawing.Sprite(self.inventory)
    self.inventory.remove(1)


def can_dropOff(self, player):
    # if items can be dropped off, drop off


