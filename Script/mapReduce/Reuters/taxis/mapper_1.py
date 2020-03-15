#!/usr/bin/env python

import sys
import datetime


franja_hor = [0, 1]
tipo_vehi = ''
l = None
destino = None
for linea in sys.stdin:
    linea.strip()
    try:
        l = linea.split(',')
    except IndexError as e:
        pass
    
    if l:        
        if 'vendorid' not in l[0].lower():            
            if len(l) == 18:
                tipo_vehi = 'yellow'
                destino = l[8]
            if len(l) == 19:
                tipo_vehi = 'green'
                destino = l[6]
            if len(l) == 6:
                tipo_vehi = 'fhv'
                destino = l[4]
            if len(l) == 7:
                tipo_vehi = 'hfhv'
                destino = l[5]
            # capturar hora
            fecha_hora = l[1].split()
            fecha = fecha_hora[0].split('-')
            hora = fecha_hora[1].split(':')[0]
            hora = int(hora)

            # comparar hora dataset con franja horaria
            if (franja_hor[0] <= hora) and (hora <= franja_hor[1]):                
                dia_semana = datetime.datetime(
                    int(fecha[0]), int(fecha[1]), int(fecha[2])).weekday()
                # entrega salida al reducer
                #print('{},{},{}'.format(tipo_vehi, dia_semana, destino))
                print '%s,%s,%s' % (tipo_vehi, dia_semana, destino)
