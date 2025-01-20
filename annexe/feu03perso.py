"""Sudoku"""

import time
import pathlib
import sys

PATH = pathlib.Path.cwd()
ANNEX_PATH = PATH / "annexe"

start_time = time.time()
end_time = time.time()
number_of_solution = 0


######################   Partie 1 :  Fonctions utilisées   ######################

def resolve_sudoku(sudoku: list[tuple[int, int, list[int]]]) -> list[tuple[int, int, list[int]]]:

    def resolve_horizontal(sudoku: list[tuple[int, int, list[int]]]) -> list[tuple[int, int, list[int]]]:

        new_sudoku = sudoku

        for y in range(9):
            new_possible_number_in_cell = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for i in new_sudoku:
                if i[1] == y and len(i[2]) == 1 and i[2][0] in new_possible_number_in_cell:
                    new_possible_number_in_cell.remove(i[2][0])

            for i in new_sudoku:
                if i[1] == y and len(i[2]) > 1:
                    temp_list = []
                    for j in i[2]:
                        if j in new_possible_number_in_cell:
                            temp_list.append(j)
                    i[2] = temp_list  # type: ignore

            for i in new_sudoku:
                if i[1] == y and len(i[2]) > 1:
                    j_is_solution = True
                    for j in i[2]:
                        for k in new_sudoku:
                            if k[1] == y and len(k[2]) > 1:
                                if i[0] == k[0] and i[1] == k[1]:
                                    continue
                                if j in k[2]:
                                    j_is_solution = False
                                    break
                    if j_is_solution:
                        i[2] = [j]  # type: ignore
                        break

        return new_sudoku

    def resolve_vertical(sudoku: list[tuple[int, int, list[int]]]) -> list[tuple[int, int, list[int]]]:

        new_sudoku = sudoku

        for x in range(9):
            new_possible_number_in_cell = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for i in new_sudoku:
                if i[0] == x and len(i[2]) == 1 and i[2][0] in new_possible_number_in_cell:
                    new_possible_number_in_cell.remove(i[2][0])

            for i in new_sudoku:
                if i[0] == x and len(i[2]) > 1:
                    temp_list = []
                    for j in i[2]:
                        if j in new_possible_number_in_cell:
                            temp_list.append(j)
                    i[2] = temp_list  # type: ignore

            for i in new_sudoku:
                if i[0] == x and len(i[2]) > 1:
                    j_is_solution = True
                    for j in i[2]:
                        for k in new_sudoku:
                            if k[0] == x and len(i[2]) > 1:
                                if i[0] == k[0] and i[1] == k[1]:
                                    continue
                                if j in k[2]:
                                    j_is_solution = False
                                    break
                    if j_is_solution:
                        i[2] = j  # type: ignore
                        break

        return new_sudoku

    def resolve_sub_square(sudoku: list[tuple[int, int, list[int]]]) -> list[tuple[int, int, list[int]]]:

        new_sudoku = sudoku

        for x in range(3):
            for y in range(3):
                new_possible_number_in_cell = [1, 2, 3, 4, 5, 6, 7, 8, 9]

                for i in new_sudoku:
                    if (x*3) <= i[0] <= ((x*3) + 2) and (y*3) <= i[1] <= ((y*3) + 2) and len(i[2]) == 1 and i[2][0] in new_possible_number_in_cell:
                        new_possible_number_in_cell.remove(i[2][0])

                for i in new_sudoku:
                    if (x*3) <= i[0] <= ((x*3) + 2) and (y*3) <= i[1] <= ((y*3) + 2) and len(i[2]) > 1:
                        temp_list = []
                        for j in i[2]:
                            if j in new_possible_number_in_cell:
                                temp_list.append(j)
                        i[2] = temp_list  # type: ignore

                for i in new_sudoku:
                    if (x*3) <= i[0] <= ((x*3) + 2) and (y*3) <= i[1] <= ((y*3) + 2) and len(i[2]) > 1:
                        j_is_solution = True
                        for j in i[2]:
                            for k in new_sudoku:
                                if (x*3) <= k[0] <= ((x*3) + 2) and (y*3) <= k[1] <= ((y*3) + 2) and len(i[2]) > 1:
                                    if i[0] == k[0] and i[1] == k[1]:
                                        continue
                                    if j in k[2]:
                                        j_is_solution = False
                                        break
                        if j_is_solution:
                            i[2] = j  # type: ignore
                            break

        return new_sudoku

    repr_input_sudoku = repr(sudoku)
    new_sudoku = resolve_sub_square(
        resolve_vertical(resolve_horizontal(sudoku)))

    if repr_input_sudoku != repr(new_sudoku):
        resolve_sudoku(new_sudoku)

    return new_sudoku


