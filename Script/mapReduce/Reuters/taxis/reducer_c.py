#!/usr/bin/env python

import sys

distancia=None
proporcion=[]
cerca=0
lejos=0
total=0

for entrada in sys.stdin:
    entrada.strip()
    distancia=entrada.split(',')   
    if int(distancia)<=3 :
        cerca+=1
    else:
        lejos+=1

total=cerca+lejos
proporcion=[float(cerca)/total, float(lejos)/total]

print proporcion[0],proporcion[1]