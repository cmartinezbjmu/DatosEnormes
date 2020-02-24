#!/usr/bin/env python

import sys
import re

patron_body = re.compile('<BODY>')
patron_body_close = re.compile('</BODY>')
patron_titulo = re.compile('<TITLE>')
patron_fecha = re.compile('<DATE>')
patron_pais = re.compile('<PLACES>')
total_noticias = 0
longitud_palabra = 0
titulo = ""

flag = False
for linea in sys.stdin:
    if patron_pais.match(linea):
        linea = linea.split('<PLACES>')[1]
        linea = linea.split('</PLACES>')[0]
        linea.strip()
        linea = linea.replace('</D>', ' ')
        pais = re.sub("<.*?>", "", linea).lower()

    if patron_fecha.match(linea):
        linea = linea.split('<DATE>')[1]
        linea = linea.split('</DATE>')[0]
        linea.strip()
        fecha = re.sub("<.*?>", "", linea).lower()

    if patron_titulo.match(linea):
        linea = linea.split('<TITLE>')[1]
        linea = linea.split('</TITLE>')[0]
        linea.strip()
        titulo = re.sub("<.*?>", "", linea).lower()

    if patron_body.findall(linea):
        total_palabras = 0
        linea = linea.split('<BODY>')[1]
        linea = linea.split('</BODY>')[0]
        flag = True

    if flag:
        # captura el body        
        body = re.sub("<.*?>", "", linea).lower()        
        body = body.strip()        
        palabras = body.split()
        total_palabras += len(palabras)
        for palabra in palabras:
            if longitud_palabra < len(palabra):
                longitud_palabra = len(palabra)
                palabra_larga = palabra
        titulo_palabra = titulo
        fecha_palabra = fecha
        pais_noticia_max = pais
        
    if patron_body_close.findall(linea): 
        flag = False       
        total_noticias += 1
        longitud_palabra = 0
        print '%s\t%s\t%s\t%s\t%s' % (total_palabras, palabra_larga, titulo_palabra, fecha_palabra, pais_noticia_max)
        #print("{}\t{}\t{}\t{}\t{}".format(total_palabras, palabra_larga, titulo_palabra, fecha_palabra, pais_noticia_max))
    
