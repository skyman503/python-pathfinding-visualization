import pygame
from queue import PriorityQueue


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw, start_node):
    while current in came_from:
        current = came_from[current]
        if current != start_node:
            current.make_path()
        draw()


def algorithm(draw, grid, start_node, end_node):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start_node))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start_node] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start_node] = h(start_node.get_pos(), end_node.get_pos())
    open_set_hash = {start_node}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end_node:
            reconstruct_path(came_from, end_node, draw, start_node)
            end_node.make_end()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end_node.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start_node:
            current.make_closed()
    return False
