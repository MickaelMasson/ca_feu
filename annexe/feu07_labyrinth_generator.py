"""Labyrinthe : annexe"""

import random


def is_neighbours(x, y, labyrinth, wall_char):
    neighbors = []
    # Haut, Bas, Gauche, Droite
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for direction in directions:
        neighbor = (x + direction[0], y + direction[1])
        if (0 <= neighbor[0] < len(labyrinth) and
            0 <= neighbor[1] < len(labyrinth[0]) and
                labyrinth[neighbor[0]][neighbor[1]] != wall_char):
            neighbors.append(neighbor)
    return neighbors


def labyrinth_generator():
    height = 15
    width = 60
    wall = "█"  # chars[0]
    empty = " "  # chars[1]
    way = "+"  # chars[2]
    start = "1"  # chars[3]
    end = "2"  # chars[4]
    chars = f"{wall}{empty}{way}{start}{end}"

    entry_directions = ["north", "east", "south", "west"]
    exit_directions = entry_directions
    place_entry = random.choice(entry_directions)
    exit_directions = entry_directions
    exit_directions.remove(place_entry)
    place_exit = random.choice(exit_directions)

    if place_entry == "north":
        entry_x = random.randint(2, width - 2)
        entry_y = 0
        entry_must_path_x = entry_x
        entry_must_path_y = 1
    elif place_entry == "east":
        entry_x = width - 1
        entry_y = random.randint(2, height - 2)
        entry_must_path_x = width - 2
        entry_must_path_y = entry_y
    elif place_entry == "south":
        entry_x = random.randint(2, width - 2)
        entry_y = height - 1
        entry_must_path_x = entry_x
        entry_must_path_y = height - 2
    elif place_entry == "west":
        entry_x = 0
        entry_y = random.randint(2, height - 2)
        entry_must_path_x = 1
        entry_must_path_y = entry_y

    if place_exit == "north":
        exit_x = random.randint(2, width - 2)
        exit_y = 0
        exit_must_path_x = exit_x
        exit_must_path_y = 1
    elif place_exit == "east":
        exit_x = width - 1
        exit_y = random.randint(2, height - 2)
        exit_must_path_x = width - 2
        exit_must_path_y = exit_y
    elif place_exit == "south":
        exit_x = random.randint(2, width - 2)
        exit_y = height - 1
        exit_must_path_x = exit_x
        exit_must_path_y = height - 2
    elif place_exit == "west":
        exit_x = 0
        exit_y = random.randint(2, height - 2)
        exit_must_path_x = 1
        exit_must_path_y = exit_y

    # print(f"{height}x{width}{chars}")

    labyrinth_str = str(height)+"x"+str(width)+chars+"\n"
    # print(labyrinth_str)

    for y in range(height):
        for x in range(width):
            if y == entry_y and x == entry_x:
                labyrinth_str += start
            elif y == exit_y and x == exit_x:
                labyrinth_str += end
            elif (1 <= y <= height - 2 and 1 <= x <= width - 2 and random.randint(0, 100) > 20) or ():
                labyrinth_str += empty
            elif (entry_must_path_x == x and entry_must_path_y == y) or (exit_must_path_x == x and exit_must_path_y == y):
                labyrinth_str += empty
            else:
                labyrinth_str += wall
        labyrinth_str += "\n"

    return labyrinth_str
