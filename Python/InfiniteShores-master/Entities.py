import pygame
import GameBase
import Drawing
import Debug
import Constants
import math

bomb_tex = pygame.image.load("res/entities/bomb.png")
heart_tex = pygame.image.load("res/entities/heart.png")
heart_container_tex = pygame.image.load("res/entities/heart-container.png")
gold_tex = pygame.image.load("res/entities/gold.png")
pedestal_tex = pygame.image.load("res/entities/shop_pedestal.png")
wall_tex = pygame.image.load("res/wall.png")
ship_tex = pygame.image.load("res/ship_exit.png")

def fix_textures():
    global bomb_tex, heart_tex, heart_container_tex, gold_tex, pedestal_tex, wall_tex, ship_tex
    bomb_tex = bomb_tex.convert_alpha()
    heart_tex = heart_tex.convert_alpha()
    heart_container_tex = heart_container_tex.convert_alpha()
    gold_tex = gold_tex.convert_alpha()
    pedestal_tex = pedestal_tex.convert_alpha()
    wall_tex = wall_tex.convert_alpha()
    ship_tex = ship_tex.convert_alpha()


class Bomb(GameBase.Entity):
    def __init__(self, room, pos):
        super().__init__(room)
        self.pos = pos

        self.fuse = Constants.BOMB_FUSE_LENGTH

    def update(self):
        self.fuse -= 1

        if self.fuse == 0:
            Debug.print("Boom")
            for entity in self.room.entities:
                if not hasattr(entity, "health"):
                    continue
                center = self.get_collision().center
                other_center = entity.get_collision().center
                dist = pygame.math.Vector2(center[0], center[1]).distance_to(pygame.math.Vector2(other_center[0], other_center[1]))
                if dist < 64:
                    entity.hurt(self, 10)

    def draw(self, screen):
        spr = Drawing.Sprite(bomb_tex)
        if self.fuse >= 0:
            spr.pos = pygame.math.Vector2(self.pos.x - 16, self.pos.y - 48)
            spr.subrect = pygame.Rect(int((Constants.BOMB_FUSE_LENGTH - self.fuse) / (180 / 7)) * 32, 0, 32, 64)
            spr.draw(screen)
        else:
            stage = int(self.fuse / -5)
            spr.pos = pygame.math.Vector2(self.pos.x - 16, self.pos.y - 48)
            spr.subrect = pygame.Rect(256 + 32 * stage, 0, 32, 64)
            spr.scale = pygame.math.Vector2(1, 1)
            spr.draw(screen)

    def is_dead(self):
        return self.fuse <= -25


class Pickup(GameBase.Entity):
    def __init__(self, room):
        super().__init__(room)

        self.inactive_timer = 60
        self.picked_up = False

    def update(self):
        super().update()

        if self.inactive_timer > 0:
            self.inactive_timer -= 1

    def on_pickup(self, player):
        self.picked_up = True

    def can_pickup(self, player):
        return not self.picked_up and self.inactive_timer <= 0

    def draw_shop(self, screen, pedestal_pos):
        pass

    def is_dead(self):
        return self.picked_up


class ItemPickup(Pickup):
    def __init__(self, room, item):
        super().__init__(room)

        self.item = item
        self.collision = pygame.Rect(8, 8, 16, 16)

    def draw(self, screen):
        super().draw(screen)
        self.item.draw_world(screen, self.pos)

    def draw_shop(self, screen, pedestal_pos):
        self.item.draw_shop(screen, pedestal_pos)

    def on_pickup(self, player):
        super().on_pickup(player)
        item = player.inventory[self.item.type.value]
        if item is not None:
            item_entity = ItemPickup(self.room, item)
            item_entity.pos = self.pos
            self.room.entities.append(item_entity)
        player.inventory[self.item.type.value] = self.item


class HealthPickup(Pickup):
    def __init__(self, room, amt):
        super().__init__(room)

        self.amt = amt
        self.spr = Drawing.Sprite(heart_tex)
        self.spr.subrect = pygame.Rect((4 - min(4, amt)) * 16, 0, 16, 16)

    def draw(self, screen):
        self.spr.pos = self.pos
        self.spr.draw(screen)

        super().draw(screen)

    def draw_shop(self, screen, pedestal_pos):
        self.spr.pos = pedestal_pos + pygame.math.Vector2(0, -10)
        self.spr.draw(screen)

    def on_pickup(self, player):
        super().on_pickup(player)
        player.health = min(player.health + self.amt, player.health_max)

    def can_pickup(self, player):
        return super().can_pickup(player) and player.health < player.health_max


class GoldPickup(Pickup):
    def __init__(self, room, amt):
        super().__init__(room)

        self.amt = amt
        self.spr = Drawing.Sprite(gold_tex)
        sub = int(math.log2(amt))
        self.spr.subrect = pygame.Rect(sub % 4 * 32, int(sub / 4) * 32, 32, 32)
        self.collision = pygame.Rect(8, 8, 16, 16)

    def draw(self, screen):
        self.spr.pos = self.pos
        self.spr.draw(screen)

        super().draw(screen)

    def on_pickup(self, player):
        super().on_pickup(player)
        player.gold += self.amt


