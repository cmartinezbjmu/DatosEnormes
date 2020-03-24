#!/usr/bin/env python

import sys

# tipo_vehi=''
sitio=''
mes=''


N_sitios=int(sys.argv[1])

sitios=dict()
meses=dict()

for entrada in sys.stdin:
    entrada.strip()
    sitio,mes = entrada.split(',')
    mes=mes.replace('\n','').replace('\t','')
    if sitio in sitios.keys():
        if mes in meses.keys():                       
            sitios[sitio][mes]+=1
        else:
            sitios[sitio][mes]=1             
    else:
        meses=dict()
        meses[mes]=1
        sitios[sitio]=meses


max_n=[]
for i in sitios.keys():
    max_n.append([i,max(sitios[i].values())])
ordenado=sorted(max_n, key=lambda x: x[1],reverse = True)       

ordenado_n= ordenado[:N_sitios]

max_sitios=[]
for item in ordenado_n:
    max_sitios.append(item[0])


for i in max_sitios:
    print '%s,%s' % (i,sitios[i]) 



