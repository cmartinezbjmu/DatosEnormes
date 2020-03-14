#!/usr/bin/env python

import sys
import re

for line in sys.stdin:
    line = line.split(',')
    
    if line[0] != 'VendorID':
        print '%s' % (line[0])

