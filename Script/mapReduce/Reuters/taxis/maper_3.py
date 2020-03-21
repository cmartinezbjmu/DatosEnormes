#!/usr/bin/env python

import sys
import datetime
from datetime import datetime
#from geopy.geocoders import Nominatim

dia = 4
mes = '02'
tipo_vehi = ''
l = None
sitio = None
for linea in sys.stdin:
    linea.strip()
    if '"' in linea: linea = linea.replace('"', '')
    try:
        l = linea.split(',')        
    except IndexError as e:
        pass

    if l:
        # sitio de recogida
        if (l[0].lower != 'vendorid') or (l[0].lower != 'pickup_datetime'):
            if (len(l) == 18): # yellow year 2019
                tipo_vehi = 'yellow'
                sitio = l[5]
                fecha = l[1]
                dia_semana=datetime.strptime(fecha.split()[0], '%Y-%m-%d').weekday()
                mes=datetime.strptime(fecha.split()[0], '%Y-%m-%d').month
                franja=fecha.split()[1].split(':')[0]


            if (len(l) == 17): # Yellow 2017
                tipo_vehi = 'yellow'
                sitio = l[5]
                fecha = l[1]
                dia_semana=datetime.strptime(fecha.split()[0], '%Y-%m-%d').weekday()
                mes=datetime.strptime(fecha.split()[0], '%Y-%m-%d').month
                franja=fecha.split()[1].split(':')[0]


            if len(l) == 20: # green year 2019
                tipo_vehi = 'green'
                sitio=l[7]
                fecha = l[1]
                dia_semana=datetime.strptime(fecha.split()[0], '%Y-%m-%d').weekday()
                mes=datetime.strptime(fecha.split()[0], '%Y-%m-%d').month
                franja=fecha.split()[1].split(':')[0]

                
            if  len(l) == 19 or len(l) == 21:
                tipo_vehi = 'green'
                sitio=l[7]  #Cambiar
                fecha = l[1] #Cambiar
                dia_semana=datetime.strptime(fecha.split()[0], '%Y-%m-%d').weekday()
                mes=datetime.strptime(fecha.split()[0], '%Y-%m-%d').month
                franja=fecha.split()[1].split(':')[0]

                


            try:
                fecha_hora = l[1].split()
                fecha = fecha_hora[0].split('-')
                if ((fecha[0] == '2016') or (fecha[0] == '2015')) and (len(l) == 19):
                    tipo_vehi = 'yellow'
                    fecha = l[1]
                    dia_semana=datetime.strptime(fecha.split()[0], '%Y-%m-%d').weekday()
                    mes=datetime.strptime(fecha.split()[0], '%Y-%m-%d').month
                    franja=fecha.split()[1].split(':')[0]
                    longitud=l[5]
                    latitud=l[6]
                    sitio=latitud + longitud

                
                if (fecha[0] == '2016') and (len(l) == 21):
                    tipo_vehi = 'green'
                    fecha = l[1]
                    dia_semana=datetime.strptime(fecha.split()[0], '%Y-%m-%d').weekday()
                    mes=datetime.strptime(fecha.split()[0], '%Y-%m-%d').month
                    franja=fecha.split()[1].split(':')[0]
                    longitud=l[5]
                    latitud=l[6]
                    sitio=latitud + longitud
                                    
                if (fecha[0] == '2015') and (len(l) == 21):
                    tipo_vehi = 'green'
                    fecha = l[1]
                    dia_semana=datetime.strptime(fecha.split()[0], '%Y-%m-%d').weekday()
                    mes=datetime.strptime(fecha.split()[0], '%Y-%m-%d').month
                    franja=fecha.split()[1].split(':')[0]
                    longitud=l[5]
                    latitud=l[6]
                    sitio=latitud + longitud

                    
                if ((fecha[0] == '2014') or (fecha[0] == '2013') or (fecha[0] == '2012') or (fecha[0] == '2011')  or (fecha[0] == '2010')  or (fecha[0] == '2009') ) and (len(l) == 18):
                    tipo_vehi = 'yellow'
                    fecha = l[1]
                    dia_semana=datetime.strptime(fecha.split()[0], '%Y-%m-%d').weekday()
                    mes=datetime.strptime(fecha.split()[0], '%Y-%m-%d').month
                    franja=fecha.split()[1].split(':')[0]
                    longitud=l[5]
                    latitud=l[6]
                    sitio=latitud + longitud

                    
                if ((fecha[0] == '2014') or (fecha[0] == '2013')) and (len(l) == 22):
                    tipo_vehi = 'green'
                    fecha = l[1]
                    dia_semana=datetime.strptime(fecha.split()[0], '%Y-%m-%d').weekday()
                    mes=datetime.strptime(fecha.split()[0], '%Y-%m-%d').month
                    franja=fecha.split()[1].split(':')[0]
                    longitud=l[5]
                    latitud=l[6]
                    sitio=latitud + longitud

                                    
            except IndexError as e:
                pass
            
            
    print(tipo_vehi,sitio,dia_semana,mes,1)