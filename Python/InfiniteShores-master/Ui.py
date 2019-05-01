import pygame
import Drawing


class Widget:
    def __init__(self):
        pass

    def update_event(self, evt):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class Button(Widget):
    def __init__(self, text, x, y, w, h):
        super().__init__()

        self.rect = pygame.Rect(x, y, w, h)

        self.text = Drawing.Text(pygame.font.SysFont("Consolas", int(h * 0.8)), text)
        draw_x = self.rect.left + (self.rect.width - self.text.get_width()) / 2
        draw_y = self.rect.top + int(self.rect.height * 0.1)
        self.text.pos = pygame.math.Vector2(draw_x, draw_y)

        self.hovered = False

        self.fillColor = pygame.Color(255, 255, 255)
        self.outlineColor = pygame.Color(0, 0, 0)
        self.outlineThickness = 2
        self.hoverColor = pygame.Color(128, 128, 128)

    def update_event(self, evt):
        if evt.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(evt.pos)
        elif evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
            if self.rect.collidepoint(evt.pos):
                if hasattr(self, "callback"):
                    self.callback()

    def draw(self, screen):
        pygame.draw.rect(screen, self.hoverColor if self.hovered else self.fillColor, self.rect, 0)
        pygame.draw.rect(screen, self.outlineColor, self.rect, self.outlineThickness)

        self.text.draw(screen)
