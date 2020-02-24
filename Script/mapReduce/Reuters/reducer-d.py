#!/usr/bin/env python


from operator import itemgetter
from collections import Counter
import sys

tema_actual = None
conteo_actual = 0
tema = None
palabras_frecuentes = Counter()

# La entrada proviene de la salida del mapper
for linea in sys.stdin:
    # Elimina espacios en blanco
    linea = linea.strip()
    # asociasion de palabras y conteo
    tema, conteo = linea.split('\t')

    try:
        conteo = int(conteo)
    except ValueError:
        continue

    # Verifica si la palabra ya existe para incrementar la cuenta en 1
    if tema_actual == tema:
        conteo_actual += conteo
    else:
        if tema_actual:
            # Escribe el resultado a STDOUT
            palabras_frecuentes[tema_actual] = conteo_actual

        conteo_actual = conteo
        tema_actual = tema

# Escribe la ultima palabra a la salida STDOUT
if tema_actual == tema:    
    palabras_frecuentes[tema_actual] = conteo_actual

for tema, total in palabras_frecuentes.items():
    print 'Existen %s noticias del tema %s' % (total, tema)