#!/usr/bin/env python

import sys
import datetime
from geopy.geocoders import Nominatim

franja_hor = [0, 3]
tipo_vehi = ''
l = None
destino = None
for linea in sys.stdin:
    linea.strip()
    if '"' in linea: linea = linea.replace('"', '')
    try:
        l = linea.split(',')        
    except IndexError as e:
        pass

    if l:
        #print(len(l))
        #print(l)
        if (l[0].lower != 'vendorid') or (l[0].lower != 'pickup_datetime'):
            if (len(l) == 18) or (len(l) == 17):
                tipo_vehi = 'yellow'
                destino = l[8]
            if len(l) == 20 or len(l) == 19 or len(l) == 21:
                tipo_vehi = 'green'
                destino = l[6]
                
            if (len(l) == 6) or (len(l) == 5):
                tipo_vehi = 'fhv'
                destino = l[4]
            if len(l) == 3:
                tipo_vehi = 'fhv'
                destino = '265'
            if len(l) == 7:                     
                tipo_vehi = 'hfhv'
                destino = l[5]
                #print(destino)

            try:
                tipo = 0
                # capturar hora
                fecha_hora = l[1].split()
                fecha = fecha_hora[0].split('-')
                if ((fecha[0] == '2016') or (fecha[0] == '2015')) and (len(l) == 19):
                    tipo = 1
                    tipo_vehi = 'yellow'
                    lat = 10           
                
                if (fecha[0] == '2016') and (len(l) == 21):
                    tipo = 1
                    tipo_vehi = 'green'
                    lat = 8
                
                if (fecha[0] == '2015') and (len(l) == 23):
                    tipo = 1
                    tipo_vehi = 'green'
                    lat = 8

                if ((fecha[0] == '2014') or (fecha[0] == '2013') or (fecha[0] == '2012') or (fecha[0] == '2011')  or (fecha[0] == '2010')  or (fecha[0] == '2009') ) and (len(l) == 18):
                    tipo = 1
                    tipo_vehi = 'yellow'
                    lat = 10

                if ((fecha[0] == '2014') or (fecha[0] == '2013')) and (len(l) == 22):
                    tipo = 1
                    tipo_vehi = 'green'
                    lat = 8

                if (fecha[0] != '2019') and (tipo_vehi == 'hfhv'): tipo_vehi = 'fhv'
                if tipo == 1:      
                    lat, lon = l[lat], l[lat-1]
                    #print lat, lon
                    geolocator = Nominatim(user_agent="bigdata20", timeout=15)
                    ubicacion = geolocator.reverse('%s, %s' % (lat, lon))
                    ubicacion = str(ubicacion).split(',')[2].strip().lower()
                    #print ubicacion
                    f = open("taxi_zone_lookup.csv")
                    destino = None
                    for ciudad in f.readlines():
                        if (ubicacion in ciudad.lower()):
                            destino = ciudad.split(';')[0]
                            break
                    if not destino:
                        destino = '265'
                            
                hora = fecha_hora[1].split(':')[0]
                hora = int(hora)
                # comparar hora dataset con franja horaria
                if (franja_hor[0] <= hora) and (hora <= franja_hor[1]):
                    dia_semana = datetime.datetime(
                        int(fecha[0]), int(fecha[1]), int(fecha[2])).weekday()
                    # entrega salida al reducer
                    #print('{},{},{}'.format(tipo_vehi, dia_semana, destino))                    
                    if destino != '\n': print '%s,%s,%s' % (tipo_vehi, dia_semana, destino)


            except IndexError as e:
                pass
