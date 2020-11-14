from json import load
from pygame import draw, display

with open(r'config\config.json', mode='r') as config_file:
    config = load(config_file)


class Node:
    def __init__(self, row, col, width, total_rows, is_start_node, is_end_node):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = config["colors"]["WHITE"]
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.is_start_node = is_start_node
        self.is_end_node = is_end_node
        self.distance = float("inf")
        self.visited = False
        self.prev_node = None

    def set_distance(self, distance):
        self.distance = distance

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == config["colors"]["RED"]

    def is_open(self):
        return self.color == config["colors"]["GREEN"]

    def is_wall(self):
        return self.color == config["colors"]["BLACK"]

    def is_start(self):
        return self.color == config["colors"]["ORANGE"]

    def is_end(self):
        return self.color == config["colors"]["PURPLE"]

    def reset(self):
        self.color = config["colors"]["WHITE"]

    def make_start(self):
        self.is_start_node = True
        self.color = config["colors"]["ORANGE"]

    def make_closed(self):
        self.color = config["colors"]["RED"]

    def make_open(self):
        self.color = config["colors"]["GREEN"]

    def make_wall(self):
        self.color = config["colors"]["BLACK"]

    def make_end(self):
        self.is_end_node = True
        self.color = config["colors"]["PURPLE"]

    def make_path(self):
        self.color = config["colors"]["TURQUOISE"]

    def draw(self, win):
        draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])
        return self.neighbors

    def __lt__(self, other):
        return False


class Grid:
    def __init__(self, rows, width):
        self.rows = rows
        self.width = width
        self.grid = []
        self.gap = self.width // self.rows

    def make_grid(self):
        self.grid = []
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.rows):
                node = Node(i, j, self.gap, self.rows, False, False)
                self.grid[i].append(node)
        return self.grid

    def draw_grid(self, win):
        for i in range(self.rows):
            draw.line(win, config["colors"]["GREY"], (0, i * self.gap), (self.width, i * self.gap))
            for j in range(self.rows):
                draw.line(win, config["colors"]["GREY"], (j * self.gap, 0), (j * self.gap, self.width))

    def draw(self, win):
        win.fill(config["colors"]["WHITE"])
        for row in self.grid:
            for spot in row:
                spot.draw(win)
        self.draw_grid(win)
        display.update()

    def get_clicked_pos(self, pos):
        y, x = pos
        row = y // self.gap
        col = x // self.gap
        return row, col
