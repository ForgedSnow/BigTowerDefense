import pygame
import pygame.gfxdraw
from map import board, map_selection
from tower import tower

starting_resolution = "480p"
resolution_dict = {
    "1080p": (1920, 1080),
    "720p": (1280, 720),
    "480p": (640, 480)
}


class title_screen:
    def __init__(self):
        #init
        self.menu_buttons = []

        self.resolution = resolution_dict.get(starting_resolution)
        pygame.init()
        pygame.display.set_caption("Video Game")

        self.window = pygame.display.set_mode(self.resolution)
        self.graphics = self.default_graphics()

        self.state = "main"
        running = True
        clock = pygame.time.Clock()

        #draw board
        self.maps = map_selection()
        self.board = board(self.maps.map_list[3])

        #virtual canvas buffer
        buffer = pygame.Surface(self.resolution, pygame.SRCALPHA)

        #test blob
        class blob:
            def __init__(self, parent):
                self.distance = 0.5
                self.parent = parent
                self.speed = 0.1
                self.color = (125, 125, 125)
                self.size = 10
                self.center = (-1, -1)
                self.radius = 4

            def update(self):
                self.distance += self.speed
                if self.distance > self.parent.board.path.length:
                    #self.distance = 0.5
                    pass
                self.center = self.parent.board.path.get_position(self.distance)
                self.center = self.center[0] * self.parent.board.scale + self.parent.board.scale / 2 - self.radius,\
                              self.center[1] * self.parent.board.scale + self.parent.board.scale / 2 - self.radius

            def draw(self):
                graphics = pygame.Surface(self.parent.resolution, pygame.SRCALPHA)
                rectangle = pygame.Rect(self.center, (self.radius * 2, self.radius * 2))
                pygame.draw.rect(graphics, self.color, rect=rectangle)
                return graphics

        enemies = []
        start = 0.5
        for each in range(0, 16):
            enemy = blob(self)
            enemy.distance += start
            enemies.append(enemy)
            start -= 1.5

        towers = []
        tower_locations = [(8, 9), (12, 9)]

        for point in tower_locations:
            additional = tower(self.board.scale)
            additional.location = point
            towers.append(additional)

        """
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
        """

        while running:
            buffer.fill((0, 0, 0))
            time_delta = clock.tick(60) / 1000.0
            #time_delta = clock.tick(30) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                if event.type == pygame.USEREVENT:
                    if self.state == "main":
                        pass

            buffer.blit(self.graphics, (0, 0))
            buffer.blit(self.board.draw(), (0, 0))

            for enemy in enemies:
                enemy.update()
                buffer.blit(enemy.draw(), (0, 0))

            range_color = (0, 0, 0, 50)
            circle = pygame.Surface(self.resolution, pygame.SRCALPHA)

            for tower_member in towers:
                pygame.draw.circle(circle, range_color, tower_member.get_center(),
                                   tower_member.range * self.board.scale)

            buffer.blit(circle, (0, 0))

            for tower_member in towers:
                buffer.blit(tower_member.draw(), tower_member.top_left())

            self.board.draw_ends(buffer)

            self.window.blit(buffer, (0, 0))
            pygame.display.update()

        pygame.quit()

    def default_graphics(self):
        background_color = (61, 120, 180)
        background = pygame.Surface(self.resolution)
        background.fill(background_color)

        return background


if __name__ == "__main__":
    title_screen()
