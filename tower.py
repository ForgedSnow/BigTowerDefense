import pygame
import draw_helper as gg


class tower:
    def __init__(self, scale):
        self.scale = scale
        self.level = 1
        self.speed = 1
        self.power = 1
        self.price = 1
        self.amp = 1
        self.range = 5
        self.direction = 0
        self.location = (-1, -1)
        self.radius = scale // 2

    def get_damage(self):
        return self.price / 100 * self.power * self.amp

    def get_center(self):
        return self.scale * (self.location[0] + 0.5), self.scale * (self.location[1] + 0.5)

    def top_left(self):
        return self.scale * self.location[0], self.scale * self.location[1]

    def draw(self):
        # create canvas to paint the board onto
        # background_color = (61, 120, 180)
        background = pygame.Surface((self.scale, self.scale), pygame.SRCALPHA)
        # background.fill(background_color)

        color = (255, 255, 255)

        #center = (self.location[0] + 0.5) * self.scale, (self.location[1] + 0.5) * self.scale
        center = (0.5 * self.scale, 0.5 * self.scale)

        pygame.draw.circle(background, color, center, self.radius)
        gg.draw_line(center, self.direction, self.radius, (15, 15, 15), background, 2)

        return background

    damage = property(get_damage)
