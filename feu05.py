"""Trouver le plus grand carré : annexe"""
# Voici un générateur de plateau écrit en Ruby :


# if ARGV.count != 3
#     puts "params needed: x y density"
#     exit
# end

# x = ARGV[0].to_i
# y = ARGV[1].to_i
# density = ARGV[2].to_i

# puts "#{y}.xo"
# for i in 0..y do
#     for j in 0..x do
#         print ((rand(y) * 2 < density) ? 'x' : '.')
#     end
#     print "\n"
# end


import random
import pathlib
import sys

empty_character = '⋅'
obstacle_character = 'X'
display_square_character = '█'
folder_path = "annexe"
file_name = "plateau.txt"

CURRENT_PATH = pathlib.Path.cwd()
PATH = CURRENT_PATH / folder_path
FILE_WITH_PATH = PATH / file_name


######################   Partie 1 :  Fonctions utilisées   ######################

def write_file(content_file: str) -> None:

    with open(FILE_WITH_PATH, "w") as objet_file:
        objet_file.write(content_file)

    return None


def board_generator(x: int, y: int, density: int) -> str:

    board_str = f"{y}{empty_character}{
        obstacle_character}{display_square_character}\n"

    for i in range(y):
        for _j in range(x):
            board_str += obstacle_character if random.randint(
                0, y * 2) < density else empty_character
        if i < y - 1:
            board_str += "\n"

    return board_str


#######################   Partie 2 :  Gestion d'erreur   ########################

def is_valid_arguments(is_number_of_argument_expected: bool) -> bool:

    if not is_number_of_argument_expected:
        print("Error : Vous devez saisir 3 nombres entiers, respectivement pour la 'largeur du plateau', la 'hauteur du plateau' et la 'densité du plateau'")
        return False

    return True


def is_valid_density(density: int, y: int) -> bool:

    if density > y * 2 or density < 1:
        print(f"Error : La densité ne peux dépasser 2y, pour ce plateau de {
              y} de large la densité doit etre comprise entre 1 et {y * 2}")
        return False

    return True


def is_digit(arguments: list[str]) -> bool:

    for argument in arguments:
        if not argument.isdigit():
            print(f"Error : {argument} doit etre un nombre entier")
            return False

    return True


############################   Partie 3 :  Parsing   ############################

def get_arguments() -> list[str]:

    arguments = sys.argv[1:]

    return arguments


##########################   Partie 4 :  Résolution   ###########################

def get_board_file() -> None:

    arguments = get_arguments()

    if not is_valid_arguments(len(arguments) == 3):
        return None

    if not is_digit(arguments):
        return None

    numbers = list(map(int, arguments))

    x, y, density = numbers

    if not is_valid_density(int(density), int(y)):
        return None

    board = board_generator(x, y, density)

    write_file(board)

    print("Plateau généré avec succes.")
    return


###########################   Partie 5 :  Affichage   ###########################
get_board_file()
