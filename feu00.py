"""Echauffement"""
"""Créez un programme qui affiche un rectangle dans le terminal.

Exemples d’utilisation :
$> python exo.py 5 3
o---o
|   |
o---o

$> python exo.py 5 1
o---o

$> python exo.py 1 1
o

Gérer les problèmes potentiels d’arguments."""


######################   Partie 1 :  Fonctions utilisées   ######################




import sys
def display_rectangle(rectangle_width: int, rectangle_height: int) -> None:

    corner_character = "o"
    horizontal_character = "-"
    vertical_character = "|"
    empty_character = " "

    first_or_last_line = corner_character + horizontal_character * \
        (rectangle_width - 2) + (corner_character if rectangle_width > 1 else "")

    intermediate_line = vertical_character + empty_character * \
        (rectangle_width - 2) + (vertical_character if rectangle_width > 1 else "")

    for i in range(rectangle_height):
        if i == 0 or i == rectangle_height - 1:
            print(first_or_last_line)
        else:
            print(intermediate_line)

    return None


#######################   Partie 2 :  Gestion d'erreur   ########################

def is_valid_arguments(is_number_of_argument_expected: bool) -> bool:

    if not is_number_of_argument_expected:
        print("Error : le nombre d'arguments n'est pas valide")
        return False

    return True


def is_digit(string: str) -> bool:

    for character in string:
        if not "0" <= character <= "9":
            print(f"Error, '{string}' n'est pas un nombre entier positif")
            return False

    return True


def is_greater_than(is_min_rectangle_size: bool) -> bool:

    if not is_min_rectangle_size:
        print(f"Error, la taille minimum de votre rectangle doit etre de 1x1")
        return False

    return True


############################   Partie 3 :  Parsing   ############################

def get_arguments() -> list[str]:

    arguments = sys.argv[1:]

    return arguments


##########################   Partie 4 :  Résolution   ###########################

def get_rectangle() -> None:

    arguments = get_arguments()

    if not is_valid_arguments(len(arguments) == 2):
        return None

    for argument in arguments:
        if not is_digit(argument):
            return
    numbers = list(map(int, arguments))

    for number in numbers:
        if not is_greater_than(number >= 1):
            return

    rectangle_width = numbers[0]
    rectangle_height = numbers[1]

    display_rectangle(rectangle_width, rectangle_height)

    return None


###########################   Partie 5 :  Affichage   ###########################

get_rectangle()
