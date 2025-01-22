"""Trouver le plus grand carré"""
# Créez un programme qui remplace les caractères vides par des caractères plein pour représenter le plus grand carré possible sur un plateau. Le plateau sera transmis dans un fichier. La première ligne du fichier contient les informations pour lire la carte : nombre de lignes du plateau, caractères pour “vide”, “obstacle” et “plein”.


# Exemples d’utilisation :
# $> cat plateau
# 9.xo
# ...........................
# ....x......................
# ............x..............
# ...........................
# ....x......................
# ...............x...........
# ...........................
# ......x..............x.....
# ..x.......x................
# $> ruby exo.rb plateau
# .....ooooooo...............
# ....xooooooo...............
# .....ooooooox..............
# .....ooooooo...............
# ....xooooooo...............
# .....ooooooo...x...........
# .....ooooooo...............
# ......x..............x.....
# ..x.......x................

# Vous devez gérer les potentiels problèmes d’arguments, de fichiers, ou de carte invalide.

# Une carte est valide uniquement si : les lignes ont toute la même longueur, il y a au moins une ligne d’une case, les lignes sont séparées d’un retour à la ligne, les caractères présents dans la carte sont uniquement ceux de la première ligne

# En cas de plusieurs solutions, le carré le plus en haut à gauche sera choisi.

# Vous trouverez un générateur de plateau sur la feuille suivante.


import pathlib
import sys

annexe_folder_path = "annexe"

CURRENT_PATH = pathlib.Path.cwd()
ANNEXE_FOLDER_PATH = CURRENT_PATH / annexe_folder_path


######################   Partie 1 :  Fonctions utilisées   ######################


def read_file(file_path: pathlib.Path) -> str:

    with open(file_path, "r") as objet_file:
        file_content = objet_file.read()

    return file_content


def get_plate_list(plate_str: str) -> list[tuple[int, int, str]]:

    plate_without_settings = plate_str.split("\n", 1)[1]
    plate_list = []
    x = 0
    y = 0

    for character in plate_without_settings:
        if character == "\n":
            y += 1
            x = 0
            continue
        plate_list.append([x, y, character])
        x += 1

    return plate_list


def get_reading_parameters(file_content: str) -> tuple[int, str, str, str]:

    settings = file_content.split("\n")[0]

    number_of_rows = settings[0]

    for character in settings[1:]:
        if character not in "0123456789":
            break
        else:
            number_of_rows += character

    empty_character = settings[len(number_of_rows)]
    obstacle_character = settings[len(number_of_rows) + 1]
    display_square_character = settings[len(number_of_rows) + 2]

    number_of_rows = int(number_of_rows)

    return number_of_rows, empty_character, obstacle_character, display_square_character


def get_biggest_square(obstacle_character: str, plate_list: list[tuple[int, int, str]]) -> tuple[tuple[int, int], tuple[int, int]]:

    start_coordinates = (0, 0)
    end_coordinates = (0, 0)
    air_of_square = 0
    temp_start_coordinates = (0, 0)
    temp_end_coordinates = (0, 0)

    for i in range(len(plate_list)):

        if plate_list[i][2] == obstacle_character:
            continue

        temp_start_coordinates = (plate_list[i][0], plate_list[i][1])
        temp_end_coordinates = (plate_list[i][0], plate_list[i][1])
        last_x_possible = None

        for j in range(i, len(plate_list)):
            if (plate_list[j][0] < temp_start_coordinates[0] or
                    plate_list[j][1] < temp_start_coordinates[1]):
                continue
            if last_x_possible is not None and plate_list[j][0] >= last_x_possible:
                continue
            if plate_list[j][2] == obstacle_character:
                last_x_possible = plate_list[j][0]
                continue

            temp_end_coordinates = (plate_list[j][0], plate_list[j][1])

            if (temp_end_coordinates[0] - temp_start_coordinates[0]) != (
                    temp_end_coordinates[1] - temp_start_coordinates[1]):
                continue

            temp_air_of_square = (temp_end_coordinates[0] - temp_start_coordinates[0] + 1)*(
                temp_end_coordinates[1] - temp_start_coordinates[1] + 1)

            if temp_air_of_square > air_of_square:
                start_coordinates = (
                    temp_start_coordinates[0], temp_start_coordinates[1])
                end_coordinates = (
                    temp_end_coordinates[0], temp_end_coordinates[1])
                air_of_square = temp_air_of_square

    return start_coordinates, end_coordinates


