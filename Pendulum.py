import numpy as np
import pygame as py
from collections import deque

G: float = 5


class DoublePendulum:
    def __init__(self, d1: float, d2: float, m1: float, m2: float,
                 a1: float, a2: float, screenSize: tuple,
                 colors: dict[str, tuple]):

        self.center = np.array([screenSize[0] / 2, screenSize[1] / 2])

        self.d1 = d1
        self.d2 = d2
        self.m1 = m1
        self.m2 = m2

        '''self.a1 = np.radians(np.random.uniform(0, 360))
        self.a2 = np.radians(np.random.uniform(0, 360))'''
        self.a1 = np.radians(a1)
        self.a2 = np.radians(a2)

        self.vel1 = 0
        self.vel2 = 0

        self.acc1 = 0
        self.acc2 = 0

        self.screenSize = screenSize
        self.radius1 = self.m1 / 5
        self.radius2 = self.m2 / 5
        self.colors = colors

        self.trail = deque()

    def draw_trail(self, SCREEN):
        if len(self.trail) < 2: return
        py.draw.lines(SCREEN,
                      self.colors['TRAIL'],
                      False,
                      list(self.trail),
                      1
                      )


    def draw_pendulum(self, SCREEN, deltaTime: float, TAIL: bool, ONLY_HEAD: bool):
        self.update_angles(deltaTime)

        pos1: np.array = self.center + np.array([self.d1 * np.sin(self.a1),
                                                 self.d1 * np.cos(self.a1)])
        pos2: np.array = pos1 + np.array([self.d2 * np.sin(self.a2),
                                          self.d2 * np.cos(self.a2)])

        if TAIL:
            self.trail.append(pos2)
            if len(self.trail) > 100:
                self.trail.popleft()
        else:
            self.trail = deque()

        if not ONLY_HEAD:
            py.draw.line(SCREEN,
                         self.colors['LINE'],
                         self.center,
                         pos1,
                         2
                         )
            py.draw.line(SCREEN,
                         self.colors['LINE'],
                         pos1,
                         pos2,
                         2
                         )
            py.draw.circle(SCREEN,
                           self.colors['CENTER'],
                           self.center,
                           5
                           )
            py.draw.circle(SCREEN,
                           self.colors['BALL1'],
                           pos1,
                           self.radius1**0.5 * 2 + 5
                           )

        py.draw.circle(SCREEN,
                       self.colors['BALL2'],
                       pos2,
                       self.radius2 ** 0.5 * 2 + 5
                       )


    def update_angles_pre(self, deltaTime: float):
        num1 = -G * (2 * self.m1 + self.m2) * np.sin(self.a1)
        num2 = -self.m2 * G * np.sin(self.a1 - 2 * self.a2)
        num3 = -2 * np.sin(self.a1 - self.a2) * self.m2
        num4 = (self.vel2 ** 2) * self.d2 + (self.vel1 ** 2) * self.d1 * np.cos(self.a1 - self.a2)

        den = self.d1 * (2 * self.m1 + self.m2 - self.m2 * np.cos(2 * self.a1 - 2 * self.a2))

        self.acc1 = (num1 + num2 + num3 * num4) / den

        num1 = 2 * np.sin(self.a1 - self.a2)
        num2 = self.vel1 ** 2 * self.d1 * (self.m1 + self.m2)
        num3 = G * (self.m1 + self.m2) * np.cos(self.a1)
        num4 = self.vel2 ** 2 * self.d2 * self.m2 * np.cos(self.a1 - self.a2)

        den = self.d2 * (2 * self.m1 + self.m2 - self.m2 * np.cos(2 * self.a1 - 2 * self.a2))

        self.acc2 = (num1 * (num2 + num3 + num4)) / den

        self.vel1 += self.acc1 * deltaTime
        self.vel2 += self.acc2 * deltaTime

        self.a1 += self.vel1
        self.a2 += self.vel2

        # Air friction
        self.vel1 *= 0.9996
        self.vel2 *= 0.9996

    def update_angles(self, deltaTime: float):
        # Fórmula 1: aceleración angular de theta1
        num1 = -G * (2 * self.m1 + self.m2) * np.sin(self.a1)
        num2 = -self.m2 * G * np.sin(self.a1 - 2 * self.a2)
        num3 = -2 * np.sin(self.a1 - self.a2) * self.m2 * (
                self.vel2 ** 2 * self.d2 + self.vel1 ** 2 * self.d1 * np.cos(self.a1 - self.a2))
        den = self.d1 * (2 * self.m1 + self.m2 - self.m2 * np.cos(2 * self.a1 - 2 * self.a2))
        self.acc1 = (num1 + num2 + num3) / den

        # Fórmula 2: aceleración angular de theta2
        num1 = 2 * np.sin(self.a1 - self.a2) * (
                self.vel1 ** 2 * self.d1 * (self.m1 + self.m2) + G * (self.m1 + self.m2) * np.cos(
            self.a1) + self.vel2 ** 2 * self.d2 * self.m2 * np.cos(self.a1 - self.a2))
        den = self.d2 * (2 * self.m1 + self.m2 - self.m2 * np.cos(2 * self.a1 - 2 * self.a2))
        self.acc2 = num1 / den

        # Actualizar velocidades angulares
        self.vel1 += self.acc1 * deltaTime
        self.vel2 += self.acc2 * deltaTime

        # Actualizar ángulos
        self.a1 += self.vel1
        self.a2 += self.vel2

        # Considerar fricción del aire
        self.vel1 *= 0.99975
        self.vel2 *= 0.99975
