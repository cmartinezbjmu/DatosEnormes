#!/usr/bin/env python

import sys
import operator
from collections import Counter

tipo_veh = ''
precio = ''
precio_min_yellow = 200
precio_max_yellow = 0
precio_acum_yellow = 0
precio_prom_yellow = 0
cantidad_yellow = 0
precio_min_green = 200
precio_max_green = 0
precio_acum_green = 0
precio_prom_green = 0
cantidad_green = 0

resultado = dict()

for entrada in sys.stdin:
    entrada.strip()
    tipo_veh, precio = entrada.split(',')
    precio = precio.replace('\n', '')

    if (float(precio) > 0):
        if (tipo_veh == 'yellow'):
            if float(precio) < precio_min_yellow:
                precio_min_yellow = float(precio)

            if float(precio) > precio_max_yellow:
                precio_max_yellow = float(precio)
        
            cantidad_yellow = cantidad_yellow + 1
            precio_acum_yellow = precio_acum_yellow + float(precio)

        if (tipo_veh == 'green'):
            if float(precio) < precio_min_green:
                precio_min_green = float(precio)

            if float(precio) > precio_max_green:
                precio_max_green = float(precio)
        
            cantidad_green = cantidad_green + 1
            precio_acum_green = precio_acum_green + float(precio)

if cantidad_yellow > 1:
    precio_prom_yellow = precio_acum_yellow / float(cantidad_yellow)
    resultado['yellow'] = [precio_max_yellow, precio_min_yellow, precio_prom_yellow]

if cantidad_green > 1:
    precio_prom_green = precio_acum_green / float(cantidad_green)
    resultado['green'] = [precio_max_green, precio_min_green, precio_prom_green]

print '%s' % (resultado)