def get_plate_with_display_square_character(display_square_character: str, plate_list: list[tuple[int, int, str]],
                                            start_coordinates: tuple[int, int], end_coordinates: tuple[int, int]) -> list[tuple[int, int, str]]:

    new_plate = []
    color_square_character = f"\033[31m{display_square_character}\033[0m"

    for i in plate_list:
        if start_coordinates[0] <= i[0] <= end_coordinates[0] and start_coordinates[1] <= i[1] <= end_coordinates[1]:
            new_plate.append([i[0], i[1], color_square_character])
        else:
            new_plate.append(i)

    return new_plate


def get_string_from_list(plate_list: list[tuple[int, int, str]]) -> str:

    plate_str = ""
    line_index = 0

    for i in plate_list:
        if i[1] != line_index:
            plate_str += "\n"
            line_index = i[1]
        plate_str += str(i[2])

    return plate_str


#######################   Partie 2 :  Gestion d'erreur   ########################

def is_valid_arguments(is_number_of_argument_expected: bool) -> bool:

    if not is_number_of_argument_expected:
        print("Error : Vous devez saisir le nom du fichier .txt qui contient le plateau")
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


def is_valid_plateau(file_content: str) -> bool:

    firts_line = file_content.split("\n")[0]

    if len(firts_line) < 4:
        print("Error 1, la premiere ligne du fichier doit contenir 4 paramètres\nEn premier ; le nombre de ligne du Plateau\nEn deuxième ; le caractère vide\nEn troisième ; le caractère obstacle\nEn quatrième ; le caractère plein")
        return False

    number_of_rows = firts_line[0]

    if firts_line[0] not in "123456789":
        print("Error 2, le premier character de la premiere ligne du fichier doit contenir le nombre de lignes du plateau")
        return False

    for character in firts_line[1:]:
        if character not in "0123456789":
            break
        else:
            number_of_rows += character

    if len(firts_line) != len(number_of_rows) + 3:
        print("Error 3, la premiere ligne du fichier doit contenir 4 paramètres\nEn premier ; le nombre de ligne du Plateau\nEn deuxième ; le caractère vide\nEn troisième ; le caractère obstacle\nEn quatrième ; le caractère plein")
        return False

    empty_character = firts_line[len(number_of_rows)]
    obstacle_character = firts_line[len(number_of_rows) + 1]
    display_square_character = firts_line[len(number_of_rows) + 2]

    number_of_rows = int(number_of_rows)

    rows = file_content.split("\n")
    plate = rows[1:]

    for row in plate:
        for character in row:
            if character not in [empty_character, obstacle_character]:
                print(f"Error 4, la carte doit contenir uniquement les caractères suivants : '{
                    empty_character}'' ou '{obstacle_character}'")
                return False

    if len(rows) < 2:
        print('Error 5, le plateau doit contenir au moins une ligne')
        return False

    if len(plate[0]) < 1:
        print('Error 6, le plateau doit contenir au moins un caratère par ligne')
        return False

    for row in plate:
        if len(row) != len(plate[0]):
            print(
                "Error 7, toutes les lignes du plateau doivent être de la même longueur")
            return False

    if len(plate) != number_of_rows:
        print("Error 8, le nombre de ligne du plateau doit correspondre à la valeur du premier paramètre dans la premiere ligne du fichier")
        return False

    return True


############################   Partie 3 :  Parsing   ############################

def get_arguments() -> list[str]:

    arguments = sys.argv[1:]

    return arguments


##########################   Partie 4 :  Résolution   ###########################
def find_biggest_square():

    arguments = get_arguments()

    if not is_valid_arguments(len(arguments) == 1):
        return None

    file_name = arguments[0]

    if not is_valid_file_name(file_name.endswith(".txt")):
        return None

    file_path = ANNEXE_FOLDER_PATH / file_name

    if not is_exists_file(file_path):
        return None

    file_content = read_file(file_path)

    if not is_valid_plateau(file_content):
        return None

    print("\n", "-" * 14, " Plateau proposé ",
          "-" * 14, "\n\n", file_content, "\n\n", sep="")

    number_of_rows, empty_character, obstacle_character, display_square_character = get_reading_parameters(
        file_content)

    plate_list = get_plate_list(file_content)

    start_coordinates, end_coordinates = get_biggest_square(
        obstacle_character, plate_list)

    plate_with_biggest_square = get_plate_with_display_square_character(
        display_square_character, plate_list, start_coordinates, end_coordinates)

    plate_with_biggest_square_str = get_string_from_list(
        plate_with_biggest_square)

    print("-" * 5, " Plateau avec le plus grand carré ",
          "-" * 6, "\n\n", plate_with_biggest_square_str, "\n", sep="")


###########################   Partie 5 :  Affichage   ###########################

find_biggest_square()
