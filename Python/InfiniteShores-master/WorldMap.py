import pygame
import Main
import GameBase
import Debug
import Constants
import Drawing
import random
import gibberish
import Entities
import Characters
import Items
import Game
import Generation

water_tex = pygame.image.load("res/sea.png")
scroll_tex = pygame.image.load("res/ui/scroll_featurename.png")
selector_tex = pygame.image.load("res/ui/sea_selection.png")


def make_store_pedestal(room, pos):
    items = [Entities.ItemPickup(room, Items.BasicMeleeItem("sword", 2)),
             Entities.ItemPickup(room, Items.BasicMeleeItem("cutlass", 3)),
             Entities.ItemPickup(room, Items.BowItem()),
             Entities.HealthPickup(room, random.randint(1, 5)),
             Entities.BombPickup(room) ]
    items[0].cost = 35
    items[1].cost = 75
    items[2].cost = 75
    items[3].cost = items[3].amt * 7
    items[4].cost = 20
    item = random.choice(items)
    pedestal = Entities.ShopPedestal(room, item, item.cost)
    pedestal.pos = pos
    room.entities.append(pedestal)

# 10/31 - some comments added by Dom

class Island:
    def __init__(self, pos, name):
        self.pos = pos
        self.name = name
        self.rooms = []
        self.length = 0
        self.width = 0

        self.start_room = None
        self.start_pos = pygame.math.Vector2(5, 5) * Constants.TILE_SIZE

    def get_room_at(self, pos):
        for room in self.rooms:
            if room.pos == pos:
                return room
        return None

    def get_size(self):
        w = 0
        h = 0
        for room in self.rooms:
            w = max(w, room.pos.x + 1)
            h = max(h, room.pos.y + 1)

        return pygame.math.Vector2(w, h)

    def scout(self):
        for room in self.rooms:
            room.discovered = True


