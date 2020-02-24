#!/usr/bin/env python

import sys
import re

patron_body = re.compile('<BODY>')
patron_body_close = re.compile('</BODY>')
total_noticias = 0

flag = False
for linea in sys.stdin:
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
    
    if patron_body_close.findall(linea):        
        total_noticias += 1
        print '%s\t%s' % (total_noticias, total_palabras)
        #print("{}\t{}".format(total_noticias, total_palabras))
           
            
        
    
    
