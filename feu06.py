"""Labyrinthe"""
import sys
import pathlib

import feu07

PATH = pathlib.Path.cwd()
ANNEX_PATH = PATH / "annexe"

######################   Partie 1 :  Fonctions utilisées   ######################


def read_file(file_path: pathlib.Path) -> str:

    with open(file_path, "r") as objet_file:
        file_content = objet_file.read()

    return file_content


def get_reading_parameters(file_content: str) -> tuple[int, int, str, str, str, str, str]:

    first_row = file_content.split("\n")[0]

    height = first_row[0]

    for character in first_row[1:]:
        if character not in "0123456789":
            break
        else:
            height += character

    index_x = file_content.find("x")

    width = first_row[index_x + 1]

    for character in first_row[index_x + 2:]:
        if character not in "0123456789":
            break
        else:
            width += character

    wall_character = first_row[-5]
    path_character = first_row[-4]
    solution_character = first_row[-3]
    start_character = first_row[-2]
    goal_character = first_row[-1]
    height = int(height)
    width = int(width)

    return height, width, wall_character, path_character, solution_character, start_character, goal_character


def heuristic(start: tuple[int, int], goal: tuple[int, int]) -> int:

    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


def get_neighbors(position: tuple[int, int], labyrinth: list[list[str]],
                  wall_character: str) -> list[tuple[int, int]]:

    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for direction in directions:
        neighbor = (position[0] + direction[0], position[1] + direction[1])
        if (0 <= neighbor[0] < len(labyrinth) and
            0 <= neighbor[1] < len(labyrinth[0]) and
                labyrinth[neighbor[0]][neighbor[1]] != wall_character):
            neighbors.append(neighbor)

    return neighbors


def reconstruct_path(came_from: dict[tuple[int, int], tuple[int, int]],
                     current: tuple[int, int]) -> list[tuple[int, int]]:

    total_path = [current]

    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)

    return total_path


def a_star(labyrinth: list[list[str]], start: tuple[int, int], goal: tuple[int, int],
           wall_character: str) -> str | None | list[tuple[int, int]]:

    open_set = [(0, start)]
    came_from = {}
    # g_score est le coût pour atteindre un noeud depuis le départ.
    g_score = {start: 0}
    # f_score est le coût total estimé pour atteindre l'arrivée
    # en passant par un noeud (g_score + heuristic).
    f_score = {start: heuristic(start, goal)}

    while open_set:
        open_set.sort(key=lambda x: x[0])
        current = open_set[0][1]
        open_set.pop(0)

        if current == goal:
            return reconstruct_path(came_from, current)

        neighbors = get_neighbors(current, labyrinth, wall_character)

        for neighbor in neighbors:
            attempt_g_score = g_score.get(current) + 1  # type: ignore

            if attempt_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = attempt_g_score
                f_score[neighbor] = attempt_g_score + heuristic(neighbor, goal)

                if neighbor not in [i[1] for i in open_set]:
                    open_set.append((f_score[neighbor], neighbor))

    return None


def solve_labyrinth(labyrinth_input: str, height: int, width: int, wall_character: str,
                    path_character: str, solution_character: str, start_character: str,
                    goal_character: str) -> str:

    labyrinth_rows = labyrinth_input.split("\n")[1:]
    labyrinth = [list(row) for row in labyrinth_rows]
    start = (0, 0)
    goal = (0, 0)
    color_solution_character = f'\033[32m{solution_character}\033[0m'

    for i in range(height):
        for j in range(width):
            if labyrinth[i][j] == start_character:
                start = (i, j)
            elif labyrinth[i][j] == goal_character:
                goal = (i, j)

    path = a_star(labyrinth, start, goal, wall_character)

    if path is None:
        return "Ce labyrinthe est sans issue.\n\n" + labyrinth_input

    for (x, y) in path:
        if labyrinth[x][y] not in (start_character, goal_character):  # type: ignore
            labyrinth[x][y] = color_solution_character  # type: ignore

    solved_labyrinth_str = '\n'.join([''.join(row) for row in labyrinth])
    number_of_strokes = len(path) - 1
    solved_labyrinth_and_number_of_strokes_str = solved_labyrinth_str + f"\n\nSORTIE ATTEINTE EN {
        number_of_strokes} COUPS !"

    return solved_labyrinth_and_number_of_strokes_str


#######################   Partie 2 :  Gestion d'erreur   ########################

def is_valid_arguments(is_number_of_argument_expected: bool) -> bool:
    if not is_number_of_argument_expected:
        print("Error : Vous ne pouvez pas donner plus d'un labyrinth à résoudre")
        return False
    return True


def is_valid_file_name(is_valid_file_name: bool) -> bool:
    if not is_valid_file_name:
        print("Error, vous devez saisir les noms du fichier avec l'extention : .txt")
        return False
    return True


def is_exists_file(file_path: pathlib.Path) -> bool:
    if not pathlib.Path.exists(file_path):
        print(f"\033[31mFichier non trouvé :\033[0m {file_path}")
        return False
    return True


