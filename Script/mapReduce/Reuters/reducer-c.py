#!/usr/bin/env python


from operator import itemgetter
from collections import Counter
import sys


total_noticias = 0
total_palabras = 0

# La entrada proviene de la salida del mapper
for linea in sys.stdin:
    # Elimina espacios en blanco
    linea = linea.strip()
    # asociasion de palabras y conteo
    n, conteo = linea.split('\t', 1)   

    try:
        conteo = int(conteo)        
    except ValueError:
        continue
    total_noticias += 1    
    total_palabras += conteo    

print 'Promedio de palabras en las noticias es: {:0.2f}'.format((total_palabras/float(total_noticias)))
#print('Promedio de palabras en las noticias es: {}'.format(total_palabras/float(total_noticias)))
