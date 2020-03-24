#!/usr/bin/env python

import sys

origen=None
destino=None
hora=None
precio=None
maxpico=0
hora_list=[]
pico_list=[]
precios_pico=[]
precios=[]
promedio=0
promedio_pico=0
horas=[]
horas_pico=dict()
origene=sys.argv[1]
destinoe=sys.argv[2]

for entrada in sys.stdin:
    entrada.strip()
    origen,destino,hora,precio=entrada.split(',')

    if origen==origene and destino==destinoe:
        if hora in horas:
            horas_pico[hora]+=1
        else:
            horas.append(hora)
            horas_pico[hora]=1

        maxpico=max(horas_pico.values())


        hora_list = list(horas_pico.keys()) 
        pico_list = list(horas_pico.values()) 

        horapico=hora_list[pico_list.index(maxpico)]


        if hora==horapico:
            precios_pico.append(float(precio))
        else:
            precios.append(float(precio))
        

    


try:
    promedio_pico=sum(precios_pico)/len(precios_pico)
    #promedio=sum(precios)/len(precios)
    print horapico, promedio_pico#, promedio
except:
    pass