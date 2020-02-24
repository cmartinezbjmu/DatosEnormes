#!/usr/bin/env python

import sys
import re

patron_tema = re.compile('<TOPICS>')
total_noticias = 0
longitud_palabra = 0
titulo = ""

flag = False
for linea in sys.stdin:
    if patron_tema.match(linea):
        linea = linea.split('<TOPICS>')[1]
        linea = linea.split('</TOPICS>')[0]
        linea.strip()
        linea = linea.replace('</D>', ',')
        temas = re.sub("<.*?>", "", linea).lower()
        temas = temas[:-1]
        if temas == "":
            temas = list('')
        if temas != list(''):
            temas = temas.split(',')
        #print(temas)
        for tema in temas:            
            print '%s\t%s' % (tema, 1)