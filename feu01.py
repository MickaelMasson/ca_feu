"""Évaluer une expression"""
"""Créez un programme qui reçoit une expression arithmétique dans une chaîne de caractères et en retourne le résultat après l’avoir calculé.

Vous devez gérer les 5 opérateurs suivants : “+” pour l’addition, “-” pour la soustraction, “*” la multiplication, “/” la division et “%” le modulo.

Exemple d’utilisation :


$> ruby exo.rb “4 + 21 * (1 - 2 / 2) + 38”
42


Vous pouvez partir du principe que la chaîne de caractères donnée en argument sera valide."""


######################   Partie 1 :  Fonctions utilisées   ######################


import sys
TOKENS = [
    ("LEFT_PARENTHESIS", "("),
    ("RIGHT_PARENTHESIS", ")"),
    ("TIMES", "*"),
    ("DIVIDE", "/"),
    ("MODULO", "%"),
    ("PLUS", "+"),
    ("MINUS", "-"),
    ("NUMBER", "0123456789."),
    ("SPACE", " ")
]


def lexer(string: str) -> list:

    tokens = []
    i = 0

    while i < len(string):
        character = string[i]
        for token_type, valid_chars in TOKENS:
            if character in valid_chars:
                if token_type == "NUMBER":
                    start = i
                    while i < len(string) and string[i] in valid_chars:
                        i += 1
                    number_str = string[start:i]
                    number = float(number_str)
                    tokens.append(("NUMBER", number))
                    break
                elif token_type == "SPACE":
                    i += 1
                    break
                else:
                    tokens.append((token_type, character))
                    i += 1
                    break
    return tokens


def get_ast(tokens: list) -> list:

    start_parenthesis = -1
    for i in range(len(tokens)):
        if tokens[i][0] == "LEFT_PARENTHESIS":
            start_parenthesis = i
        elif tokens[i][0] == "RIGHT_PARENTHESIS" and start_parenthesis != -1:
            sub_expression = get_ast(tokens[start_parenthesis + 1:i])
            tokens = tokens[:start_parenthesis] + [(
                "NUMBER", sub_expression)] + tokens[i + 1:]
            return get_ast(tokens)

    i = 0
    while i < len(tokens):
        if tokens[i][0] in ["TIMES", "DIVIDE", "MODULO"]:
            if tokens[i - 1][0] == "NUMBER":
                left = tokens[i - 1][1]
            else:
                left = tokens[i - 1]
            if tokens[i + 1][0] == "NUMBER":
                right = tokens[i + 1][1]
            else:
                right = tokens[i + 1]
            sub_ast = [tokens[i][0], left, right]
            tokens = tokens[:i-1] + [("NUMBER", sub_ast)] + tokens[i+2:]
            i = 0
            continue
        i += 1

    i = 0
    while i < len(tokens):
        if tokens[i][0] in ["PLUS", "MINUS"]:
            if i == 0:
                if tokens[i][0] == "MINUS" and i + 1 < len(tokens):
                    if tokens[i + 1][0] == "NUMBER":
                        right = tokens[i + 1][1]
                    else:
                        right = tokens[i + 1]
                    sub_ast = - right
                    tokens = [("NUMBER", sub_ast)] + tokens[i+2:]
                    i = 0
                    continue
            if tokens[i - 1][0] == "NUMBER":
                left = tokens[i - 1][1]
            else:
                tokens[i - 1]
            if tokens[i + 1][0] == "NUMBER":
                right = tokens[i + 1][1]
            else:
                tokens[i + 1]
            sub_ast = [tokens[i][0], left, right]
            tokens = tokens[:i-1] + [("NUMBER", sub_ast)] + tokens[i+2:]
            i = 0
            continue
        i += 1

    return tokens[0][1]


def evaluate(ast: list) -> float:  # type: ignore

    if isinstance(ast, float):
        return ast

    operator = ast[0]
    left = evaluate(ast[1])
    right = evaluate(ast[2])

    if operator == "PLUS":
        return left + right
    elif operator == "MINUS":
        return left - right
    elif operator == "TIMES":
        return left * right
    elif operator == "DIVIDE":
        return left / right
    elif operator == "MODULO":
        return left % right


#######################   Partie 2 :  Gestion d'erreur   ########################

def is_valid_arguments(is_number_of_argument_expected: bool) -> bool:

    if not is_number_of_argument_expected:
        print("Error : le nombre d'arguments n'est pas valide")
        return False

    return True


