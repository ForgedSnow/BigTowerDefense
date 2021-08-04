import pygame
from pygame.math import Vector2


def draw_line(point, angle, length, color, surface, width=1):
    vector = Vector2()
    vector.from_polar((length, angle))
    pygame.draw.line(surface, color, point, point + vector, width)
