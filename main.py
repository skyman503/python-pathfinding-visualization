import pygame
from json import load
from core.models import Grid
from core.algorithms import astar, dijkstra
with open(r'config\config.json', mode='r') as config_file:
    config = load(config_file)

WIDTH = config["screen_width"]
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")


def main(win, width):
    grid_object = Grid(config["ROWS"], width)
    grid = grid_object.make_grid()
    start_node = None
    end_node = None
    run = True
    working = False
    while run:
        grid_object.draw(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = grid_object.get_clicked_pos(pos)
                node = grid[row][col]
                if not start_node and node != end_node:
                    start_node = node
                    start_node.make_start()
                elif not end_node and node != start_node:
                    end_node = node
                    end_node.make_end()
                elif node != end_node and node != start_node:
                    node.make_wall()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = grid_object.get_clicked_pos(pos)
                node = grid[row][col]
                node.reset()
                if node == start_node:
                    start_node = None
                elif node == end_node:
                    end_node = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start_node and end_node and not working:
                    working = True
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    astar.algorithm(lambda: grid_object.draw(win), grid, start_node, end_node)
                if event.key == pygame.K_d and start_node and end_node and not working:
                    dijkstra.dijkstra(grid_object, start_node, end_node, WIN)
                    shortest_path = dijkstra.get_shortest_path(end_node)
                    for node in shortest_path:
                        if node != start_node and node != end_node:
                            node.make_path()
                if event.key == pygame.K_c:
                    working = False
                    start_node = None
                    end_node = None
                    grid = grid_object.make_grid()
    pygame.quit()


main(WIN, WIDTH)