def suggest_to_resolve(sudoku: list[tuple[int, int, list[int]]]) -> list[tuple[int, int, list[int]]] | None:

    stop_chrono()
    print(
        "\033[F" * 3, f"\n⏱  Temps écoulé : {get_time()}" + 41*" " + "\n" + 41*" " + "\n", end="")

    if is_complete_resolved(sudoku):
        print("\033[F" * 2,
              f"\r⏱  Résolu en {get_time()}" + 41*" " + "\n" + 41*" ")
        return sudoku

    for cell in sudoku:

        if len(cell[2]) > 1:
            number_to_try = []
            for number in cell[2]:
                number_to_try.append(number)

            for number in number_to_try:
                try_sudoku_list = [cell[:] for cell in sudoku]
                index = try_sudoku_list.index(cell)
                try_sudoku_list[index][2] = [number]  # type: ignore

                if is_valid_sudoku_grid(try_sudoku_list):
                    result = suggest_to_resolve(try_sudoku_list)
                    if result:
                        return result
            return None

    return None


def get_string_from_list(sudoku_list):

    sudoku_str = ""
    line_index = 0

    for i in sudoku_list:
        if i[1] != line_index:
            sudoku_str += "\n"
            line_index = i[1]
        sudoku_str += str(i[2][0])

    return sudoku_str


def get_sudoku_list(string: str) -> list[tuple[int, int, list[int]]]:

    sudoku_list = []
    x = 0
    y = 0

    for character in string:
        if character == "\n":
            y += 1
            x = 0
            continue
        if character != ".":
            sudoku_list.append([x, y, [int(character)]])
        else:
            sudoku_list.append([x, y, [1, 2, 3, 4, 5, 6, 7, 8, 9]])
        x += 1

    return sudoku_list


def read_file(file_with_path: pathlib.Path) -> str:

    with open(file_with_path, "r") as objet_file:
        file_content = objet_file.read()

    return file_content


def write_file(file_with_path: pathlib.Path, sudoku_str: str) -> None:

    with open(file_with_path, "w") as objet_file:
        objet_file.write(sudoku_str)

    return None


def format_sudoku_with_boxes(sudoku_str):
    rows = sudoku_str.strip().split("\n")

    top_line = '   ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗'
    mid_block_line = '   ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣'
    mid_line = '   ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢'
    bottom_line = '   ╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝'
    row_separator = '   ║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║'

    table = [top_line]
    for i, row in enumerate(rows):
        table.append(row_separator.format(*row))
        if i in [2, 5]:
            table.append(mid_block_line)
        elif i != 8:
            table.append(mid_line)
    table.append(bottom_line)
    sudoku_in_boxes = '\n'.join(table)
    return sudoku_in_boxes


def start_chrono() -> None:
    global start_time
    start_time = time.time()


def stop_chrono() -> None:
    global end_time
    end_time = time.time()


def get_time() -> str:
    total_time = end_time - start_time
    minutes, seconds = divmod(int(total_time), 60)
    milliseconds = int((total_time - int(total_time)) * 1000)
    if minutes == 0:
        total_time_string = f"{seconds:02}s {milliseconds:03}ms"
        return total_time_string
    else:
        total_time_string = f"{
            minutes:02}m {seconds:02}s {milliseconds:03}"
        return total_time_string


#######################   Partie 2 :  Gestion d'erreur   ########################

def is_valid_arguments(is_number_of_argument_expected: bool) -> bool:

    if not is_number_of_argument_expected:
        print("Error : Vous devez saisir le nom du fichier .txt qui contient la grille de sudoku")
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