class Sea:
    def __init__(self, name):
        self.name = name

        self.islands = {}

        if name == "Test":
            self.generate_sea_test()
        else:
            self.generate_sea()

    def generate_sea_test(self):
        # implementing Generation.py
        gen = Generation.Generation()
        gen.make()
        while not gen.isComplete():
            del gen
            print("Generation failed, remaking...")
            gen = Generation.Generation()
            gen.make()
        gen.printRooms()


        # island is at (3, 3)
        test = Island(pygame.math.Vector2(3, 3), "Test")
        self.islands[str(test.pos)] = test

        #
        # Test island generation
        #
        x, y = 0, 0
        shop_exists = False
        # Loop for each room on Generated island
        for row in gen.rows:
            for room in row:
                if room.iter_num is 6 and not shop_exists:
                    room_shop = GameBase.Room(test, pygame.math.Vector2(y, x))
                    room_shop.neighbors = room.neighbors
                    room_shop.gen_Object = room
                    shop_exists = True
                    # print ("shop at " + str(y) + ", " + str(x))
                elif room.iter_num is 1:
                    room_pickups = GameBase.Room(test, pygame.math.Vector2(y, x))
                    room_pickups.neighbors = room.neighbors
                    room_pickups.gen_Object = room
                    # print ("start at " + str(y) + ", " + str(x))
                elif room.iter_num is 2:
                    room_creation = GameBase.Room(test, pygame.math.Vector2(y, x))
                    room_creation.neighbors = room.neighbors
                    room_creation.gen_Object = room
                elif room.iter_num is 3:
                    room_enemies = GameBase.Room(test, pygame.math.Vector2(y, x))
                    room_enemies.neighbors = room.neighbors
                    room_enemies.gen_Object = room
                elif room.iter_num is 4:
                    room_boss = GameBase.Room(test, pygame.math.Vector2(y, x))
                    room_boss.neighbors = room.neighbors
                    room_boss.gen_Object = room
                else:
                    empty_room = GameBase.Room(test, pygame.math.Vector2(y, x))
                    empty_room.neighbors = room.neighbors
                    empty_room.gen_Object = room
                    # print ("empty at " + str(y) + ", " + str(x))
                    test.rooms.append(empty_room)
                y += 1
            x += 1
            y = 0

        # pickups room
        # places stuff in room_pickups
        ship = Entities.ExitShip(room_pickups)
        ship.pos = pygame.math.Vector2(Constants.TILE_SIZE * Constants.ROOM_SIZE / 2,
                                       Constants.TILE_SIZE * Constants.ROOM_SIZE / 2)
        room_pickups.entities.append(ship)
        room_pickups.type = GameBase.RoomType.EXIT

        for i in range(1, 5):
            heart = Entities.HealthPickup(room_pickups, i)
            heart.pos = pygame.math.Vector2(64 + 48 * i, 96) # location of hearts on screen
            room_pickups.entities.append(heart)

        for i in range(1, 7):
            enemie = Characters.SnakeEnemy(room_enemies)
            enemie.pos = pygame.math.Vector2(64 + 48 * i, 112) # places the location of the enemie
            room_enemies.entities.append(enemie)

        for i in range(1, 4):
            enemie = Characters.HornetEnemy(room_enemies)
            enemie.pos = pygame.math.Vector2(80 + 120 * i, 112) # places the location of the enemie
            room_enemies.entities.append(enemie)

        for i in range(0, 10):
            g = pow(2, i)
            gold = Entities.GoldPickup(room_pickups, g)
            gold.pos = pygame.math.Vector2(Constants.ROOM_SIZE * Constants.TILE_SIZE - 96, 64 + 48 * i) # location of gold on screen
            room_pickups.entities.append(gold)

        item = Entities.ItemPickup(room_pickups, Items.BasicMeleeItem("sword", 2))
        item.pos = pygame.math.Vector2(100, 200)
        room_pickups.entities.append(item)
        item3 = Entities.ItemPickup(room_pickups, Items.BasicMeleeItem("cutlass", 3))
        item3.pos = pygame.math.Vector2(300, 200)
        room_pickups.entities.append(item3)
        item2 = Entities.ItemPickup(room_pickups, Items.BowItem())
        item2.pos = pygame.math.Vector2(200,200)
        room_pickups.entities.append(item2)

        test.rooms.append(room_enemies)

        test.rooms.append(room_pickups)
        test.start_room = room_pickups

        # boss room
        b = Characters.WizardEnemy(room_boss)
        b.teleport()
        room_boss.entities.append(b)
        test.rooms.append(room_boss)
        room_boss.type = GameBase.RoomType.BOSS

        # shop room
        # places stuff in room_shop
        room_shop.type = GameBase.RoomType.SHOP

        shopkeeper = Characters.Shopkeeper(room_shop)
        shopkeeper.pos = pygame.math.Vector2(100, 300)
        room_shop.entities.append(shopkeeper)

        pedestal = Entities.ShopPedestal(room_shop, Entities.ItemPickup(room_shop, Items.DummyItem()), 30)
        pedestal.pos = pygame.math.Vector2(108, 375)
        room_shop.entities.append(pedestal)

        test.rooms.append(room_shop)


        test.rooms.append(room_creation)


        for room in test.rooms:
            keys = list(room.neighbors.keys())
            factor = 64
            # if North exit
            if 1 in keys:
                thingy = Entities.HealthPickup(room, 1)
                # thingy.pos = pygame.math.Vector2(factor * 4, factor * 2)
                # room.entities.append(thingy)
            else:
                if (room.pos.y != 0):
                    for i in range(9):
                        wall = Entities.Terrain(room)
                        wall.pos = pygame.math.Vector2(factor * i, 0)
                        room.entities.append(wall)
            # if East exit
            if 2 in keys:
                thingy = Entities.HealthPickup(room, 2)
                # thingy.pos = pygame.math.Vector2(factor * 7, factor * 4)
                # room.entities.append(thingy)
            else:
                if (room.pos.x != 2):
                    for i in range(9):
                        wall = Entities.Terrain(room)
                        wall.pos = pygame.math.Vector2(factor * 8, factor * i)
                        room.entities.append(wall)
            # if South exit
            if 3 in keys:
                thingy = Entities.HealthPickup(room, 3)
                # thingy.pos = pygame.math.Vector2(factor * 4, factor * 7)
                # room.entities.append(thingy)
            else:
                if (room.pos.y != 2):
                    for i in range(9):
                        wall = Entities.Terrain(room)
                        wall.pos = pygame.math.Vector2(factor * i, factor * 8)
                        room.entities.append(wall)
            # if West exit
            if 4 in keys:
                thingy = Entities.HealthPickup(room, 4)
                # thingy.pos = pygame.math.Vector2(factor * i, factor * 4)
                # room.entities.append(thingy)
            else:
                if (room.pos.x != 0):
                    for i in range(9):
                        wall = Entities.Terrain(room)
                        wall.pos = pygame.math.Vector2(0, factor * i)
                        room.entities.append(wall)

        # for checking the number of rooms created:
        #
        #     print(len(test.rooms))


    def generate_sea(self):
        random.seed(self.name)
        island_count = random.randint(5, 8)
        island_names = []
        for i in range(0, island_count):
            island_names.append(gibberish.generate_word(random.randint(1, 3)))
        Debug.print("Islands of the " + self.name + " Sea: " + str(island_names))

        for i in range(0, island_count):
            x = random.randint(0, 6)
            y = random.randint(0, 6)
            pos = pygame.math.Vector2(x, y)
            name = island_names[i].capitalize()
            self.islands[str(pos)] = Island(pos, name)
            generation(self.islands[str(pos)])


