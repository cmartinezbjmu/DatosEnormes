#!/usr/bin/env python


from operator import itemgetter
from collections import Counter
import sys

palabra_actual = None
conteo_actual = 0
palabra = None
palabras_frecuentes = Counter()

# La entrada proviene de la salida del mapper
for linea in sys.stdin:
    # Elimina espacios en blanco
    linea = linea.strip()
    # asociasion de palabras y conteo
    palabra, conteo = linea.split('\t', 1)

    try:
        conteo = int(conteo)
    except ValueError:
        continue

    # Verifica si la palabra ya existe para incrementar la cuenta en 1
    if palabra_actual == palabra:
        conteo_actual += conteo
    else:
        if palabra_actual:
            # Escribe el resultado a STDOUT
            palabras_frecuentes[palabra_actual] = conteo_actual

        conteo_actual = conteo
        palabra_actual = palabra

# Escribe la ultima palabra a la salida STDOUT
if palabra_actual == palabra:    
    palabras_frecuentes[palabra_actual] = conteo_actual

for palabra, total in palabras_frecuentes.most_common(10):
    #print '%s\t%s' % (palabra, total)
    print '%s\t%s' % (palabra, total)