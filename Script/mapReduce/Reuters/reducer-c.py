#!/usr/bin/env python


from operator import itemgetter
from collections import Counter
import sys


total_noticias = 0
total_palabras = 0
longitud = 0
palabra = ""
max_palabras = 0

# La entrada proviene de la salida del mapper
for linea in sys.stdin:
    # Elimina espacios en blanco
    linea = linea.strip()
    # asociacion de palabras y conteo
    conteo, palabra_larga, titulo, fecha, pais = linea.split('\t')
    
    try:
        conteo = int(conteo)

    except ValueError:
        continue
    total_noticias += 1    
    total_palabras += conteo
    if len(palabra) < len(palabra_larga):
        palabra = palabra_larga
        titulo_larga = titulo
        fecha_larga = fecha
    
    if max_palabras < conteo:
        max_palabras = conteo
        titulo_max_palabras = titulo
        pais_noticia_max = pais
    

#print 'Promedio de palabras en las noticias es: {:0.2f}'.format((total_palabras/float(total_noticias)))
#print 'Promedio de palabras en las noticias es: {:0.2f}'.format((total_palabras/float(total_noticias)))
#print 'Promedio de palabras en las noticias es: {:0.2f}'.format((total_palabras/float(total_noticias)))
print('Promedio de palabras en las noticias es: {}'.format(total_palabras/total_noticias))
print('La palabra mas larga es: {} y el titulo de la noticia es: {} publicada en la fecha: {}'.format(palabra, titulo_larga, fecha_larga))
print('La noticia que tiene mas palabras es: {} con {} palabras, publicada en {}'.format(titulo_max_palabras, conteo, pais))