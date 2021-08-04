import pygame


class board:
    def __init__(self, selected_path):
        self.scale = 20
        self.size = (32, 24)
        self.resolution = (self.size[0] * self.scale, self.size[1] * self.scale)
        self.path = selected_path
        self.ends = pygame.Surface(self.resolution, pygame.SRCALPHA)

    def draw_ends(self, surface):
        end_color = (0, 0, 0)

        def draw_tile(x, y):
            pygame.draw.rect(surface, end_color, pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale))

        draw_tile(self.path.end.x, self.path.end.y)
        draw_tile(self.path.beginning.x, self.path.beginning.y)

    def draw(self):
        #create canvas to paint the board onto
        background_color = (61, 120, 180)
        background = pygame.Surface(self.resolution)
        background.fill(background_color)

        path_color = (255, 255, 255)

        def draw_tile(x, y):
            #print("DRAW", x, y)
            #background.fill(path_color, rect=pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale))
            pygame.draw.rect(background, path_color, pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale))

        def connect_points(one, two):
            draw_tile(one.x, one.y)
            if one.x == two.x:
                #vertical path
                if one.y > two.y:
                    for index in range(1, one.y - two.y):
                        draw_tile(one.x, two.y + index)
                else:
                    for index in range(1, two.y - one.y):
                        draw_tile(one.x, one.y + index)

            else:
                #horizontal path
                if one.x > two.x:
                    for index in range(1, one.x - two.x):
                        draw_tile(two.x + index, one.y)
                else:
                    for index in range(1, two.x - one.x):
                        draw_tile(one.x + index, one.y)

        selected = self.path.beginning
        for point in self.path.path:
            if point == self.path.beginning:
                continue
            """
            if point == self.path.end:
                draw_tile(point.x, point.y)
                continue
            """
            connect_points(selected, point)
            selected = point

        draw_tile(self.path.end.x, self.path.end.y)

        return background


class path:
    class path_node:
        def __init__(self, xy):
            self.location = xy
            self.x = xy[0]
            self.y = xy[1]
            self.position = 0

    def __init__(self):
        self.width = 1
        self.height = 1
        self.length = -1
        self.sections = []
        self.beginning = path.path_node((0, 0))
        self.end = path.path_node((1, 1))
        self.path = []

    def add_section(self, point):
        if self.length < 0:
            self.beginning = path.path_node(point)

        self.path.append(path.path_node(point))
        self.length += 1

    def get_position(self, distance_along_path):
        selected = -1
        distance_along_path += 1
        for index in range(0, len(self.sections) - 1):
            if self.sections[index] <= distance_along_path < self.sections[index + 1]:
                selected = index
                break

        if selected == -1:
            print("section not found error")
            return -1, -1

        distance_from_point = distance_along_path - self.sections[selected]
        one = self.path[selected]
        two = self.path[selected + 1]
        if one.x == two.x:
            #vertical
            if one.y > two.y:
                #down
                return one.x, one.y - distance_from_point
            if one.y < two.y:
                #up
                return one.x, one.y + distance_from_point
        if one.y == two.y:
            #horiztonal
            if one.x > two.x:
                #left
                return one.x - distance_from_point, one.y
            if one.x < two.x:
                #right
                return one.x + distance_from_point, one.y

        print("first segment not implemented")
        return 0, 0

    def calculate_sections(self):
        length = 0.5
        selected = self.beginning
        point_positions = []

        def distance(one, two):
            if one.x == two.x and one.y == two.y:
                return 0
            if one.x == two.x:
                return abs(one.y - two.y)
            else:
                return abs(one.x - two.x)

        for point in self.path:
            if point == self.beginning:
                continue
            else:
                length += distance(selected, point)
                selected = point
                point_positions.append(length)

        return point_positions

    def calculate_length(self):
        length = 1
        selected = self.beginning

        def distance(one, two):
            if one.x == two.x:
                return abs(one.y - two.y)
            else:
                return abs(one.x - two.x)

        for point in self.path:
            if point == self.beginning:
                continue
            length += distance(selected, point)
            selected = point

        return length

    def complete_path(self):
        if self.length > 0:
            self.end = self.path[-1]
        self.length = self.calculate_length()
        self.sections = self.calculate_sections()
        print(self.sections)


class map_selection:
    def __init__(self):
        self.path = []
        self.map_list = self.construct_map_list()

    @staticmethod
    def construct_map_list():
        map_0 = path()
        map_0_path = [(0, 2), (13, 2), (13, 13), (0, 13)]
        for each in map_0_path:
            map_0.add_section(each)
        map_0.complete_path()

        map_1 = path()
        map_1_path = [(3, 0), (3, 13), (6, 13), (6, 2), (9, 2), (9, 13), (12, 13), (12, 2), (15, 2)]
        for each in map_1_path:
            map_1.add_section(each)
        map_1.complete_path()

        map_2 = path()
        map_2_path = [(0, 0), (15, 0)]
        for each in map_2_path:
            map_2.add_section(each)
        map_2.complete_path()

        map_3 = path()
        map_3_path = [(2, -1), (2, 3), (29, 3), (29, 22), (2, 22), (2, 6), (26, 6), (26, 19), (5, 19), (5, -1)]
        for each in map_3_path:
            map_3.add_section(each)
        map_3.complete_path()

        return map_0, map_1, map_2, map_3
