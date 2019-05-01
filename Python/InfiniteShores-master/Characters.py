import pygame
import GameBase
import Drawing
import math
import Items
import Entities
import Debug
import Constants
import random


def drop_pickup(room, pickup, pos):
    pickup.pos = pygame.math.Vector2(pos.x, pos.y)
    room.entities.append(pickup)


def drop_item(room, item, pos):
    pickup = Entities.ItemPickup(room, item)
    drop_pickup(room, pickup, pos)


def drop_health(room, amt, pos):
    pickup = Entities.HealthPickup(room, amt)
    drop_pickup(room, pickup, pos)


def drop_gold(room, amt, pos):
    pickup = Entities.GoldPickup(room, amt)
    drop_pickup(room, pickup, pos)


class Player(GameBase.Character):
    def __init__(self, game, room):
        super().__init__(room)
        self.game = game

        self.spr = Drawing.Sprite(pygame.image.load("res/player.png").convert_alpha())
        self.frame = 0

        self.anim_counter = 0
        self.prevPos = self.pos

        self.gold = 0
        self.bombs = 3

        self.health = self.health_max = 12
        self.hostile = False

        self.player_room_hook = self.collide_exit

        self.inventory[0] = Items.BasicMeleeItem("dagger", 1)

    def update(self):
        super().update()

        diff = (self.pos.x - self.prevPos.x, self.pos.y - self.prevPos.y)
        self.anim_counter += math.fabs(diff[0]) + math.fabs(diff[1])
        while self.anim_counter > 10:
            self.frame = (self.frame + 1) % 4
            self.anim_counter -= 10

        self.prevPos = pygame.math.Vector2(self.pos.x, self.pos.y)

    def draw(self, screen):
        # using direction of player to find location of frame on image
        if self.facing == GameBase.Direction.UP:
            super().draw(screen)

        # select specific frame in image
        self.spr.subrect = pygame.Rect(self.facing.value * 32, self.frame * 32, 32, 32)
        self.spr.pos = pygame.math.Vector2(int(self.pos.x) - 16, int(self.pos.y) - 16)
        self.spr.scale = pygame.math.Vector2(2, 2)

        if self.invuln_timer == 0 or int(self.invuln_timer / 20) % 2 == 1:
            self.spr.draw(screen)

        if self.facing != GameBase.Direction.UP:
            super().draw(screen)

        Debug.draw_player_interact_rect(self.interact_rect())

    # picks up Entities.Pickup objects on contact
    def on_collide(self, entity):
        if isinstance(entity, Entities.Pickup) and entity.can_pickup(self):
            entity.on_pickup(self)
        # Collisions
        elif not isinstance(entity, Entities.Pickup):
            myColl = self.get_collision()
            myPrevColl = self.get_collision()
            myPrevColl = myPrevColl.move(-self.pos.x + self.prevPos.x, -self.pos.y + self.prevPos.y)

            otherColl = entity.get_collision()
            if myColl.left < otherColl.right <= myPrevColl.left:
                self.pos.x += otherColl.right - myColl.left
            elif myPrevColl.right <= otherColl.left < myColl.right:
                self.pos.x -= myColl.right - otherColl.left

            if myColl.top < otherColl.bottom <= myPrevColl.top:
                self.pos.y += otherColl.bottom - myColl.top
            elif myPrevColl.bottom <= otherColl.top < myColl.bottom:
                self.pos.y -= myColl.bottom - otherColl.top

    # checking to shift rooms
    def collide_exit(self, room_offset):
        next_room_pos = self.room.pos + room_offset
        next_room = self.room.island.get_room_at(next_room_pos)
        if next_room is not None:
            self.room.entities.remove(self)
            self.game.room = next_room
            self.room = next_room
            self.game.room.entities.append(self)
            if room_offset == pygame.math.Vector2(1, 0):
                self.pos.x = 0
            elif room_offset == pygame.math.Vector2(-1, 0):
                self.pos.x = Constants.ROOM_SIZE * Constants.TILE_SIZE - self.get_collision().width
            if room_offset == pygame.math.Vector2(0, 1):
                self.pos.y = 0
            elif room_offset == pygame.math.Vector2(0, -1):
                self.pos.y = Constants.ROOM_SIZE * Constants.TILE_SIZE - self.get_collision().height


class Shopkeeper(GameBase.Character):
    def __init__(self, room):
        super().__init__(room)

        self.spr = Drawing.Sprite(pygame.image.load("res/characters/shopkeeper.png").convert_alpha())
        self.frame = 0

        self.anim_counter = 0

        self.health = self.maxhealth = 20

    def update(self):
        super().update()

        self.anim_counter += 1
        if self.anim_counter >= 20:
            self.anim_counter = 0
            self.frame += 1
            if self.frame > 2:
                self.frame = 0

    def draw(self, screen):
        self.spr.subrect = pygame.Rect(self.frame * 24, self.facing.value * 32, 24, 32)
        self.spr.pos = pygame.math.Vector2(int(self.pos.x) - 8, int(self.pos.y) - 16)
        self.spr.scale = pygame.math.Vector2(2, 2)
        self.spr.draw(screen)

        super().draw(screen)


