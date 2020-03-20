#!/usr/bin/env python

import sys
import operator
from collections import Counter

tipo_veh = ''
precio = ''

dic_principal = dict()
conteo_destinos = dict()

for entrada in sys.stdin:
    entrada.strip()
    tipo_veh, precio = entrada.split(',')
    precio = precio.replace('\n', '')

    

max_ubicacion = None
keys = list(dic_principal.keys())
for key, values in dic_principal.items():
    max_ubicacion = max(values, key=values.get)
    print '%s\t%s\t%s' % (key, max_ubicacion, values[max_ubicacion])
