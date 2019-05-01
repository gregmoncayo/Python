from enum import Enum
import Drawing
import Debug
import pygame
import Parser
import Constants
import math
import Generation
import random
import Characters

emotes_tex = pygame.image.load("res/emotes.png")


class Direction(Enum):
    DOWN = 0
    RIGHT = 1
    UP = 2
    LEFT = 3


class ItemType(Enum):
    MELEE = 0
    RANGED = 1
    UTILITY = 2


class RoomType(Enum):
    NORMAL = 0
    SHOP = 1
    EXIT = 2
    BOSS = 3

# Parent for all in-room objects
class Entity:
    def __init__(self, room):
        self.room = room
        self.pos = pygame.math.Vector2(0, 0)
        self.collision = pygame.Rect(0, 0, 16, 16)

    def update(self):
        for entity in self.room.entities:
            if self.get_collision().colliderect(entity.get_collision()) and entity is not self:
                self.on_collide(entity)

    def draw(self, screen):
        Debug.draw_collision_rect(self.get_collision())

    def get_collision(self):
        return self.collision.move(self.pos.x, self.pos.y)

    def on_collide(self, entity):
        pass

    def can_interact(self, player):
        return False

    def on_interact(self, player):
        pass

    def is_dead(self):
        return False



class Room:
    def __init__(self, island, pos):
        self.entities = []
        self.island = island
        self.pos = pos
        self.discovered = False
        self.visited = False
        self.type = RoomType.NORMAL

        # Get background textures
        self.map = Parser.main(pos, self.island.width, self.island.length)
        self.tileLib = Parser.tileDict()
        self.tiles = []
        self.drawX = 0
        self.drawY = 0

        # Get room contents
        self.layout = Parser.getLayout(self.type)
        self.layoutLib = Parser.getLayoutLib()

        # Data from generation
        self.neighbors = dict()
        self.gen_Object = Generation.Generation().Room()

        # Apply background textures
        self.bg = pygame.Surface(pygame.math.Vector2(Constants.ROOM_SIZE * Constants.TILE_SIZE,
                                                     Constants.ROOM_SIZE * Constants.TILE_SIZE))
        for element in self.map:
            self.tilesRow = []
            for unit in element:
                tilename = self.tileLib[unit].replace('"', '')
                tilename = random.choice(tilename.split('&'))
                self.image = Drawing.Sprite(pygame.image.load(tilename).convert_alpha())
                self.image.scale = pygame.math.Vector2(64 / self.image.tex.get_width(),
                                                       64 / self.image.tex.get_height())
                self.tilesRow.append(self.image)
            self.tiles.append(self.tilesRow)

        for element in self.tiles:
            for unit in element:
                unit.pos = pygame.math.Vector2(self.drawX, self.drawY)
                unit.draw(self.bg)
                self.drawX += 64
            self.drawY += 64
            self.drawX = 0

        # Apply room contents
        self.drawX = 0
        self.drawY = 0
        for row in self.layout:
            for element in row:
                if element in self.layoutLib:
                    obj = 0
                    if element is "h":
                        obj = Characters.HornetEnemy(self)
                    elif element is "s":
                        obj = Characters.SnakeEnemy(self)
                    obj.pos = pygame.math.Vector2(self.drawX, self.drawY)
                    self.entities.append(obj)
                self.drawX += 64
            self.drawY += 64
            self.drawX = 0


    def update(self):
        for entity in self.entities:
            entity.update()
        self.entities[:] = [x for x in self.entities if not x.is_dead()]

    # TODO draw world
    def draw(self, screen):
        '''for element in self.tiles:
            for unit in element:
                unit.draw(screen)'''
        spr = Drawing.Sprite(self.bg)
        spr.draw(screen)

        for entity in self.entities:
            entity.draw(screen)