class Scene(Main.Scene):
    def __init__(self, game, gen = True, test = False):
        super().__init__(game)
        self.test = test

        self.gen = gen
        if gen:
            self.game.sea = Sea("Test" if test else gibberish.generate_word(random.randint(1, 3)).capitalize())
        self.selected_tile = pygame.Vector2(3, 3)

        self.name_font = pygame.font.SysFont("Consolas", 30)
        self.island_placeholder = pygame.image.load("res/island-placeholder.png")

        self.sea_bg = pygame.Surface(pygame.math.Vector2(7 * 64, 7 * 64))
        for ix in range(0, 7):
            for iy in range(0, 7):
                tile = -1
                if ix == 0:
                    if iy == 0:
                        tile = 0
                    elif iy == 6:
                        tile = 6
                    else:
                        tile = 3
                elif ix == 6:
                    if iy == 0:
                        tile = 2
                    elif iy == 6:
                        tile = 8
                    else:
                        tile = 5
                else:
                    if iy == 0:
                        tile = 1
                    elif iy == 6:
                        tile = 7
                    else:
                        tile = 4

                spr = Drawing.Sprite(water_tex)
                spr.subrect = pygame.Rect(tile % 3 * 16, int(tile / 3) * 16, 16, 16)
                spr.scale = pygame.math.Vector2(4, 4)
                spr.pos = pygame.math.Vector2(ix * 64, iy * 64)
                spr.draw(self.sea_bg)

    def update_event(self, evt):
        if evt.type == pygame.KEYDOWN:
            # Selector movement
            if evt.key == pygame.K_w:
                self.selected_tile.y -= 1
            elif evt.key == pygame.K_s:
                self.selected_tile.y += 1
            elif evt.key == pygame.K_a:
                self.selected_tile.x -= 1
            elif evt.key == pygame.K_d:
                self.selected_tile.x += 1

            # Wrap around
            if self.selected_tile.x < 0:
                self.selected_tile.x += 7
            if self.selected_tile.x >= 7:
                self.selected_tile.x -= 7
            if self.selected_tile.y < 0:
                self.selected_tile.y += 7
            if self.selected_tile.y >= 7:
                self.selected_tile.y -= 7

            # Select island
            if evt.key == pygame.K_RETURN:
                if str(self.selected_tile) in self.game.sea.islands:
                    sel_island = self.game.sea.islands[str(self.selected_tile)]
                    self.game.island = sel_island
                    # if not self.test and self.gen:
                    #     generation(self.game.island)
                    self.game.room = sel_island.start_room
                    self.game.scene = Game.Scene(self.game)


    def update(self):
        pass

    def draw(self, screen):
        screen.fill(pygame.Color(0, 0, 0))

        # Draw the sea background
        sea_spr = Drawing.Sprite(self.sea_bg)
        sea_spr.pos = pygame.math.Vector2((Constants.WINDOW_SIZE[0] - self.sea_bg.get_width()) / 2,
                                          (Constants.WINDOW_SIZE[1] - self.sea_bg.get_height()) / 2)
        sea_spr.draw(screen)

        # Draw the islands
        for key in self.game.sea.islands.keys():
            island = self.game.sea.islands[key]
            island_spr = Drawing.Sprite(self.island_placeholder)
            island_spr.pos = pygame.math.Vector2(island.pos.x * 64, island.pos.y * 64) + sea_spr.pos
            island_spr.scale = pygame.math.Vector2(4, 4)
            island_spr.draw(screen)

        # Draw the scrolls and titles
        spr = Drawing.Sprite(scroll_tex)
        spr.pos = pygame.math.Vector2((Constants.WINDOW_SIZE[0] - scroll_tex.get_width() * 2) / 2, 0)
        spr.scale = pygame.math.Vector2(2, 2)
        spr.draw(screen)
        spr.pos.y = Constants.WINDOW_SIZE[1] - scroll_tex.get_height() * 2
        spr.draw(screen)

        text = Drawing.Text(self.name_font, self.game.sea.name + " Sea")
        text.color = pygame.Color(0, 0, 0)
        text.pos = pygame.math.Vector2((Constants.WINDOW_SIZE[0] - text.get_width()) / 2, 15)
        text.draw(screen)

        if str(self.selected_tile) in self.game.sea.islands:
            sel_island = self.game.sea.islands[str(self.selected_tile)]
            text.string = sel_island.name + " Island"
            text.pos = pygame.math.Vector2((Constants.WINDOW_SIZE[0] - text.get_width()) / 2,
                                           Constants.WINDOW_SIZE[1] - text.get_height() - 15)
            text.draw(screen)

        # Draw the selector
        spr = Drawing.Sprite(selector_tex)
        spr.pos = self.selected_tile * 64 + sea_spr.pos
        spr.draw(screen)

    def select_island(self, island):
        for isle in self.game.sea.islands:
            if self.game.sea.islands[isle] is island:
                self.selected_tile = pygame.math.Vector2(island.pos.x, island.pos.y)