def is_valid_input_sudoku(file_content: str) -> bool:

    error = "Error, la grille de sudoku n'est pas au bon format.\nVous devez saisir 9 lignes composé de 9 chiffres ou . pour les cellule vides"

    if len(file_content) != 89:
        print(error)
        return False

    rows = file_content.split("\n")

    if len(rows) != 9:
        print(error)
        return False

    for row in rows:
        if len(row) != 9:
            print(error)
            return False
        for i in row:
            if i not in [".", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                print(error)
                print(f"'{i}' est un caractère non autorisé")
                return False

    return True


def is_valid_sudoku_grid(sudoku: list[tuple[int, int, list[int]]] | None) -> bool | None:

    if sudoku is None:
        return None

    for i in range(9):
        number_list = []
        for j in sudoku:
            if j[0] == i and len(j[2]) == 1:
                if j[2][0] in number_list:
                    return False
                number_list.append(j[2][0])

    for i in range(9):
        number_list = []
        for j in sudoku:
            if j[1] == i and len(j[2]) == 1:
                if j[2][0] in number_list:
                    return False
                number_list.append(j[2][0])

    for i in range(3):
        for j in range(3):
            number_list = []
            for k in sudoku:
                if (i*3) <= k[0] <= ((i*3) + 2) and (j*3) <= k[1] <= ((j*3) + 2) and len(k[2]) == 1:
                    if k[2][0] in number_list:
                        return False
                    number_list.append(k[2][0])

    return True


def is_complete_resolved(sudoku_list):

    for cell in sudoku_list:
        if len(cell[2]) > 1:
            return False

    return True


def is_impossible_to_solve(sudoku: list[tuple[int, int, list[int]]] | None) -> bool:

    if sudoku is None:
        print(
            "\033[31mLa grille proposé est impossible à résoudre\033[0m\n")
        return True

    for cell in sudoku:
        if len(cell[2]) == 0:
            print(
                "\033[31mLa grille proposé est impossible à résoudre\033[0m\n")
            return True

    return False


############################   Partie 3 :  Parsing   ############################

def get_arguments() -> list[str]:
    arguments = sys.argv[1:]
    return arguments


##########################   Partie 4 :  Résolution   ###########################

def get_resolved_sudoku():
    arguments = get_arguments()
    if not is_valid_arguments(len(arguments) == 1):
        return None
    file_name = arguments[0]

    if not is_valid_file_name(file_name.endswith(".txt")):
        return None
    file_path = ANNEX_PATH / file_name

    if not is_exists_file(file_path):
        return None
    file_content = read_file(file_path)

    if not is_valid_input_sudoku(file_content):
        return None

    format_file_content = format_sudoku_with_boxes(file_content)
    print(format_file_content)

    sudoku_list = get_sudoku_list(file_content)

    start_chrono()
    resolved_sudoku = resolve_sudoku(sudoku_list)

    if is_impossible_to_solve(resolved_sudoku):
        return

    if not is_complete_resolved(resolved_sudoku):
        print("Nous allons essayer chaque solution jusqu'a trouver la solution\nCela peut prendre un peu plus de temps")
        resolved_sudoku = suggest_to_resolve(resolved_sudoku)

    if is_impossible_to_solve(resolved_sudoku):
        return

    resolved_sudoku_str = get_string_from_list(resolved_sudoku)
    format_resolved_sudoku = format_sudoku_with_boxes(resolved_sudoku_str)
    print(format_resolved_sudoku)

    resolved_file_name = file_name.rstrip(".txt") + "_resolved.txt"
    resolved_file_path = ANNEX_PATH / resolved_file_name
    time_to_resolve = get_time()
    content_resolved_sudoku_file = f"'{file_name}'\n\n      ⏱ Grille résolut en " + time_to_resolve + "\n\n" + format_file_content + \
        "\n\n" + format_resolved_sudoku

    write_file(resolved_file_path, content_resolved_sudoku_file)


###########################   Partie 5 :  Affichage   ###########################

get_resolved_sudoku()
