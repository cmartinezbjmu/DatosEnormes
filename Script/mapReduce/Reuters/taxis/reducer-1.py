#!/usr/bin/env python

import sys
import operator
from collections import Counter

tipo_veh = ''
destino = ''
dia_semana = ''

dic_principal = dict()
conteo_destinos = dict()

for entrada in sys.stdin:
    entrada.strip()
    tipo_veh, dia_semana, destino = entrada.split(',')
    destino = destino.split('\n')[0]

    llave_principal = '{}_{}'.format(tipo_veh, dia_semana)
    llave_destino = destino
    if llave_principal in dic_principal:
        # 'si existe llave principal'
        if llave_destino in conteo_destinos:
            # 'si existe el destino'
            contador = conteo_destinos[llave_destino]
            contador += 1
            conteo_destinos[llave_destino] = contador
        else:
            conteo_destinos[llave_destino] = 1

    else:
        conteo_destinos = dict()
        conteo_destinos[llave_destino] = 1
        dic_principal[llave_principal] = conteo_destinos

    def get_key(val):
        for key, value in dic_principal.items():
            if val == value:
                return key

        return "key doesn't exist"

max_ubicacion = None
keys = list(dic_principal.keys())
for key, values in dic_principal.items():
    max_ubicacion = max(values, key=values.get)
    print '%s\t%s\t%s' % (key, max_ubicacion, values[max_ubicacion])


