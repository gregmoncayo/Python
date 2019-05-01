# Runs the game, the main "exe" for the project

import pygame
import MainMenu
import Constants
import Debug
import Characters


class Scene:
    def __init__(self, game):
        self.game = game
        self.widgets = []

    def update_event(self, evt):
        for widget in self.widgets:
            widget.update_event(evt)

    def update(self):
        for widget in self.widgets:
            widget.update()

    def draw(self, screen):
        for widget in self.widgets:
            widget.draw(screen)


class Game:
    def __init__(self):
        pygame.init()
        Debug.init()

        pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
        pygame.mixer.init(22050, -16, 2, 4096)
        pygame.mixer.music.load("res/ThemeSong.wav")
        pygame.mixer.music.play(-1)

        # TODO: Icon
        pygame.display.set_caption("Infinite Shores")

        self.screen = pygame.display.set_mode(Constants.WINDOW_SIZE)

        self.scene = MainMenu.Scene(self)

        self.running = True

        self.sea = None
        self.island = None
        self.room = None
        self.player = Characters.Player(self, self.room)
        self.player.pos = pygame.math.Vector2(Constants.ROOM_SIZE * Constants.TILE_SIZE / 2,
                                              Constants.ROOM_SIZE * Constants.TILE_SIZE / 2)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    Debug.do_debug_input(event)
                self.scene.update_event(event)

            Debug.debug_surface.fill((255, 255, 255, 0))
            self.scene.update()

            self.screen.fill((255, 255, 255))

            self.scene.draw(self.screen)

            if Constants.DEBUG:
                Debug.draw_fps(clock.get_fps())
                Debug.draw_console()
                self.screen.blit(Debug.debug_surface, (0, 0))

            pygame.display.update()
            clock.tick(Constants.FRAMERATE)

        pygame.quit()


if __name__ == "__main__":
    global game
    game = Game()
    game.run()
