import GameBase
import Main
import Characters
import pygame
import Constants
import Drawing
import Entities
import WorldMap
import Items
import Debug
import MainMenu


class Scene(Main.Scene):
    def __init__(self, game):
        super().__init__(game)

        self.dead_timer = 0

        self.game.player.room = self.game.room
        self.game.room.entities.append(self.game.player)

        self.heart_tex = pygame.image.load("res/ui/hearts.png").convert_alpha()
        self.bomb_tex = pygame.image.load("res/ui/bomb.png").convert_alpha()
        self.gold_tex = pygame.image.load("res/ui/gold.png").convert_alpha()
        self.room_icons_tex = pygame.image.load("res/ui/room_icons.png").convert_alpha()
        self.label_font = pygame.font.SysFont("Consolas", 12)
        self.large_font = pygame.font.SysFont("Consolas", 20)

        Entities.fix_textures()

    # movement keys bound
    def update(self):
        if pygame.key.get_pressed()[pygame.K_w]:
            self.game.player.move(GameBase.Direction.UP)
        if pygame.key.get_pressed()[pygame.K_s]:
            self.game.player.move(GameBase.Direction.DOWN)
        if pygame.key.get_pressed()[pygame.K_a]:
            self.game.player.move(GameBase.Direction.LEFT)
        if pygame.key.get_pressed()[pygame.K_d]:
            self.game.player.move(GameBase.Direction.RIGHT)

        mouse_pos = pygame.mouse.get_pos()
        self.game.player.face_point(pygame.math.Vector2(mouse_pos[0], mouse_pos[1]))

        self.game.room.update()
        self.game.room.discovered = self.game.room.visited = True

    # button press events
    def update_event(self, evt):
        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_q or evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
            if self.game.player.use_time < 0:
                self.game.player.selected_item = 0
                self.game.player.use_item()
        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_e or evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 3:
            if self.game.player.use_time < 0:
                self.game.player.selected_item = 1
                self.game.player.use_item()
        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_r or evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 2:
            if self.game.player.use_time < 0:
                self.game.player.selected_item = 2
                self.game.player.use_item()
        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_f:
            if self.game.player.bombs > 0:
                self.game.player.bombs -= 1
                self.game.room.entities.append(Entities.Bomb(self.game.room, pygame.math.Vector2(self.game.player.pos[0] + 16,
                                                                                            self.game.player.pos[1] + 16)))
        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
            self.game.player.interact()

        # Created by Gregory Moncayo
        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_v:
            dropped_item = Entities.ItemPickup(self.game.room, self.game.player.inventory[0])
            dropped_item.pos = pygame.math.Vector2(self.game.player.pos[0] + 16, self.game.player.pos[1] + 16)
            self.game.room.entities.append(dropped_item)
            self.game.player.inventory[0] = None

    # in-game object drawing
    def draw(self, screen):
        self.game.room.draw(screen)

        pygame.draw.rect(screen, Constants.GAME_UI_BG,
                         pygame.Rect(Constants.ROOM_SIZE * Constants.TILE_SIZE, 0,
                                     Constants.GAME_UI_WIDTH, Constants.WINDOW_SIZE[1]),
                         0)

        # Render health
        heart_spr = Drawing.Sprite(self.heart_tex)
        heart_pos = pygame.math.Vector2(Constants.ROOM_SIZE * Constants.TILE_SIZE + 25, 25)
        for h in range(0, int(self.game.player.health_max / 4)):
            # Heart quarters
            subhearts = self.game.player.health - h * 4
            if subhearts < 0:
                subhearts = 0
            elif subhearts > 4:
                subhearts = 4

            # Draw heart
            heart_spr.pos = heart_pos
            heart_spr.subrect = pygame.Rect((4 - subhearts) * 32, 0, 32, 32)
            heart_spr.draw(screen)

            # Prepare position of next heart
            heart_pos.x += 42
            if h % 5 == 4:
                heart_pos.y += 42
                heart_pos.x = Constants.ROOM_SIZE * Constants.TILE_SIZE + 25

        # Draw item slots
        slot = pygame.Rect(Constants.ITEMSLOT_X, Constants.ITEMSLOT_Y, Constants.ITEMSLOT_SIZE, Constants.ITEMSLOT_SIZE)
        slot_top = ["Q", "E", "R"]
        slot_bottom = ["MELEE", "RANGED", "UTILITY"]
        for i in range(0, Constants.ITEMSLOT_COUNT):
            pygame.draw.rect(screen, Constants.ITEMSLOT_BG, slot, 0)
            pygame.draw.rect(screen, Constants.ITEMSLOT_OUTLINE, slot, 1)
            text = Drawing.Text(self.label_font, slot_top[i])
            text.color = Constants.ITEMSLOT_LABEL
            text.pos = pygame.math.Vector2((slot.x + slot.width / 2) - text.get_width() / 2,
                                           slot.y - text.get_height() - Constants.ITEMSLOT_MARGIN_LABEL)
            text.draw(screen)
            text.string = slot_bottom[i]
            text.pos = pygame.math.Vector2((slot.x + slot.width / 2) - text.get_width() / 2,
                                           slot.y + slot.height + Constants.ITEMSLOT_MARGIN_LABEL)
            text.draw(screen)

            if self.game.player.inventory[i] is not None:
                self.game.player.inventory[i].draw_menu(screen, (slot.x + 8, slot.y + 8))
            slot = slot.move(slot.width + Constants.ITEMSLOT_MARGIN_INNER, 0)

        # Draw bomb count
        bomb_spr = Drawing.Sprite(self.bomb_tex)
        bomb_spr.pos = pygame.math.Vector2(Constants.BOMBCOUNT_X, Constants.BOMBCOUNT_Y)
        bomb_spr.draw(screen)
        bomb_label = Drawing.Text(self.label_font, "F")
        bomb_label.color = pygame.Color(255, 255, 255)
        bomb_label.pos = pygame.math.Vector2(bomb_spr.pos.x + (self.bomb_tex.get_width() - bomb_label.get_width()) / 2,
                                             bomb_spr.pos.y - bomb_label.get_height() - Constants.BOMBCOUNT_MARGIN_LABEL)
        bomb_label.draw(screen)
        bomb_label.string = str(self.game.player.bombs)
        bomb_label.pos = pygame.math.Vector2(bomb_spr.pos.x + self.bomb_tex.get_width() - bomb_label.get_width(),
                                             bomb_spr.pos.y + self.bomb_tex.get_height() - bomb_label.get_height())
        bomb_label.draw(screen)

        # Draw gold amount
        gold_spr = Drawing.Sprite(self.gold_tex)
        gold_spr.pos = pygame.math.Vector2(Constants.GOLDAMOUNT_X, Constants.GOLDAMOUNT_Y)
        gold_spr.draw(screen)
        gold_label = Drawing.Text(self.large_font, str(self.game.player.gold))
        gold_label.color = pygame.Color(255, 255, 255)
        gold_label.pos = pygame.math.Vector2(gold_spr.pos.x + self.gold_tex.get_width() + 4, gold_spr.pos.y + 8)
        gold_label.draw(screen)

        # Draw a minimap of some sort
        minimap_bg = pygame.Rect(Constants.MINIMAP_X, Constants.MINIMAP_Y,
                                 Constants.MINIMAP_SIZE, Constants.MINIMAP_SIZE)
        pygame.draw.rect(screen, Constants.MINIMAP_BG, minimap_bg, 0)
        pygame.draw.rect(screen, Constants.MINIMAP_OUTLINE, minimap_bg, 1)

        to_center_x = (Constants.MINIMAP_SIZE - self.game.island.get_size().x * Constants.MINIMAP_ROOM_SIZE) / 2
        to_center_y = (Constants.MINIMAP_SIZE - self.game.island.get_size().y * Constants.MINIMAP_ROOM_SIZE) / 2
        for room in self.game.island.rooms:
            pos = room.pos
            col = pygame.Color(64, 64, 64)
            if not room.discovered:
                continue
            if room.visited:
                col = pygame.Color(128, 128, 128)
            if room.pos == self.game.room.pos:
                col = pygame.Color(196, 196, 196)
            draw_x = Constants.MINIMAP_X + pos.x * Constants.MINIMAP_ROOM_SIZE + to_center_x + 2
            draw_y = Constants.MINIMAP_Y + pos.y * Constants.MINIMAP_ROOM_SIZE + to_center_y + 2
            draw_w = Constants.MINIMAP_ROOM_SIZE - 4
            draw_h = Constants.MINIMAP_ROOM_SIZE - 4
            if 1 in room.neighbors:
                draw_y -= 2
                draw_h += 2
            if 2 in room.neighbors:
                draw_w += 2
            if 3 in room.neighbors:
                draw_h += 2
            if 4 in room.neighbors:
                draw_x -= 2
                draw_w += 2

            pygame.draw.rect(screen, col, pygame.Rect(draw_x, draw_y, draw_w, draw_h), 0)
            if room.type != GameBase.RoomType.NORMAL:
                icon_spr = Drawing.Sprite(self.room_icons_tex)
                icon_spr.subrect = pygame.Rect((room.type.value - 1) * 16, 0, 16, 16)
                icon_spr.pos = pygame.math.Vector2(draw_x + (Constants.MINIMAP_ROOM_SIZE - 16) / 2,
                                                   draw_y + (Constants.MINIMAP_ROOM_SIZE - 16) / 2)
                icon_spr.draw(screen)

        if self.game.player.health <= 0:
            self.dead_timer += 1
            if self.dead_timer >= 180:
                self.dead_timer = 0
                self.game.scene = MainMenu.Scene(self.game)

    def leave_island(self):
        self.game.room.entities.remove(self.game.player)
        self.game.scene = WorldMap.Scene(self.game, False)
        self.game.scene.select_island(self.game.island)
        self.game.room = None
        self.game.island = None
        self.game.player = Characters.Player(self.game, self.game.room)
        self.game.player.pos = pygame.math.Vector2(Constants.ROOM_SIZE * Constants.TILE_SIZE / 2,
                                                   Constants.ROOM_SIZE * Constants.TILE_SIZE / 2)
