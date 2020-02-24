#!/usr/bin/env python

import sys
import json

for linea in sys.stdin:
    archivo = json.loads(linea)
    palabras = archivo["title"].split(' ')
    
    for palabra in palabras:
        print '%s\t%s' % (palabra, 1)
        #print ('{}\t{}'.format(palabra, 1))