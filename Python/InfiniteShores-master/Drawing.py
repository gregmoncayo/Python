import pygame


class Sprite:
    def __init__(self, tex): # tex = image file
        self.tex = tex
        self.subrect = None
        self.rotation = 0
        self.scale = pygame.math.Vector2(1, 1)
        self.origin = pygame.math.Vector2(0, 0)

        self.pos = pygame.math.Vector2(0, 0)

        self.recalc = True
        self.__sprtex = None
        self.__renderoffset = pygame.math.Vector2(0, 0)

    @property
    def tex(self):
        return self.__tex

    @tex.setter
    def tex(self, tex):
        self.recalc = True
        self.__tex = tex

    @property
    def subrect(self):
        return self.__subrect

    @subrect.setter
    def subrect(self, subrect):
        self.recalc = True
        self.__subrect = subrect

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, rotation):
        self.recalc = True
        self.__rotation = rotation

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, scale):
        self.recalc = True
        self.__scale = scale

    @property
    def origin(self):
        return self.__origin

    @origin.setter
    def origin(self, origin):
        self.recalc = True
        self.__origin= origin

    def draw(self, screen):
        if self.recalc:
            self.recalculate()
        screen.blit(self.__sprtex, self.pos - self.__renderoffset)

    def recalculate(self):
        self.recalc = False
        if self.subrect is None:
            self.__sprtex = self.tex
        else:
            self.__sprtex = pygame.Surface(self.subrect.size, pygame.SRCALPHA)
            self.__sprtex.blit(self.tex, pygame.math.Vector2(-self.subrect[0], -self.subrect[1]))
        self.__renderoffset = pygame.math.Vector2(self.origin.x, self.origin.y)
        if self.scale.x != 1 or self.scale.y != 1:
            self.__sprtex = pygame.transform.scale(self.__sprtex, (int(self.__sprtex.get_width() * self.scale.x),
                                                                   int(self.__sprtex.get_height() * self.scale.y)))
            self.__renderoffset = pygame.math.Vector2(self.origin.x * self.scale.x, self.origin.y * self.scale.y)
        if self.rotation != 0:
            vec = self.__renderoffset - pygame.math.Vector2(self.__sprtex.get_width() / 2, self.__sprtex.get_height() / 2)
            vec = vec.rotate(-self.rotation)
            self.__sprtex = pygame.transform.rotate(self.__sprtex, self.rotation)
            self.__renderoffset = vec + pygame.math.Vector2(self.__sprtex.get_width() / 2, self.__sprtex.get_height() / 2)


class Text:
    def __init__(self, font, string):
        self.font = font
        self.string = string
        self.color = pygame.Color(0, 0, 0)
        self.pos = pygame.math.Vector2(0, 0)

        self.recalc = True
        self.__text = None

    @property
    def font(self):
        return self.__font

    @font.setter
    def font(self, font):
        self.recalc = True
        self.__font = font

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.recalc = True
        self.__color = color

    @property
    def string(self):
        return self.__string

    @string.setter
    def string(self, string):
        self.recalc = True
        self.__string = string

    def draw(self, screen):
        if self.recalc:
            self.recalculate()
        screen.blit(self.__text, self.pos)

    def get_width(self):
        if self.recalc:
            self.recalculate()
        return self.__text.get_width()

    def get_height(self):
        if self.recalc:
            self.recalculate()
        return self.__text.get_height()

    def recalculate(self):
        self.recalc = False
        self.__text = self.__font.render(self.__string, True, self.__color)
