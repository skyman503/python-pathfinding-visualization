import pygame


def sort_nodes_by_distance(unvisited_nodes):
    unvisited_nodes = sorted(unvisited_nodes, key=lambda x: x.distance)
    return unvisited_nodes


def get_unvisited_neighbors(node, grid):
    neighbors = node.update_neighbors(grid)
    unvisited = []
    for neighbor in neighbors:
        if not neighbor.visited:
            unvisited.append(neighbor)
    return unvisited


def update_unvisited_neighbors(node, grid, end_node):
    unvisited_neighbors = get_unvisited_neighbors(node, grid)
    for neighbor in unvisited_neighbors:
        neighbor.distance = node.distance + 1
        neighbor.prev_node = node
        if neighbor != end_node:
            neighbor.make_open()


def get_all_nodes(grid):
    all_nodes = []
    for row in grid:
        for node in row:
            all_nodes.append(node)
    return all_nodes


def get_shortest_path(end_node):
    nodes_shortest_path = []
    current_node = end_node
    while current_node is not None:
        nodes_shortest_path.insert(0, current_node)
        current_node = current_node.prev_node
    return nodes_shortest_path


def dijkstra(grid_object, start_node, end_node, window):
    visited_nodes_in_order = []
    if start_node == end_node or start_node is None or end_node is None:
        return False
    start_node.set_distance(0)
    unvisited_nodes = get_all_nodes(grid_object.grid)
    while len(unvisited_nodes) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        unvisited_nodes = sort_nodes_by_distance(unvisited_nodes)
        closest_node = unvisited_nodes.pop(0)
        if closest_node.is_wall():
            continue
        if closest_node.distance == float("inf"):
            return visited_nodes_in_order
        closest_node.visited = True
        visited_nodes_in_order.append(closest_node)
        for node in visited_nodes_in_order:
            if node != start_node and node != end_node:
                node.make_closed()
        if closest_node == end_node:
            return visited_nodes_in_order
        update_unvisited_neighbors(closest_node, grid_object.grid, end_node)
        grid_object.draw(window)