# Parent for PC and NPCs
class Character(Entity):
    def __init__(self, room):
        super().__init__(room)
        self.inventory = [None, None, None]
        self.selected_item = 0
        self.use_time = -1
        self.facing = Direction.DOWN
        self.collision = pygame.Rect(0, 0, 32, 32)
        self.health = self.health_max = 4
        self.speed = 2
        self.hostile = False
        self.invuln_timer = 0

        self.emote_spr = None
        self.emote_time = 0
        self.emote_offset = pygame.math.Vector2(0, 48)

    def update(self):
        super().update()
        if self.use_time >= 0:
            if self.inventory[self.selected_item] is not None:
                self.inventory[self.selected_item].during_use(self)
            self.use_time -= 1
            if self.use_time < 0 and self.inventory[self.selected_item] is not None:
                self.inventory[self.selected_item].finish_using(self)

        if self.invuln_timer > 0:
            self.invuln_timer -= 1

    def draw(self, screen):
        super().draw(screen)

        if self.use_time >= 0 and self.inventory[self.selected_item] is not None:
            self.inventory[self.selected_item].draw(screen, self)

        if self.emote_time > 0:
            self.emote_time -= 1
            self.emote_spr.pos = self.pos - self.emote_offset
            self.emote_spr.draw(screen)

    def move(self, direction):
        if direction == Direction.UP:
            self.pos.y -= self.speed
        elif direction == Direction.DOWN:
            self.pos.y += self.speed
        elif direction == Direction.LEFT:
            self.pos.x -= self.speed
        elif direction == Direction.RIGHT:
            self.pos.x += self.speed

        self.facing = direction

        # player_room_hook in Characters.py
        # I assume this lets the player leave rooms?
        if self.pos.x < 0:
            self.pos.x = 0
            if hasattr(self, "player_room_hook"):
                self.player_room_hook(pygame.math.Vector2(-1, 0))
            else:
                self.on_collide(Direction.LEFT)
        elif self.pos.x > Constants.ROOM_SIZE * Constants.TILE_SIZE - self.get_collision().width:
            self.pos.x = Constants.ROOM_SIZE * Constants.TILE_SIZE - self.get_collision().width
            if hasattr(self, "player_room_hook"):
                self.player_room_hook(pygame.math.Vector2(1, 0))
            else:
                self.on_collide(Direction.RIGHT)
        if self.pos.y < 0:
            self.pos.y = 0
            if hasattr(self, "player_room_hook"):
                self.player_room_hook(pygame.math.Vector2(0, -1))
            else:
                self.on_collide(Direction.UP)
        elif self.pos.y > Constants.ROOM_SIZE * Constants.TILE_SIZE - self.get_collision().height:
            self.pos.y = Constants.ROOM_SIZE * Constants.TILE_SIZE - self.get_collision().height
            if hasattr(self, "player_room_hook"):
                self.player_room_hook(pygame.math.Vector2(0, 1))
            else:
                self.on_collide(Direction.DOWN)

    def is_dead(self):
        return self.health <= 0

    def on_death(self):
        pass

    def hurt(self, source, amt):
        # Enemies don't get invulnerability
        if not self.hostile and self.invuln_timer > 0:
            return
        self.invuln_timer = 50

        prev_health = self.health
        self.health = min(max(0, self.health - amt), self.health_max)
        if prev_health > 0 and self.health <= 0:
            self.on_death()

    def use_item(self):
        item = self.inventory[self.selected_item]
        if item is not None:
            item.use(self)
            self.use_time = item.use_time()

    def interact_rect(self):
        if self.facing == Direction.DOWN:
            return self.get_collision().move(0, self.get_collision().height)
        elif self.facing == Direction.UP:
            return self.get_collision().move(0, -self.get_collision().height)
        elif self.facing == Direction.RIGHT:
            return self.get_collision().move(self.get_collision().width, 0)
        elif self.facing == Direction.LEFT:
            return self.get_collision().move(-self.get_collision().width, 0)

        Debug.log("Bad facing dir?")
        return None

    def interact(self):
        check = self.interact_rect()

        for entity in self.room.entities:
            if entity.can_interact(self) and check.colliderect(entity.get_collision()):
                Debug.print("Interact w/ " + entity.__class__.__name__)
                entity.on_interact(self)
                break

    def emote(self, index, time=60):
        self.emote_time = time
        self.emote_spr = Drawing.Sprite(emotes_tex)
        self.emote_spr.subrect = pygame.Rect(index % 10 * 16, int(index / 10) * 16, 16, 16)
        self.emote_spr.scale = pygame.math.Vector2(2, 2)

    def face_point(self, point):
        deg = math.degrees(math.atan2(self.pos.y - point.y, self.pos.x - point.x))
        deg += 180 + 45
        if deg >= 360:
            deg -= 360
        self.facing = Direction((3 - int(deg / 90) + 2) % 4)


# Parent for usable items
class Item:
    def __init__(self):
        self.tex = None
        self.type = ItemType.MELEE
        pass

    def display_name(self, char):
        return None

    def use_time(self):
        return 30

    def draw(self, screen, char):
        if self.tex is None:
            return

        spr = Drawing.Sprite(self.tex)
        spr.pos = pygame.math.Vector2(char.get_collision().center[0], char.get_collision().center[1])
        spr.origin = pygame.math.Vector2(self.tex.get_width() / 2, self.tex.get_height() / 2)

        if char.facing == Direction.UP:
            spr.pos.y -= 24
            spr.rotation = 270
        elif char.facing == Direction.DOWN:
            spr.pos.y += 24
            spr.rotation = 90
        elif char.facing == Direction.LEFT:
            spr.pos.x -= 24
            spr.rotation = 0
        elif char.facing == Direction.RIGHT:
            spr.pos.x += 24
            spr.rotation = 180

        spr.draw(screen)

    def draw_menu(self, screen, pos):
        spr = Drawing.Sprite(self.tex)
        spr.pos = pos

        spr.draw(screen)

    def draw_world(self, screen, pos):
        spr = Drawing.Sprite(self.tex)
        spr.pos = pos

        spr.draw(screen)

    def draw_shop(self, screen, pedestal_pos):
        spr = Drawing.Sprite(self.tex)
        spr.pos = pedestal_pos + pygame.math.Vector2(-8, -20)

        spr.draw(screen)

    def use(self, char):
        pass

    def during_use(self, char):
        pass

    def finish_using(self, char):
        pass
