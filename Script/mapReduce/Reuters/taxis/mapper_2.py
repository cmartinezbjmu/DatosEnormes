#!/usr/bin/env python

import sys
import datetime

dia = int(sys.argv[1])
mes = sys.argv[2]
tipo_vehi = ''
precio = ''
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
        #print(l)
        if (l[0].lower != 'vendorid') or (l[0].lower != 'pickup_datetime'):
            if (len(l) == 18): # yellow year 2019
                tipo_vehi = 'yellow'
                precio = l[len(l)-2]
            if (len(l) == 17):
                tipo_vehi = 'yellow'
                precio = l[len(l)-1]
            if len(l) == 20: # green year 2019
                tipo_vehi = 'green'
                precio = l[len(l)-4]
            if  len(l) == 19 or len(l) == 21:
                tipo_vehi = 'green'
                precio = l[len(l)-3]

            try:
                # capturar hora
                fecha_hora = l[1].split()
                fecha = fecha_hora[0].split('-')
                if ((fecha[0] == '2016') or (fecha[0] == '2015')) and (len(l) == 19):
                    tipo_vehi = 'yellow'
                    precio = l[len(l)-3]
                
                if (fecha[0] == '2016') and (len(l) == 21):
                    tipo_vehi = 'green'
                    precio = l[len(l)-3]
                
                if (fecha[0] == '2015') and ((len(l) == 21) or (len(l) == 23)):
                    tipo_vehi = 'green'
                    precio = l[len(l)-3]

                if ((fecha[0] == '2014') or (fecha[0] == '2013') or (fecha[0] == '2012') or (fecha[0] == '2011')  or (fecha[0] == '2010')  or (fecha[0] == '2009') ) and (len(l) == 18):
                    tipo_vehi = 'yellow'
                    precio = l[len(l)-1]

                if ((fecha[0] == '2014') or (fecha[0] == '2013')) and (len(l) == 22):                    
                    tipo_vehi = 'green'
                    precio = l[len(l)-5]
                
                
                if (fecha[1] == mes):                    
                    dia_semana = datetime.datetime(
                        int(fecha[0]), int(fecha[1]), int(fecha[2])).weekday()                    
                    if (dia_semana == dia) and tipo_vehi:                        
                    # entrega salida al reducer
                        print '%s,%s' % (tipo_vehi, precio.replace('\n', ''))


            except IndexError as e:
                pass
