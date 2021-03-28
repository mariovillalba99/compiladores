#Definiciones

L_CORCHETE = 256
R_CORCHETE = 257
L_LLAVE = 258
R_LLAVE = 259
COMA = 260
DOS_PUNTOS = 261
LITERAL_CADENA = 262
LITERAL_NUM = 263
PR_TRUE = 264
PR_FALSE = 265
PR_NULL = 266
TAM_LEX = 50
SALTO_LINEA = "\n"

#Estructuras
lexemas = {
    "{": L_LLAVE,
    "[": L_CORCHETE,
    "]": R_CORCHETE,
    "}": R_LLAVE,
    ",": COMA,
    ":": DOS_PUNTOS,
    "string": LITERAL_CADENA,
    "number": LITERAL_NUM,
    "true": PR_TRUE,
    "false": PR_FALSE,
    "null": PR_NULL,
}