# Makes island
def generation(island):
    width = random.randint(3, 7)
    length = random.randint(3, 7)
    # implementing Generation.py
    gen = Generation.Generation(width, length)
    gen.make()
    while not gen.isComplete():
        del gen
        print("Generation failed, remaking...")
        gen = Generation.Generation(width, length)
        gen.make()
    gen.printRooms()

    island.width = width
    island.length = length

    # Start creation
    x, y = 0, 0
    shop_exists = False
    # Loop for each room on Generated island
    for row in gen.rows:
        for room in row:
            if room.iter_num is 6 and not shop_exists:
                room_shop = GameBase.Room(island, pygame.math.Vector2(y, x))
                room_shop.neighbors = room.neighbors
                room_shop.gen_Object = room
                shop_exists = True
                # print ("shop at " + str(y) + ", " + str(x))
            elif room.iter_num is 1:
                room_pickups = GameBase.Room(island, pygame.math.Vector2(y, x))
                room_pickups.neighbors = room.neighbors
                room_pickups.gen_Object = room
                # print ("start at " + str(y) + ", " + str(x))
            else:
                empty_room = GameBase.Room(island, pygame.math.Vector2(y, x))
                empty_room.neighbors = room.neighbors
                empty_room.gen_Object = room
                # print ("empty at " + str(y) + ", " + str(x))
                island.rooms.append(empty_room)
            y += 1
        x += 1
        y = 0

    # boss room
    b = Characters.WizardEnemy(island.rooms[(len(island.rooms) - 1)])
    b.teleport()
    island.rooms[(len(island.rooms) - 1)].entities.append(b)
    island.rooms[(len(island.rooms) - 1)].type = GameBase.RoomType.BOSS

    # starting room
    island.start_room = island.rooms[0]
    ship = Entities.ExitShip(island.start_room)
    ship.pos = pygame.math.Vector2(64 * 5, 64 * 5)
    island.start_room.entities.append(ship)
    island.start_room.type = GameBase.RoomType.EXIT

    # pickups room
    # places stuff in room_pickups
    # for i in range(1, 5):
    #     heart = Entities.HealthPickup(room_pickups, i)
    #     heart.pos = pygame.math.Vector2(64 + 48 * i, 96) # location of hearts on screen
    #     room_pickups.entities.append(heart)

    # for i in range(0, 10):
    #     g = pow(2, i)
    #     gold = Entities.GoldPickup(room_pickups, g)
    #     gold.pos = pygame.math.Vector2(Constants.ROOM_SIZE * Constants.TILE_SIZE - 96, 64 + 48 * i) # location of gold on screen
    #     room_pickups.entities.append(gold)

    item = Entities.ItemPickup(room_pickups, Items.DummyItem())
    item.pos = pygame.math.Vector2(100, 200)
    room_pickups.entities.append(item)

    island.rooms.append(room_pickups)

    # shop room
    # places stuff in room_shop
    room_shop.type = GameBase.RoomType.SHOP

    shopkeeper = Characters.Shopkeeper(room_shop)
    shopkeeper.pos = pygame.math.Vector2(Constants.ROOM_SIZE * Constants.TILE_SIZE / 2 - 16, Constants.ROOM_SIZE * Constants.TILE_SIZE / 2 - 96)
    room_shop.entities.append(shopkeeper)

    pedestal_count = random.randint(1, 4)
    for i in range(pedestal_count):
        x = Constants.ROOM_SIZE * Constants.TILE_SIZE / (pedestal_count + 1) * (i + 1)
        y = shopkeeper.pos.y + 160
        make_store_pedestal(room_shop, pygame.math.Vector2(x, y))


    island.rooms.append(room_shop)


    # island.rooms.append(room_creation)

    # Wall placement
    for room in island.rooms:
        keys = list(room.neighbors.keys())
        factor = 64 # rooms are (9 * 64) x (9 * 64) pixels

        # if no North exit
        if 1 not in keys:
            # if not Northernmost row
            if (room.pos.y != 0):
                # if Westernmost column
                if (room.pos.x == 0):
                    for i in range(1, 9):
                        addWall(room, factor * i, 0)
                # if Easternmost column
                elif (room.pos.x == (width - 1)):
                    for i in range(8):
                        addWall(room, factor * i, 0)
                # make as usual
                else:
                    for i in range(9):
                        addWall(room, factor * i, 0)
            else:
                for i in range(9):
                    addBound(room, factor * i, 0)
        else:
            # if not Northernmost row
            if (room.pos.y != 0):
                # if not Westernmost column
                if (room.pos.x != 0):
                    addWall(room, 0, 0)
                # if not Easternmost column
                if (room.pos.x != (length - 1)):
                    addWall(room, factor * 8, 0)

        # if no East exit
        if 2 not in keys:
            # if not Easternmost column
            if (room.pos.x != (length - 1)):
                # if Northernmost row
                if (room.pos.y == 0):
                    for i in range(1,9):
                        addWall(room, factor * 8, factor * i)
                # if Southernmost row
                elif (room.pos.y == (width - 1)):
                    for i in range(8):
                        addWall(room, factor * 8, factor * i)
                # make as usual
                else:
                    for i in range(9):
                        addWall(room, factor * 8, factor * i)
            else:
                for i in range(9):
                    addBound(room, factor * 8, factor * i)
        else:
            # if not Easternmost column
            if (room.pos.x != (length - 1)):
                # if not Northernmost row
                if (room.pos.y != 0):
                    addWall(room, factor * 8, 0)
                # if not Southernmost row
                if (room.pos.y != (width - 1)):
                    addWall(room, factor * 8, factor * 8)

        # if no South exit
        if 3 not in keys:
            # if not Southernmost row
            if (room.pos.y != (width - 1)):
                # if Easternmost column
                if (room.pos.x == 0):
                    for i in range (1,9):
                        addWall(room, factor * i, factor * 8)
                # if Westernmost column
                elif (room.pos.x == (length - 1)):
                    for i in range (8):
                        addWall(room, factor * i, factor * 8)
                # draw wall as usual
                else:
                    for i in range(9):
                        addWall(room, factor * i, factor * 8)
            else:
                for i in range(9):
                    addBound(room, factor * i, factor * 8)
        else:
            # if not Southernmost row
            if (room.pos.y != (width - 1)):
                # if not Easternmost column
                if (room.pos.x != 0):
                    addWall(room, 0, factor * 8)
                # if not Westernmost column
                if (room.pos.x != (length - 1)):
                    addWall(room, factor * 8, factor * 8)

        # if West exit
        if 4 not in keys:
            # if not Westernmost room
            if (room.pos.x != 0):
                # if Northernmost room
                if (room.pos.y == 0):
                    for i in range(1,9):
                        addWall(room, 0, factor * i)
                # if Southernmost room 
                elif (room.pos.y == (width - 1)):
                    for i in range(8):
                        addWall(room, 0, factor * i)
                # draw wall as usual
                else:
                    for i in range(9):
                        addWall(room, 0, factor * i)
            else:
                for i in range(9):
                    addBound(room, 0, factor * i)
        else:
            # if not Westernmost column
            if (room.pos.x != 0):
                # if not Northernmost row
                if (room.pos.y != 0):
                    addWall(room, 0, 0)
                # if not Southernmost row
                if (room.pos.y != (width - 1)):
                    addWall(room, 0, factor * 8)

def addWall(room, x, y):
    wall = Entities.Terrain(room)
    wall.pos = pygame.math.Vector2(x, y)
    room.entities.append(wall)

def addBound(room, x, y):
    wall = Entities.Terrain(room, False)
    wall.pos = pygame.math.Vector2(x, y)
    room.entities.append(wall)
