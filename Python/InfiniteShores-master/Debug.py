import pygame
import Constants
import Drawing
from code import InteractiveConsole

debug_surface = None
debug_font_big = None
debug_font_small = None
debug_output = None
debug_input = None
debug_console = None


def init():
    global debug_surface, debug_font_big, debug_font_small
    global debug_output, debug_input, debug_console

    debug_surface = pygame.Surface(Constants.WINDOW_SIZE, pygame.SRCALPHA)
    debug_font_big = pygame.font.SysFont("Consolas", 30)
    debug_font_small = pygame.font.SysFont("Consolas", 12)
    debug_output = []
    debug_input = None


def draw_collision_rect(rect):
    pygame.draw.rect(debug_surface, (255, 0, 0), rect, 1)

def draw_player_interact_rect(rect):
    pygame.draw.rect(debug_surface, (255, 255, 0), rect, 1)


def draw_fps(fps):
    text = Drawing.Text(debug_font_big, str(int(fps)))
    text.pos = pygame.math.Vector2(10, 10)
    text.draw(debug_surface)


def draw_console():
    y = Constants.WINDOW_SIZE[1] - 20
    text = Drawing.Text(debug_font_small, "")

    if debug_input is not None:
        text.string = "> " + debug_input
        text.pos = pygame.math.Vector2(10, y)
        text.draw(debug_surface)
    y -= 15

    for line in debug_output[::-1]:
        text.string = line
        text.pos = pygame.math.Vector2(10, y)
        text.draw(debug_surface)
        y -= 15


# To prevent them from accidentally using the python builtin help(), and the freezing the program and using the console
def help():
    print("Type some python code! (Or ` to back out.)")


console_print = print


def print(str_):
    str_ = str(str_)
    while len(debug_output) >= 5:
        del debug_output[0]
    for line in str_.split('\n'):
        debug_output.append(line)
        console_print(line)


def do_debug_input(evt):
    if not Constants.DEBUG:
        return

    global debug_console
    if debug_console is None:
        debug_console = InteractiveConsole(globals())
        debug_console.write = print
        # Nasty hack to access Main.game
        debug_console.push("import __main__")
        debug_console.push("game = __main__.game")

    global debug_input

    if evt.key == pygame.K_BACKQUOTE:
        if debug_input is None:
            debug_input = ""
        else:
            debug_input = None
        return

    if debug_input is None:
        return

    if evt.key == pygame.K_BACKSPACE:
        if len(debug_input) > 0:
            debug_input = debug_input[:-1]
    elif evt.key == pygame.K_RETURN:
        print("> " + debug_input)
        debug_console.runsource(debug_input)
        debug_input = ""
    elif evt.unicode is not None:
        debug_input = debug_input + evt.unicode
