"""Labyrinthe : annexe"""

import random
import pathlib


height = 12
width = 55
wall_character = "█"  # chars[0]
empty_character = " "  # chars[1]
path_character = "+"  # chars[2]
start_character = "1"  # chars[3]
end_character = "2"  # chars[4]
folder_path = "annexe"
file_name = "labyrinth.txt"

CURRENT_PATH = pathlib.Path.cwd()
PATH = CURRENT_PATH / folder_path
FILE_WITH_PATH = PATH / file_name


######################   Partie 1 :  Fonctions utilisées   ######################

def write_file(content_file: str) -> None:

    with open(FILE_WITH_PATH, "w") as objet_file:
        objet_file.write(content_file)

    return None


def labyrinth_generator():

    chars = f"{wall_character}{empty_character}{
        path_character}{start_character}{end_character}"
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

    labyrinth_str = str(height)+"x"+str(width)+chars+"\n"

    for y in range(height):
        for x in range(width):
            if y == entry_y and x == entry_x:
                labyrinth_str += start_character
            elif y == exit_y and x == exit_x:
                labyrinth_str += end_character
            elif (1 <= y <= height - 2 and 1 <= x <= width - 2 and random.randint(0, 100) > 20) or ():
                labyrinth_str += empty_character
            elif (entry_must_path_x == x and entry_must_path_y == y) or (exit_must_path_x == x and exit_must_path_y == y):
                labyrinth_str += empty_character
            else:
                labyrinth_str += wall_character
        if y != height - 1:
            labyrinth_str += "\n"

    return labyrinth_str

#######################   Partie 2 :  Gestion d'erreur   ########################


############################   Partie 3 :  Parsing   ############################


##########################   Partie 4 :  Résolution   ###########################

def get_labyrinth_file() -> None:

    labyrinth = labyrinth_generator()

    write_file(labyrinth)

    print("Labyrinthe généré avec succes.")
    return

###########################   Partie 5 :  Affichage   ###########################


if __name__ == "__main__":

    get_labyrinth_file()
