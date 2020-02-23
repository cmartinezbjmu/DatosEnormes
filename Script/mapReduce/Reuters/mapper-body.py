#!/usr/bin/env python

import sys
import re

patron_body = re.compile('<BODY>')
patron_body_close = re.compile('</BODY>')
flag = False
for linea in sys.stdin:
    if patron_body.findall(linea):
        linea = linea.split('<BODY>')[1]
        linea = linea.split('</BODY>')[0]
        flag = True

    if flag:        
        # captura el body        
        body = re.sub("<.*?>", "", linea).lower()        
        body = body.strip()        
        palabras = body.split()
        
        for palabra in palabras:            
            print '%s\t%s' % (palabra, 1)
            
            
        
    
    
