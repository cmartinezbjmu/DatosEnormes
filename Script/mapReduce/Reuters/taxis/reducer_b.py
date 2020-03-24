#!/usr/bin/env python

import sys

origen=None
destino=None
distancia=0
trayectos=dict()
distancias=dict()
proporcion_viajes=[]
diferencia_distancias=[]
distancia_grande=[]
difgrande=0
llave=''
sindif=0


for entrada in sys.stdin:
    entrada.strip()
    origen,destino,distancia=entrada.split(',')    
    try:
        distancia=float(distancia)
    except:
        distancia=0
    llave= origen+','+destino
    if llave in trayectos.keys():
        trayectos[llave]+=1
    else:
        trayectos[llave]=1
    if llave in distancias.keys():
        distancias[llave].append(distancia)
    else:
        distancias[llave]=[distancia]

for i in trayectos.values():
    print float(i/sum(trayectos.values()) , i/sum(trayectos.values()
    proporcion_viajes.append(i/sum(trayectos.values()))
    
proporcion_viajes.sort(reverse = True) 


for llave in distancias.keys():
    diferencia_distancias.append(max(distancias[llave])-min(distancias[llave]))

for i in diferencia_distancias:
    if i>2: distancia_grande.append(i)
    
difgrande=len(distancia_grande)
sindif=len(diferencia_distancias)-len(distancia_grande)

# print(difgrande,sindif,proporcion_viajes)
print difgrande,sindif,proporcion_viajes
