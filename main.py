import math, pygame
import random

from pygame.math import Vector2

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
TEAL = [0, 255, 255]

class Node:
    storage = []
    start = None
    target = None
    directions = [
        [0, 1], [0, -1],
        [1, 0], [-1, 0],
        [1, 1], [-1, -1],
        [1, -1], [-1, 1]
    ]

    def __init__(self, _position: Vector2, _walkable):
        self.position = Vector2(_position)
        self.walkable = _walkable
        self.neighbors = []
        self.parent = None  # path to node from start
        self.checked = False
        self.end_node = False

        # A* Algorithm
        self.g = 1  # G: If using 4 directions, always will be 1
        self.cost = 0

        Node.storage.append(self)

    # The heuristic: we are using the Euclidean Distance formula
    def get_cost(self, goal):
        self.cost = self.position.distance_to(Node.start.position) + self.position.distance_to(goal.position)

    def get_neighbors(self):
        neighbors = []

        for n in Node.storage:
            if not n.walkable:
                continue

            if self.position.x == n.position.x and self.position.y - 1 == n.position.y:  # UP
                neighbors.append(n)
            elif self.position.x == n.position.x and self.position.y + 1 == n.position.y:  # DOWN
                neighbors.append(n)
            elif self.position.x - 1 == n.position.x and self.position.y == n.position.y:  # LEFT
                neighbors.append(n)
            elif self.position.x + 1 == n.position.x and self.position.y == n.position.y:  # RIGHT
                neighbors.append(n)

        return neighbors

    def draw_self(self, surf):
        color = WHITE

        if self == Node.start:
            color = GREEN
        elif self == Node.target:
            color = RED
        elif self.end_node:
            color = TEAL
        elif self.checked:
            color = BLUE
        elif not self.walkable:
            color = BLACK

        pygame.draw.rect(surf, color, [
            self.position.x * TILE_SIZE,
            self.position.y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        ])

MAP_WIDTH = 50
MAP_HEIGHT = 30
TILE_SIZE = 32

def generate_map():
    Node.storage.clear()

    for h in range(0, MAP_HEIGHT):
        for w in range(0, MAP_WIDTH):
            num = random.randrange(0, 3)  # 0-3
            if num == 0:
                Node([w, h], False)
            else:
                Node([w, h], True)

    Node.start = Node.storage[random.randrange(0, len(Node.storage))]
    Node.target = Node.storage[random.randrange(0, len(Node.storage))]

    if not Node.start.walkable or not Node.target.walkable:
        generate_map()
        return

    print("Generated map: " + str(len(Node.storage)))

def reconstruct_path(target):

    if target.parent is None:
        print("error")
        return None

    n = target.parent
    while n is not None:
        n.end_node = True
        n = n.parent

    print("Path found!")

def pathfinder(target):
    target.target = True

    open_list = []  # Nodes we are considering for closed_list
    explored = []  # Finished list?

    open_list.append(Node.start)  # Initialize the list with START
    Node.start.get_cost(target)

    while len(open_list) > 0:
        current = open_list[0]

        for n in open_list:
            if n.cost < current.cost or n.cost == current.cost:
                current = n
            else:
                continue

        open_list.remove(current)

        current.checked = True

        # get neighboring nodes
        # set the neighboring nodes parent to current
        for n in current.get_neighbors():
            # if our neighbor is the target node, we are done with the pathfinding
            if n == target:
                n.parent = current
                reconstruct_path(current)
                # Reverse calculate the path and return it
                return
            elif n in explored:
                continue
            elif not n.walkable:
                continue

            n.get_cost(target)

            n.parent = current

            explored.append(current)
            if n not in open_list:
                open_list.append(n)

    print("No path was found!")

generate_map()

# Start the pathfinder and give it the target node
pathfinder(Node.target)

window = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                generate_map()
                pathfinder(Node.target)

    window.fill(WHITE)

    for n in Node.storage:
        n.draw_self(window)

    pygame.display.flip()

pygame.quit()