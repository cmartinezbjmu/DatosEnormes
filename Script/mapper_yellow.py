import sys
import re
from datetime import datetime

for data in sys.stdin:
    linea=data.split(',')
    tiempo_recogida=datetime.strptime(linea[1], "%Y-%m-%d %H:%M:%S")
    hora=tiempo_recogida.hour    
    dia=tiempo_recogida.weekday()
    ubicacion_recoge=linea[7]
    ubicacion_deja=linea[8]
    tarifa=float(linea[10])+float(linea[11])
        
    # print '%s\t%s' % (palabra, 1)
    print('y',ubicacion_deja,hora,dia,tarifa,1)