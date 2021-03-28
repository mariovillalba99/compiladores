# Analizador Lexico	

# Descripcion:
# Implementación un analizador léxico para el lenguaje Json simplificado

import sys
from data import *

# Archivo de salida
file_output = open("output.txt", "w")


def next_lexema(file_input):
    """Lee el archivo y recorre caracter por caracter las líneas del mismo

    Args:
        file_input (file): Archivo de entrada
    """
    token = {}
    line_number = 0
    try:
        for line in file_input.readlines():
            line_number += 1
            character_position = 0
            character_current = 0
            while character_current < len(line):
                if line[character_current] == "{":
                    validate_print(get_token(line[character_current]))
                elif line[character_current] == "[":
                    validate_print(get_token(line[character_current]))
                elif line[character_current] == "]":
                    validate_print(get_token(line[character_current]))
                elif line[character_current] == "}":
                    validate_print(get_token(line[character_current]))
                elif line[character_current] == ",":
                    validate_print(get_token(line[character_current]))
                elif line[character_current] == ":":
                    validate_print(get_token(line[character_current]))
                elif line[character_current] == '"':
                    character_position = character_current + 1
                    for i in range(character_position, len(line)):
                        character_current = i
                        if line[i] == '"':
                            validate_print(get_token("string"))
                            break
                        elif line[i] == "," or line[i] == SALTO_LINEA or i == len(line):
                            print_error(
                                " Error lexico, se esperaba fin de cadena", line_number
                            )
                            character_current = i
                            if line[character_current] == SALTO_LINEA:
                                write_file("\n")
                            break
                elif (
                    line[character_current] == "t"
                    or line[character_current] == "f"
                    or line[character_current] == "n"
                ):
                    data = get_text_bool(line, character_current, len(line))
                    if data["text"] == "true":
                        validate_print(get_token("true"))
                        character_current = data["position"] - 1
                    elif data["text"] == "false":
                        validate_print(get_token("false"))
                        character_current = data["position"] - 1
                    elif data["text"] == "null":
                        validate_print(get_token("null"))
                        character_current = data["position"] - 1
                    else:
                        write_file(" Error lexico")
                        character_current = data["position"] - 1
                elif (
                    line[character_current].isalpha()
                    or line[character_current].isdigit()
                    and line[character_current] != "t"
                    and line[character_current] != "f"
                    and line[character_current] != "n"
                ):
                    data = verify_number(line, character_current, len(line))
                    if data is None:
                        position_error = get_position_error(
                            line, character_current, len(line)
                        )
                        print_error(" Error lexico, caracter no esperado", line_number)
                        character_current += position_error
                        if line[character_current] == SALTO_LINEA:
                            write_file("\n")
                    else:
                        validate_print(get_token("number"))
                        character_current = data["position"] - 1
                elif line[character_current] == SALTO_LINEA:
                    file_output.write(SALTO_LINEA)
                elif line[character_current] == " ":
                    file_output.write(" ")
                character_current += 1
    except Exception as error:
        print(error)


def get_token(lexema):
    """Obtiene el componente léxico de un lexema

    Args:
        lexema (str): Lexema encontrado en la linea actual del archivo

    Returns:
        dictionary: Diccionario con el componente léxico y el lexema encontrado
    """
    return {"compLex": lexemas.get(lexema), "lexema": lexema}


def verify_number(line, initial_position, final_position):
    """Verificación si el número cumple con la expresión regular definida

    Args:
        line (str): Línea actual del archivo
        initial_position (integer): Posición inicial de la subcadena
        final_position (integer): Posición de fin de línea

    Returns:
        dictionary: Diccionario con los datos y la posición del texto encontrado
        None: Si no cumple con la expresión regular definida
    """
    import re

    regular_exp = "[0-9]+(\.[0-9]+)?((e|E)(\+|\-)?[0-9]+)?"
    data = {}
    data["position"] = initial_position
    data["text"] = ""
    for i in range(initial_position, final_position):
        if line[i] == "," or line[i] == SALTO_LINEA:
            break
        else:
            data["position"] += 1
            data["text"] += line[i]

    match = re.search(regular_exp, data["text"])
    if match is not None:
        start_match = match.start()
        end_match = match.end()

        if data["text"][start_match:end_match].strip() == data["text"].strip():
            return data
        else:
            return None
    else:
        return None


def get_text_bool(line, initial_position, final_position):
    """Obtiene el texto de la palabras reservadas true, false o null

    Args:
        line (str): Línea actual del archivo
        initial_position (integer): Posición inicial de la subcadena
        final_position (integer): Posición de fin de la línea

    Returns:
        dictionary: Diccionario con los datos y la posición del texto encontrado
    """
    data = {}
    data["position"] = initial_position
    data["text"] = ""
    for i in range(initial_position, final_position):
        if line[i] == "," or line[i] == SALTO_LINEA:
            return data
        else:
            data["position"] += 1
            data["text"] += line[i]
    return data


def get_position_error(line, initial_position, final_position):
    """Obtiene la posición de finalización de un texto no esperado en el Json

    Args:
        line (str): Línea actual del archivo
        initial_position (integer): Posición inicial de un caracter no esperado
        final_position (integer): Posición de fin de la línea

    Returns:
        integer: Posición de fin del texto no esperado
    """
    position = 0
    for i in range(initial_position, final_position):
        if line[i] == "," or line[i] == SALTO_LINEA:
            return position
        position += 1


def print_error(text, line_number):
    """Imprime en el archivo el mensaje y linea del error

    Args:
        text (str): Texto del error
        line_number (integer): Número de línea del error
    """
    write_file(text + " en la linea " + str(line_number))


def validate_print(token):
    """Valida y obtiene el texto a imprimir de acuerdo al componente léxico del lexema

    Args:
        token (dictionary): Diccionario que contiene el compLex y lexema
    """
    compLexicos = {
        L_LLAVE: " L_LLAVE",
        L_CORCHETE: " L_CORCHETE",
        R_CORCHETE: " R_CORCHETE",
        R_LLAVE: " R_LLAVE",
        COMA: " COMA",
        DOS_PUNTOS: " DOS_PUNTOS",
        LITERAL_CADENA: " STRING",
        LITERAL_NUM: " NUMBER",
        PR_TRUE: " PR_TRUE",
        PR_FALSE: " PR_FALSE",
        PR_NULL: " PR_NULL",
    }
    write_file(compLexicos.get(token["compLex"]))


def write_file(text):
    """Escribe un texto en el archivo

    Args:
        text (str): String que se imprime en el archivo
    """
    file_output.write(text)


def main():
    try:
        if len(sys.argv) > 1:
            # Archivo de entrada
            file_input = open(sys.argv[1])
            next_lexema(file_input)
            file_input.close()
        else:
            print("Debe enviar el path del archivo por parametro.")
            sys.exit(0)
        file_output.close()
    except FileNotFoundError:
        print("No se encontro el archivo.")


if __name__ == "__main__":
    main()