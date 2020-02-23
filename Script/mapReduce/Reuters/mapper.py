#!/usr/bin/env python

import sys
import re

patron_titulo = re.compile('<TITLE>')
for linea in sys.stdin:
    if patron_titulo.match(linea):
        # captira el titulo
        titulo = re.sub("<.*?>", "", linea).lower()
        titulo = titulo.strip()
        palabras = titulo.split()

        for palabra in palabras:            
            print '%s\t%s' % (palabra, 1)
        
    
    