class MaxHealthPickup(Pickup):
    def __init__(self, room):
        super().__init__(room)

        self.spr = Drawing.Sprite(heart_container_tex)

    def draw(self, screen):
        self.spr.pos = self.pos
        self.spr.draw(screen)

        super().draw(screen)

    def on_pickup(self, player):
        super().on_pickup(player)
        player.health += 4
        player.health_max += 4


class BombPickup(Pickup):
    def __init__(self, room):
        super().__init__(room)

        self.spr = Drawing.Sprite(bomb_tex)
        self.spr.subrect = pygame.Rect(0, 0, 32, 64)

    def draw(self, screen):
        self.spr.pos = self.pos
        self.spr.draw(screen)

        super().draw(screen)

    def draw_shop(self, screen, pedestal_pos):
        self.spr.pos = pedestal_pos + pygame.math.Vector2(-8, -48)
        self.spr.draw(screen)

    def on_pickup(self, player):
        super().on_pickup(player)
        player.bombs += 1

class ShopPedestal(GameBase.Entity):
    def __init__(self, room, item, cost):
        super().__init__(room)

        self.item = item
        self.cost = cost

        self.spr = Drawing.Sprite(pedestal_tex)
        self.collision = pygame.Rect(0, 0, 16, 24)

        self.shop_font = pygame.font.SysFont("Consolas", 15)
        self.shop_text = Drawing.Text(self.shop_font, str(cost) + "g")

    def draw(self, screen):
        self.spr.pos = self.pos
        self.spr.draw(screen)

        self.item.draw_shop(screen, self.pos)

        # TODO center this
        self.shop_text.pos = self.pos + pygame.math.Vector2(-16, 32)
        self.shop_text.color = pygame.Color(0, 0, 0)
        self.shop_text.draw(screen)

        super().draw(screen)

    def can_interact(self, player):
        return True

    def on_interact(self, player):
        if player.gold >= self.cost:
            player.gold -= self.cost
            self.item.pos = self.pos
            self.room.entities.append(self.item)
            self.item = None

    def is_dead(self):
        return self.item is None


class ExitShip(GameBase.Entity):
    def __init__(self, room):
        super().__init__(room)

        self.spr = Drawing.Sprite(ship_tex)
        self.collision = pygame.Rect(0, 0, 20, 38)

    def draw(self, screen):
        self.spr.pos = self.pos
        self.spr.draw(screen)

        super().draw(screen)

    def can_interact(self, player):
        return True

    def on_interact(self, player):
        player.game.scene.leave_island()


class Terrain(GameBase.Entity):
    def __init__(self, room, visible = True):
        super().__init__(room)
        self.visible = visible
        if self.visible:
            self.spr = Drawing.Sprite(wall_tex)
        self.collision = pygame.Rect(0, 0, 64, 64)

    def draw(self, screen):
        if self.visible:
            self.spr.pos = self.pos
            self.spr.draw(screen)

        super().draw(screen)


class Bullet(GameBase.Entity):
    def __init__(self, room, direction, damage=2, hostile=True):
        super().__init__(room)
        self.spr = Drawing.Sprite(pygame.image.load("res/bullet.png").convert_alpha())
        self.direction = direction
        self.frame = 0

        self.hostile = hostile
        self.damage = damage
        self.hitSomething = False

        self.anim_counter = 0
        self.pos = pygame.math.Vector2(64 + 48, 120)
        self.prevPos = self.pos

    def draw(self, screen):
        self.spr.pos = self.pos
        self.spr.subrect = pygame.Rect(0, 0, 16, 16)
        self.spr.draw(screen)
        super().draw(screen)

    def moveBullet(self, x, y):
        self.pos.x += math.cos(self.direction) * 3
        self.pos.y += math.sin(self.direction) * 3

    def update(self):
        super().update()
        diff = (self.pos.x - self.prevPos.x, self.pos.y - self.prevPos.y)
        self.anim_counter += math.fabs(diff[0]) + math.fabs(diff[1])
        self.moveBullet(10, 10)
        self.anim_counter += 1
        if self.anim_counter >= 20:
            self.anim_counter = 0
            self.frame += 1
            if self.frame > 2:
                self.frame = 0

        self.prevPos = pygame.math.Vector2(self.pos.x, self.pos.y)

    def on_collide(self, entity):
        if isinstance(entity, Bullet) or isinstance(entity, Bomb) or isinstance(entity, Pickup) or isinstance(entity, ExitShip):
            return

        if self.hostile:
            if hasattr(entity, "hostile") and not entity.hostile and entity.invuln_timer <= 0:
                self.hitSomething = True
                entity.hurt(self, self.damage)
        else:
            if hasattr(entity, "hostile") and entity.hostile:
                self.hitSomething = True
                entity.hurt(self, self.damage)

    def is_dead(self):
        return self.hitSomething or \
               self.pos.x < 0 or self.pos.y < 0 or \
               self.pos.x > Constants.TILE_SIZE * Constants.ROOM_SIZE or self.pos.y > Constants.TILE_SIZE * Constants.ROOM_SIZE