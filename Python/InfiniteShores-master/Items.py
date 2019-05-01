import GameBase
import pygame
import Debug
import math
import Entities


class DummyItem(GameBase.Item):
    def __init__(self):
        super().__init__()
        self.tex = pygame.image.load("res/items/sword.png")
        self.tex.set_colorkey((255, 0, 255))

    def display_name(self, char):
        return "Dummy"

    def use(self, char):
        Debug.print("Used dummy item")
        self.rect = char.interact_rect()
        for entity in char.room.entities:
            if not isinstance(entity, GameBase.Character):
                continue
            if entity is not char and entity.get_collision().colliderect(self.rect):
                entity.hurt(char, 1000)

    def during_use(self, char):
        pass

    def finish_using(self, char):
        pass

class BasicMeleeItem(GameBase.Item):
    def __init__(self, name, dmg):
        super().__init__()
        self.tex = pygame.image.load("res/items/" + name + ".png")
        self.tex.set_colorkey((255, 0, 255))

        self.name = name
        self.dmg = dmg

    def display_name(self, char):
        return "Dummy"

    def use(self, char):
        Debug.print("Used " + self.name)
        self.rect = char.interact_rect()
        for entity in char.room.entities:
            if not isinstance(entity, GameBase.Character):
                continue
            if entity is not char and entity.get_collision().colliderect(self.rect):
                entity.hurt(char, self.dmg)

    def during_use(self, char):
        pass

    def finish_using(self, char):
        pass

class BowItem(GameBase.Item):
    def __init__(self):
        super().__init__()
        self.tex = pygame.image.load("res/Weapons/Bow10.PNG")
        self.tex.set_colorkey((255, 0, 255))
        self.type = GameBase.ItemType.RANGED
    
    def display_name(self, char):
        return "Bow"
    
    def use(self, char):
        Debug.print("Used bow")
        angle = math.atan2(char.pos.x - pygame.mouse.get_pos()[0], char.pos.y - pygame.mouse.get_pos()[1])
        bullet = Entities.Bullet(char.room, -angle - 3.14 / 2, 2, False)
        bullet.pos = pygame.math.Vector2(char.pos.x + 12, char.pos.y + 12)
        char.room.entities.append(bullet)

    def during_use(self, char):
        pass
    
    def finish_using(self, char):
        pass