def are_valid_numbers(expression: str) -> bool:

    current_number = ""
    in_number = False
    error = "Error : l'expression contient des nombres avec plusieurs décimales"

    for char in expression:
        if char.isdigit() or char == '.':
            current_number += char
            in_number = True
        elif in_number:
            # Fin d'un nombre, on le vérifie
            if current_number.count('.') > 1:
                print(error)
                return False
            current_number = ""
            in_number = False

    # Vérifier le dernier nombre si l'expression se termine par un nombre
    if in_number and current_number.count('.') > 1:
        print(error)
        return False

    return True


def are_valid_characters(string: str) -> bool:
    all_valid_characters = ""
    for token_type, valid_characters in TOKENS:
        all_valid_characters += valid_characters

    for character in string:
        if character not in all_valid_characters:
            print(f"Error : Caractère non autorisé dans une expression mathématique : '{
                  character}'")
            return False

    return True


def is_valid_min_tokens(min_tokens_expected: bool) -> bool:

    if not min_tokens_expected:
        print("Error, l'expression mathématique doit contenir au moins 3 éléménts")
        return False

    return True


def is_valid_parenthesis(tokens: list[tuple[str, str]]) -> bool:

    parenthesis_count = 0

    for token in tokens:
        if token[0] == "LEFT_PARENTHESIS":
            parenthesis_count += 1
        elif token[0] == "RIGHT_PARENTHESIS":
            parenthesis_count -= 1
        if parenthesis_count < 0:
            print("Error : Probleme d'ouverture de parenthese")
            return False

    if parenthesis_count != 0:
        print("Error : Probleme de fermeture de parenthese")
        return False

    return True


def is_valid_syntax(tokens: list[tuple[str, str]]) -> bool:

    operators = ["TIMES", "DIVIDE", "MODULO", "PLUS", "MINUS"]
    first_token = tokens[0][0]
    last_token = tokens[-1][0]

    if first_token in ["TIMES", "DIVIDE", "MODULO", "PLUS", "RIGHT_PARENTHESIS"]:
        print("Error : le premier élémént de l'expression mathématique doit etre un nombre ou une parenthèse ouvrante")
        return False

    if last_token != "NUMBER" and last_token != "RIGHT_PARENTHESIS":
        print("Error : le dernier élémént de l'expression mathématique doit etre un nombre ou une parenthèse fermante")
        return False

    for i in range(len(tokens) - 1):
        current_token = tokens[i][0]
        next_token = tokens[i + 1][0]

        if current_token == "LEFT_PARENTHESIS" and next_token == "RIGHT_PARENTHESIS":
            print("Error : Impossible d'avoir une parenthèse vide")
            return False

        if current_token == "LEFT_PARENTHESIS" and next_token in ["MODULO", "DIVIDE", "TIMES"]:
            print(
                "Error : Après une parenthèse ouvrante '(', les opérateurs '*', '/', et '%' ne sont pas autorisés")
            return False

        if current_token == "RIGHT_PARENTHESIS" and next_token in ["NUMBER", "LEFT_PARENTHESIS"]:
            print("Error : Après une parenthèse fermante ')', un opérateur est attendu")
            return False

        if current_token in operators and next_token not in ["NUMBER", "LEFT_PARENTHESIS"]:
            print(f"Error : Après l'opérateur '{
                  tokens[i][1]}', seul un nombre ou une parenthèse ouvrante sont attendus")
            return False

        if current_token == "NUMBER" and next_token in ["NUMBER", "LEFT_PARENTHESIS"]:
            print(
                "Error : Après un nombre, seul un opérateur ou une parenthèse fermante est attendu")
            return False

    return True


############################   Partie 3 :  Parsing   ############################

def get_arguments() -> list[str]:

    arguments = sys.argv[1:]

    return arguments


##########################   Partie 4 :  Résolution   ###########################

def get_result_of_expresion() -> float | None:

    arguments = get_arguments()

    if not is_valid_arguments(len(arguments) == 1):
        return None

    expression = arguments[0]

    if not are_valid_numbers(expression):
        return None

    if not are_valid_characters(expression):
        return None

    tokens = lexer(expression)

    if not is_valid_min_tokens(len(tokens) >= 3):
        return None

    if not is_valid_parenthesis(tokens):
        return None

    if not is_valid_syntax(tokens):
        return None

    ast = get_ast(tokens)
    result = evaluate(ast)

    return result


###########################   Partie 5 :  Affichage   ###########################

def display_result_of_expresion() -> None:

    results = get_result_of_expresion()

    if results == None:
        return

    if results.is_integer():
        results = int(results)

    arguments = get_arguments()
    expression = arguments[0]

    print(f"{expression} = {results}")

    return None


display_result_of_expresion()
