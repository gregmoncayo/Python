import pygame
import Main
import Ui
import Drawing
import Game
import Constants
import WorldMap


class Scene(Main.Scene):
    def __init__(self, game):
        super().__init__(game)

        self.title = Drawing.Text(pygame.font.SysFont("Consolas", 50), "Infinite Shores")
        self.title.pos = ((Constants.WINDOW_SIZE[0] - self.title.get_width()) / 2, 50)

        self.playButton = Ui.Button("Play", (Constants.WINDOW_SIZE[0] - 200) / 2, 250, 200, 50)
        self.playButton.callback = self.callback_button_play
        self.widgets.append(self.playButton)

        self.worldButton = Ui.Button("Test World", self.playButton.rect.x,
                                     self.playButton.rect.y + self.playButton.rect.height + 32,
                                     self.playButton.rect.width, self.playButton.rect.height)
        self.worldButton.callback = self.callback_button_world
        self.widgets.append(self.worldButton)

    def callback_button_play(self):
        self.game.scene = WorldMap.Scene(self.game, True)

    def callback_button_world(self):
        self.game.scene = WorldMap.Scene(self.game, True, True)

    def update(self):
        super().update()

    def draw(self, screen):
        self.title.draw(screen)

        super().draw(screen)
