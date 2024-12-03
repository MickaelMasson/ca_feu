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

import sys

# Fonctions utilisées
def display_rectangle(rectangle_width: int, rectangle_height: int) :
    angle_character = "o"
    horizontal_character = "-"
    vertical_character = "|"
    space_character = " "
    first_and_last_line = angle_character + horizontal_character * (rectangle_width - 2) + (angle_character if rectangle_width > 1 else "")
    intermediate_line = vertical_character + space_character * (rectangle_width - 2) + (vertical_character if rectangle_width > 1 else "")
    for i in range(1, rectangle_height + 1) :
        if i == 1 or i == rectangle_height :
            print(first_and_last_line)
        else :
            print(intermediate_line)
    return

# Partie 1 : Gestion d'erreur
def is_valid_arguments(arguments: list[str], number_of_argument: int) -> bool:
    if len(arguments) != number_of_argument :
        print("Error, le nombre d'arguments n'est pas valide")
        return False
    return True
    
def is_digit(string: str) -> bool:
    for character in string :
        if not "0" <= character <= "9" :
            print(f"Error, '{string}' n'est pas un nombre entier positif")
            return False
    return True

def is_greater_than(argument: int, index: int) -> bool:
    if argument < index :
        print(f"Error, la taille minimum de votre rectangle doit supérieur ou égale à {index}")
        return False
    return True

# Partie 2 : Parsing
def get_arguments() -> list[str] :
    arguments = sys.argv[1:]
    return arguments

# Partie 3 : Résolution
def get_rectangle() :
    arguments = get_arguments()
    number_of_argument_expected = 2
    if not is_valid_arguments(arguments, number_of_argument_expected) :
        return
    for argument in arguments :
        if not is_digit(argument) :
            return
    numbers = list(map(int, arguments))
    min_rectangle_size = 1
    for number in numbers :
        if not is_greater_than(number, min_rectangle_size) :
            return
    rectangle_width = numbers[0]
    rectangle_height = numbers[1]

    display_rectangle(rectangle_width, rectangle_height)

# Partie 4 : Affichage
get_rectangle()