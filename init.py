import numpy as np
import pygame as py
from Pendulum import DoublePendulum
import copy
import colorsys
from Text import Text


def main():
    py.init()
    # ========================= VARIABLES =========================
    screen_info = py.display.Info()
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    text_size: int = 15
    text_offSet: int = 10

    COLORS: dict[str, tuple] = {
        'WHITE': (255, 255, 255),
        'BLUE': (27, 78, 207),
        'RED': (232, 57, 51),
        'GREEN': (72, 232, 51),
        'PURPLE': (202, 67, 230),
        'YELLOW': (255, 219, 41)
    }
    REFERENCE_FPS = 1200

    TAIL = False
    RESET_SCREEN = True
    ONLY_HEAD = False
    # ========================= BASIC =========================
    screen_info  = py.display.Info()
    #screenSize = (1250, 750)
    screenSize = (screen_info.current_w, screen_info.current_h)
    SCREEN = py.display.set_mode(screenSize)
    py.display.set_caption('Py Double pendulum simulation')
    CLOCK = py.time.Clock()
    # ========================= TEXT =========================
    text_font = py.font.SysFont("Arial", text_size)
    def draw_text(textToRender: Text) -> None:
        img = text_font.render(str(textToRender), True, textToRender.text_col)
        SCREEN.blit(img, textToRender.pos)

    HeadText = Text("Only head (1)", False, 10, HEIGHT - text_size * 3 - text_offSet)
    ResetText = Text("Reset Screen (2)", True, 10, HEIGHT - text_size * 2 - text_offSet)
    TrailsText = Text("Trails (3)", False, 10, HEIGHT - text_size * 1 - text_offSet)

    ResetKeyText = Text("Rest simulation (r)", None, text_size  - text_offSet, text_size * 2 - text_offSet)

    TEXTS = [TrailsText, ResetText, HeadText, ResetKeyText]
    # ========================= COMPONENTS =========================
    PENDULUMS: list = []

    def reset_pendulums():
        for i in range(1,255):
            hue = i / 255.0
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            color = tuple(int(c * 255) for c in rgb)

            PendulumColor = {
                'LINE': COLORS['WHITE'],
                'BALL1': color,
                'BALL2': color,
                'CENTER': COLORS['WHITE'],
                'TRAIL': color
            }

            PENDULUMS.append(DoublePendulum(d1=175, d2=175,
                                            m1=10, m2=50,
                                            a1=180, a2=180 - i * 0.00001,
                                            colors=copy.deepcopy(PendulumColor),
                                            screenSize=screenSize))
    """END FUNCTION"""

    reset_pendulums()
    # ========================= BASIC =========================
    RUNNING_GAME: bool = True
    while RUNNING_GAME:
        deltaTime = CLOCK.tick(REFERENCE_FPS) / 1000.0
        if deltaTime == 0: continue

        if RESET_SCREEN: SCREEN.fill((0, 0, 0))

        # ========================= EVENTS =========================
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                RUNNING_GAME = False
            elif event.type == py.KEYUP:
                if event.key == py.K_ESCAPE:
                    RUNNING_GAME = False
                    break
                if event.key == py.K_r:
                    SCREEN.fill((0, 0, 0))
                    PENDULUMS = []
                    reset_pendulums()
                    break
                if event.key == py.K_3:
                    TAIL = not TAIL
                    break
                if event.key == py.K_2:
                    RESET_SCREEN = not RESET_SCREEN
                    break
                if event.key == py.K_1:
                    ONLY_HEAD = not ONLY_HEAD
                    break

        # ========================= COMPONENTS =========================
        for Pendulum in PENDULUMS:
            if not TAIL: break
            Pendulum.draw_trail(SCREEN)
        for Pendulum in PENDULUMS:
            Pendulum.draw_pendulum(SCREEN, deltaTime, TAIL, ONLY_HEAD)
        for text in TEXTS:
            draw_text(text)

        TrailsText.set_value(TAIL)
        ResetText.set_value(RESET_SCREEN)
        HeadText.set_value(ONLY_HEAD)

        py.display.update()
    '''END WHILE'''
    py.quit()


if __name__ == "__main__":
    main()
