"""Trouver une forme"""
# Créez un programme qui affiche la position de l’élément le plus en haut à gauche (dans l’ordre)
# d’une forme au sein d’un plateau.

# Exemples d’utilisation :
# $> cat board.txt
# 0000
# 1111
# 2331
# $> cat to_find.txt
# 11
#  1
# $> cat unfindable.txt
# 00
# 00

# $> ruby exo.rb board.txt to_find.txt
# Trouvé !
# Coordonnées : 2,1
# ----
# --11
# ---1

# $> ruby exo.rb board.txt unfindable.txt
# Introuvable

# Vous devez gérer les potentiels problèmes d’arguments et de lecture de fichiers.
import pathlib
import sys

PATH = pathlib.Path.cwd()
ANNEX_PATH = PATH / "annexe"


######################   Partie 1 :  Fonctions utilisées   ######################

def get_list_width_and_height(file_path: pathlib.Path) -> tuple[list[tuple[int, int, str]], int, int]:

    content_file = read_file(file_path)
    x_y_character_list = get_x_y_character_list(content_file)
    width, height = size_shape(x_y_character_list)

    return x_y_character_list, width, height


def read_file(file_with_path: pathlib.Path) -> str:

    with open(file_with_path, "r") as objet_file:
        file_content = objet_file.read()

    return file_content


def get_x_y_character_list(string: str) -> list[tuple[int, int, str]]:

    new_list = []
    x = 0
    y = 0
    for character in string:
        if character == "\n":
            y += 1
            x = 0
            continue
        if not character == " ":
            new_list.append((x, y, character))
        x += 1

    return new_list


def size_shape(list_: list[tuple[int, int, str]]) -> tuple[int, int]:

    index_width = 0
    for i in list_:
        if i[0] > index_width:
            index_width = i[0]
    width = index_width + 1

    index_height = 0
    for i in list_:
        if i[1] > index_height:
            index_height = i[1]
    height = index_height + 1

    return width, height


def find_shape(board_list: list[tuple[int, int, str]], width_board: int, height_board: int, to_find_list: list[
        tuple[int, int, str]], width_to_find: int, height_to_find: int) -> list:

    for y in range(height_board - height_to_find + 1):
        for x in range(width_board - width_to_find + 1):
            match_number = 0
            for x_y_character in to_find_list:
                if x_y_character in board_list:
                    match_number += 1
            if match_number == len(to_find_list):
                match_coordinates_list = to_find_list
                return match_coordinates_list

            to_find_list = [(x + 1, y, character)
                            for (x, y, character) in to_find_list]
        to_find_list = [(x - (width_board - width_to_find + 1), y + 1, character)
                        for (x, y, character) in to_find_list]

    return []


def display_result(width_board: int, height_board: int, match_coordinates: list) -> None:

    if len(match_coordinates) == 0:
        print("Introuvable")
        return

    x = match_coordinates[0][0]
    y = match_coordinates[0][1]

    string_display = ""
    for line in range(height_board):
        for column in range(width_board):
            for x_y_character in match_coordinates:
                if column == x_y_character[0] and line == x_y_character[1]:
                    character = x_y_character[2]
                    string_display += character
                    break
            else:
                string_display += "-"
        string_display += "\n"

    return print(f"Trouvé !\nCoordonnées : {x},{y}\n{string_display}")


#######################   Partie 2 :  Gestion d'erreur   ########################
def is_valid_arguments(is_number_of_argument_expected: bool) -> bool:

    if not is_number_of_argument_expected:
        print("Error : le nombre d'arguments n'est pas valide")
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


############################   Partie 3 :  Parsing   ############################

def get_arguments() -> list[str]:

    arguments = sys.argv[1:]

    return arguments


##########################   Partie 4 :  Résolution   ###########################

def get_match() -> None:

    arguments = get_arguments()
    if not is_valid_arguments(len(arguments) == 2):
        return None
    for argument in arguments:
        if not is_valid_file_name(argument.endswith(".txt")):
            return None

    for argument in arguments:
        if not is_exists_file(ANNEX_PATH / argument):
            return None

    board_file_name = arguments[0]
    board_file_path = ANNEX_PATH / board_file_name

    to_find_file_name = arguments[1]
    to_find_file_path = ANNEX_PATH / to_find_file_name

    board_list, width_board, height_board = get_list_width_and_height(
        board_file_path)
    to_find_list, width_to_find, height_to_find = get_list_width_and_height(
        to_find_file_path)

    match_coordinates = find_shape(board_list, width_board, height_board,
                                   to_find_list, width_to_find, height_to_find)

    display_result(width_board, height_board, match_coordinates)

    return


###########################   Partie 5 :  Affichage   ###########################

get_match()