class Enemy(GameBase.Character):
    def __init__(self, room, tex, frameCount=3, frameSize=64):
        super().__init__(room)
        self.spr = Drawing.Sprite(pygame.image.load("res/characters/" + tex + ".png").convert_alpha())
        self.frame = 0
        self.frameCount = frameCount
        self.frameSize = frameSize
        self.animInterval = 10

        self.animAlways = False;
        self.anim_counter = 0
        self.prevPos = self.pos

        self.health = self.health_max = 12
        self.hostile = True

    def update(self):
        super().update()

        if self.invuln_timer <= 0:
            self.ai()

        if self.animAlways:
            self.anim_counter += 1
            if self.anim_counter >= self.animInterval:
                self.anim_counter = 0
                self.frame += 1
                if self.frame > self.frameCount - 1:
                    self.frame = 0
        else:
            diff = (self.pos.x - self.prevPos.x, self.pos.y - self.prevPos.y)
            self.anim_counter += math.fabs(diff[0]) + math.fabs(diff[1])
            while self.anim_counter > self.animInterval:
                self.frame = (self.frame + 1) % self.frameCount
                self.anim_counter -= self.animInterval

        self.prevPos = pygame.math.Vector2(self.pos.x, self.pos.y)

    def draw(self, screen):
        self.spr.subrect = pygame.Rect(self.frame * self.frameSize, self.facing.value * self.frameSize, self.frameSize,
                                       self.frameSize)
        self.spr.pos = self.pos - pygame.Vector2(16, 32)
        self.spr.draw(screen)

        super().draw(screen)

    def ai(self):
        pass


class SnakeEnemy(Enemy):
    def __init__(self, room):
        super().__init__(room, "snake")

        self.facing = random.choice(
            [GameBase.Direction.UP, GameBase.Direction.DOWN, GameBase.Direction.LEFT, GameBase.Direction.RIGHT])
        self.speed = 1
        self.health = self.health_max = 3

    def on_collide(self, entity):
        if isinstance(entity, Entities.Terrain) or \
                entity is GameBase.Direction.UP or entity is GameBase.Direction.DOWN or \
                entity is GameBase.Direction.LEFT or entity is GameBase.Direction.RIGHT:
            if self.facing is GameBase.Direction.UP:
                self.facing = GameBase.Direction.DOWN
                self.move(self.facing)
            elif self.facing is GameBase.Direction.DOWN:
                self.facing = GameBase.Direction.UP
                self.move(self.facing)
            elif self.facing is GameBase.Direction.RIGHT:
                self.facing = GameBase.Direction.LEFT
                self.move(self.facing)
            elif self.facing is GameBase.Direction.LEFT:
                self.facing = GameBase.Direction.RIGHT
                self.move(self.facing)

    def ai(self):
        self.move(self.facing)

    def on_death(self):
        drop_gold(self.room, random.randint(1, 5), self.pos)


class HornetEnemy(Enemy):
    def __init__(self, room):
        super().__init__(room, "hornet")

        self.animAlways = True
        self.facing = random.choice(
            [GameBase.Direction.UP, GameBase.Direction.DOWN, GameBase.Direction.LEFT, GameBase.Direction.RIGHT])
        self.speed = 0
        self.bulletTimer = 0
        self.health = self.health_max = 5

    def ai(self):
        player = None
        for entity in self.room.entities:
            if isinstance(entity, Player):
                player = entity
                break
        if player is None:
            return

        self.face_point(player.pos)

        self.bulletTimer += 1
        if self.bulletTimer >= 120:
            self.bulletTimer = 0
            angle = math.atan2(player.pos.y - self.pos.y, player.pos.x - self.pos.x)
            bullet = Entities.Bullet(self.room, angle)
            bullet.pos = pygame.math.Vector2(self.pos.x, self.pos.y)
            self.room.entities.append(bullet)

    def on_death(self):
        drop_gold(self.room, random.randint(3, 7), self.pos)


class WizardEnemy(Enemy):
    def __init__(self, room):
        super().__init__(room, "wizard", 3, 48)

        self.animAlways = False
        self.speed = 0
        self.bulletTimer = 0
        self.health = self.health_max = 9
        self.bulletCounter = 0
        self.spr.scale = pygame.math.Vector2(2, 2)
        self.spr.origin = pygame.math.Vector2(8, 16)

    def ai(self):
        player = None
        for entity in self.room.entities:
            if isinstance(entity, Player):
                player = entity
                break
        if player is None:
            return

        self.face_point(player.pos)

        self.bulletTimer += 1
        if self.bulletTimer >= 75:
            self.bulletTimer = 0
            angle = math.atan2(player.pos.y - self.pos.y, player.pos.x - self.pos.x)
            bullet = Entities.Bullet(self.room, angle, 3)
            bullet.pos = pygame.math.Vector2(self.pos.x, self.pos.y)
            self.room.entities.append(bullet)
            self.bulletCounter += 1
            if self.bulletCounter == 3:
                self.teleport()
                self.bulletCounter = 0

    def hurt(self, source, amt):
        super().hurt(source, amt)
        self.teleport()

    def on_death(self):
        drop_pickup(self.room, Entities.MaxHealthPickup(self.room), self.pos)
        drop_gold(self.room, random.randint(15, 25),
                  self.pos + pygame.math.Vector2(random.randint(-16, 16), random.randint(-16, 16)))

    def teleport(self):
        self.pos.x = random.randint(1 * Constants.TILE_SIZE,
                                    (Constants.ROOM_SIZE - 1) * Constants.TILE_SIZE - self.get_collision().width)
        self.pos.y = random.randint(1 * Constants.TILE_SIZE,
                                    (Constants.ROOM_SIZE - 1) * Constants.TILE_SIZE - self.get_collision().height)