def is_valid_labyrinth_file(file_content: str) -> bool:

    def is_not_empty_file(file_content: str) -> bool:
        if len(file_content) == 0:
            print("Error, le fichier est vide")
            return False
        return True

    def is_min_len_first_row(file_content: str) -> bool:
        if len(first_row) < 8:
            print("Error 1,", error)
            return False
        return True

    def get_height(first_row: str) -> bool | str:
        if first_row[0] not in "123456789":
            print(
                "Error 2, le paramètre hauteur doit etre exprimé avec un entier positif,\n", error)
            return False
        height = first_row[0]

        for character in first_row[1:]:
            if character not in "0123456789":
                break
            else:
                height += character

        if int(height) < min_height:
            print(f"Error , la hauteur du labyrinth ne peut etre inférieur à {
                  min_height}")
            return False
        return height

    def is_valid_separator_height_width(first_row: str) -> bool:
        for character in first_row:
            if character not in "0123456789x":
                print(
                    "Error 3, les paramètres de hauteur et largeur doivent être séparé par le caractère 'x',\n", error)
                return False
            if character == "x":
                return True
        return False

    def get_width(first_row: str) -> bool | str:
        index_x = file_content.find("x")

        if not first_row[index_x + 1].isdigit():
            print(
                "Error 4, le paramètre largeur doit etre exprimé avec un entier positif,\n", error)
            return False

        width = first_row[index_x + 1]

        for character in first_row[index_x + 2:]:
            if character not in "0123456789":
                break
            else:
                width += character

        if int(width) < min_width:
            print(f"Error , la largeur du labyrinth ne peut etre inférieur à {
                  min_width}")
            return False

        return width

    def is_valid_number_of_settings(first_row: str, height: str, width: str):

        len_of_settings = 5

        # -1 pour le x séparateur
        if len_of_settings != len(first_row) - len(height) - len(width) - 1:
            print("Error 5, Après les paramètre de Hauteur et largeur, vous devez saisir 5 caractères désignant respectivement;\nles murs, les passages, le chemin le plus court, le départ et enfin l'arrivé")
            return False

        return True

    def is_valid_height(file_content, height):
        file_rows = file_content.split("\n")
        len_labyrinth_rows = len(file_rows) - 1
        if len_labyrinth_rows != int(height):
            print("Error , La hauteur du labyrinth doit correspondre a la valeur renseigné dans la ligne de paramètre et il ne doit pas y avoir de ligne vide")
            return False
        return True

    def is_valid_width(file_content, width):
        labyrinth_rows = file_content.split("\n")[1:]
        for row in labyrinth_rows:
            if len(row) != int(width):
                print("Error , La largeur du labyrinth sur chaque ligne doit correspondre à la valeur renseigné dans la ligne de paramètre")
                return False
        return True

    def is_only_allowed_character(file_content: str, first_row: str):

        characters_allowed = [first_row[-5], first_row[-4],
                              first_row[-2], first_row[-1]]
        labyrinth_rows = file_content.split("\n")[1:]

        for row in labyrinth_rows:
            for i in row:
                if i not in characters_allowed:
                    print(
                        "Le labyrinth ne peut etre construit qu'avec les caratères renségné dans la ligne des paramètres")
                    return False
        return True

    def is_valid_start(file_content: str, first_row: str):
        start_character = first_row[-2]
        labyrinth_rows = file_content.split("\n")[1:]
        count_of_start = 0

        for row in labyrinth_rows:
            for i in row:
                if i == start_character:
                    count_of_start += 1

        if count_of_start == 0:
            print("Error, le labyrinth doit comporter un départ")
        elif count_of_start > 1:
            print("Error, le labyrinth doit comporter un seul départ")

        return True

    def is_valid_goal(file_content: str, first_row: str):
        goal_character = first_row[-1]
        labyrinth_rows = file_content.split("\n")[1:]
        count_of_start = 0

        for row in labyrinth_rows:
            for i in row:
                if i == goal_character:
                    count_of_start += 1

        if count_of_start == 0:
            print("Error, le labyrinth doit comporter au moins une sortie")

        return True

    min_height = 4
    min_width = 4

    error = """\tLa première ligne du fichier doit se composer comme suit:
        \033[31mhauteur\033[33mx\033[31mlargeur\033[33mmur\033[31mchemin\033[33mchemin_le_plus_court\033[31mdépart\033[33marrivé\033[0m
        Exemple:
        10x10* o12"""

    if not is_not_empty_file(file_content):
        return False

    first_row = file_content.split("\n")[0]

    if not is_min_len_first_row(file_content):
        return False

    height = get_height(first_row)

    if not height:
        return False

    if not is_valid_separator_height_width(first_row):
        return False

    width = get_width(first_row)

    if not width:
        return False

    if not is_valid_number_of_settings(first_row, height, width):  # type: ignore
        return False

    if not is_valid_height(file_content, height):
        return False

    if not is_valid_width(file_content, width):
        return False

    if not is_only_allowed_character(file_content, first_row):
        return False

    if not is_valid_start(file_content, first_row):
        return False

    if not is_valid_goal(file_content, first_row):
        return False

    return True


############################   Partie 3 :  Parsing   ############################

def get_arguments() -> list[str]:
    arguments = sys.argv
    return arguments


##########################   Partie 4 :  Résolution   ###########################

def find_shortest_path() -> str | None:
    arguments = get_arguments()
    if not is_valid_arguments(len(arguments) <= 2):
        return

    if len(arguments) == 2:
        file_name = arguments[1]
        if not is_valid_file_name(file_name.endswith(".txt")):
            return
        file_path = ANNEX_PATH / file_name

        if not is_exists_file(file_path):
            return

        labyrinth_input = read_file(file_path)

    else:
        labyrinth_input = feu07.labyrinth_generator()

    if not is_valid_labyrinth_file(labyrinth_input):
        return

    height, width, wall_character, path_character, solution_character, start_character, goal_character = get_reading_parameters(
        labyrinth_input)

    solved_labyrinth = solve_labyrinth(labyrinth_input, height, width, wall_character,
                                       path_character, solution_character, start_character, goal_character)

    return solved_labyrinth

###########################   Partie 5 :  Affichage   ###########################


def display_solved_labyrinth() -> None:
    solved_labyrinth_str = find_shortest_path()
    if solved_labyrinth_str is not None:
        print(f"Labyrinthe avec le chemin :\n\n{solved_labyrinth_str}")

    return


display_solved_labyrinth()
