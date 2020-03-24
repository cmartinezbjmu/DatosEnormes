#!/usr/bin/env python

import sys
import datetime
import datetime
#from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt 


zonas=dict()
zonas={'latitude': {1: 40.690657, 2: 40.603993599999995, 3: 40.862916999999996, 4: 40.7251022, 5: 40.55662, 6: 40.604432, 7: 40.772014500000004, 8: 40.7788277, 9: 40.7614516, 10: 40.680896000000004, 11: 40.6018495, 12: 40.70282775, 13: 40.7110166, 14: 40.6339929, 15: 40.792896999999996, 16: 40.768435100000005, 17: 40.72002979999999, 18: 40.8700999, 19: 40.7327778, 20: 40.855277799999996, 21: 40.60497720000001, 22: 40.60497720000001, 23: 40.607576, 24: 40.7997764, 25: 40.68562615, 26: 40.633993, 27: 40.563225, 28: 40.710739000000004, 29: 40.57964365, 30: 40.606400799999996, 31: 40.8588468, 32: 40.8506558, 33: 40.69608485000001, 34: 40.6997716, 35: 40.6672357, 36: 40.6942696, 37: 40.6942696, 38: 40.6945474, 39: 40.643715, 40: 40.6784201, 41: 40.8078786, 42: 40.809578, 43: 40.7827725, 44: 40.508612, 45: 40.716491299999994, 46: 40.847456, 47: 40.838578000000005, 48: 40.76442279999999, 49: 40.6897222, 50: 40.76442279999999, 51: 40.8738889, 52: 40.6875, 53: 40.7876014, 54: 40.716370700000006, 55: 40.57592745, 56: 40.7469593, 57: 40.7469593, 58: 40.8391667, 59: 40.8389019, 60: 40.8366014, 61: 40.667471, 62: 40.667471, 63: 40.6899088, 64: 40.768713, 65: 40.693736, 66: 40.703725, 67: 40.6204716, 68: 40.7464906, 69: 40.824325, 70: 40.7612123, 71: 40.637485, 72: 40.658515, 73: 40.7575366, 74: 40.7947222, 75: 40.7947222, 76: 40.6667702, 77: 40.656597, 78: 40.845378100000005, 79: 40.7292688, 80: 40.714622, 81: 40.8884329, 82: 40.7365804, 83: 40.730212, 84: 40.534346, 85: 40.649548200000005, 86: 40.605382500000005, 87: 40.7076124, 88: 40.7076124, 89: 40.640145399999994, 90: 40.7410592, 91: 40.621215500000005, 92: 40.7654301, 93: 40.7407093, 94: 40.861475399999996, 95: 40.7195942, 96: 40.68623, 97: 40.6907711, 98: 40.7348246, 99: 40.5791894, 100: 40.7536941, 101: 40.7470463, 102: 40.7014917, 103: 40.700303999999996, 104: 40.700303999999996, 105: 40.700303999999996, 106: 40.6791695, 107: 40.7355189, 108: 40.5961338, 109: 40.5542718, 110: 40.55614525, 111: 40.65220295, 112: 40.723713399999994, 113: 40.7319802, 114: 40.7319802, 115: 40.6187152, 116: 40.8241451, 117: 40.5913241, 118: 40.588333299999995, 119: 40.8460552, 120: 40.8460552, 121: 40.732447799999996, 122: 40.7134361, 123: 40.58611335, 124: 40.6578815, 125: 40.726803499999995, 126: 40.8126008, 127: 40.869257899999994, 128: 40.87227365, 129: 40.755656099999996, 130: 40.7127281, 131: 40.71332165, 132: 40.6429479, 133: 40.6462149, 134: 40.7139415, 135: 40.738548, 136: 40.872570200000006, 137: 40.7395463, 138: 40.7757145, 139: 40.666770299999996, 140: 40.766436600000006, 141: 40.766436600000006, 142: 40.77231939999999, 143: 40.77231939999999, 144: 40.721047, 145: 40.748699, 146: 40.7415095, 147: 40.8162916, 148: 40.7159357, 149: 40.7120612, 150: 40.57667355, 151: 40.7997764, 152: 40.8157775, 153: 40.876298299999995, 154: 40.590846, 155: 40.611026, 156: 40.6367701, 157: 40.723158000000005, 158: 40.740283000000005, 159: 40.8256703, 160: 40.7182153, 161: 40.7622684, 162: 40.7598219, 163: 40.7622684, 164: 40.749841700000005, 165: 40.618882299999996, 166: 40.81, 167: 40.829267200000004, 168: 40.803596999999996, 169: 40.849134, 170: 40.76, 171: 40.76, 172: 40.572935, 173: 40.7469593, 174: 40.8772593, 175: 40.753991, 176: 40.563994, 177: 40.67573170000001, 178: 40.5763146, 179: 40.772014500000004, 180: 40.67677, 181: 40.6701033, 182: 40.8389893, 183: 40.8662112, 184: 40.85413105, 185: 40.8592334, 186: 40.747938, 187: 40.6331592, 188: 40.659504, 189: 40.6778708, 190: 40.66177430000001, 191: 40.72676920000001, 192: 40.7552023, 193: 40.754884000000004, 194: 40.796767700000004, 195: 40.6751032, 196: 40.72293705, 197: 40.699425299999994, 198: 40.7080556, 199: 40.79193175, 200: 40.900316, 201: 40.5805104, 202: 40.7614177, 203: 40.6620479, 204: 40.541774100000005, 205: 40.6984364, 206: 40.643491999999995, 207: 40.763766, 208: 40.823387, 209: 40.705775200000005, 210: 40.591216100000004, 211: 40.722879999999996, 212: 40.824298, 213: 40.807533, 214: 40.589453000000006, 215: 40.7127281, 216: 40.670103499999996, 217: 40.714622, 218: 40.678159, 219: 40.678159, 220: 40.881799, 221: 40.6264774, 222: 40.6478541, 223: 40.7745459, 224: 40.731533, 225: 40.685497100000006, 226: 40.7398242, 227: 40.644337, 228: 40.644337, 229: 40.75565875, 230: 40.760443, 231: 40.715380200000006, 232: 40.715373, 233: 40.75026105, 234: 40.7359091, 235: 40.856708000000005, 236: 40.7737016, 237: 40.7737016, 238: 40.787045500000005, 239: 40.787045500000005, 240: 40.8970755, 241: 40.883414, 242: 40.846769, 243: 40.8401984, 244: 40.8401984, 245: 40.5780867, 246: 40.755103999999996, 247: 40.830512, 248: 40.842147, 249: 40.734185700000005, 250: 40.830898, 251: 40.621215, 252: 40.79454570000001, 253: 40.796708, 254: 40.871333, 255: 40.714622, 256: 40.704459, 257: 40.655784600000004, 258: 40.6892698, 259: 40.897599, 260: 40.745379799999995, 261: 40.7118914, 262: 40.778006700000006, 263: 40.778006700000006, 264: 0.0, 265: 0.0}, 'longitude': {1: -74.177543, 2: -73.83541240000001, 3: -73.843405, 4: -73.9795833, 5: -74.176278, 6: -74.05897399999999, 7: -73.9302673, 8: -73.92262648880974, 9: -73.78972390000001, 10: -73.78763199999999, 11: -74.000501, 12: -74.01581850755983, 13: -74.0169369, 14: -74.0145841, 15: -73.776299, 16: -73.77707740000001, 17: -73.95552729999999, 18: -73.8856912, 19: -73.7177778, 20: -73.88638890000001, 21: -73.9934061, 22: -73.9934061, 23: -74.096325, 24: -73.96777159999999, 25: -73.98417065807277, 26: -73.9968059, 27: -73.898261, 28: -73.81356600000001, 29: -73.96111081059607, 30: -73.81901879728136, 31: -73.87590377196466, 32: -73.86652409999999, 33: -73.99502783912651, 34: -73.9753359, 35: -73.9067979, 36: -73.91874820000001, 37: -73.91874820000001, 38: -73.73846529999999, 39: -73.9006921, 40: -73.9948021, 41: -73.94541540000002, 42: -73.94779100000001, 43: -73.9653627406542, 44: -74.22321099999999, 45: -73.99625040000001, 46: -73.78646637155543, 47: -73.902035, 48: -73.9923918, 49: -73.9652778, 50: -73.9923918, 51: -73.8294444, 52: -73.9980556, 53: -73.8459682, 54: -73.98062159999999, 55: -73.99219674341339, 56: -73.8601456, 57: -73.8601456, 58: -73.8197222, 59: -73.89386451155043, 60: -73.8929618, 61: -73.9435662, 62: -73.9435662, 63: -73.8726597, 64: -73.7470765, 65: -73.984487, 66: -73.99067099999999, 67: -74.0116668, 68: -74.00152829999999, 69: -73.919137, 70: -73.8651358, 71: -73.94646, 72: -73.924993, 73: -73.78430452865169, 74: -73.9425, 75: -73.9425, 76: -73.88235829999999, 77: -73.889238, 78: -73.8909693, 79: -73.9873613, 80: -73.95345, 81: -73.82818950000001, 82: -73.8783932, 83: -73.887491, 84: -74.185652, 85: -73.95597140000001, 86: -73.75513259999998, 87: -74.009378, 88: -74.009378, 89: -73.9608797, 90: -73.98964162240998, 91: -73.9348597, 92: -73.8174291, 93: -73.8432447636799, 94: -73.8905439, 95: -73.84485529999999, 96: -73.885806, 97: -73.9766245, 98: -73.79346679999999, 99: -74.17992554500482, 100: -73.9905167, 101: -73.7115199, 102: -73.8868028, 103: -74.041134, 104: -74.041134, 105: -74.041134, 106: -73.9885041, 107: -73.98407940000001, 108: -73.9739426, 109: -74.1515318, 110: -74.10845705329207, 111: -73.99107393108886, 112: -73.9509714, 113: -73.9965658, 114: -73.9965658, 115: -74.09347509999999, 116: -73.9500618, 117: -73.8079742, 118: -74.15777779999999, 119: -73.9297329337184, 120: -73.9297329337184, 121: -73.80883093979648, 122: -73.7670772, 123: -73.95731014951106, 124: -73.83624590000001, 125: -74.00798329999999, 126: -73.8840247, 127: -73.92049490000001, 128: -73.92542709150258, 129: -73.8857755, 130: -74.0060152, 131: -73.78250595420786, 132: -73.7793733748521, 133: -73.970694, 134: -73.830742, 135: -73.810413, 136: -73.90266190000001, 137: -73.97708320000001, 138: -73.87336398511545, 139: -73.7515212, 140: -73.9590168, 141: -73.9590168, 142: -73.9844012, 143: -73.9844012, 144: -73.996224, 145: -73.95023499999999, 146: -73.9569751, 147: -73.8962205, 148: -73.9868057, 149: -73.9983332, 150: -73.94106733063637, 151: -73.96777159999999, 152: -73.951554, 153: -73.9104292, 154: -73.890985, 155: -73.910558, 156: -74.1587547, 157: -73.912637, 158: -74.007892, 159: -73.9152416, 160: -73.87867088764077, 161: -73.9795443, 162: -73.9724708, 163: -73.9795443, 164: -73.984251, 165: -73.96548890000001, 166: -73.9625, 167: -73.9065253, 168: -73.919798, 169: -73.906462, 170: -73.8130556, 171: -73.8130556, 172: -74.1152, 173: -73.8601456, 174: -73.8768626, 175: -73.765966, 176: -74.11597540000001, 177: -73.9124338, 178: -73.96853709999999, 179: -73.9302673, 180: -73.84374609999999, 181: -73.9859723, 182: -73.8604128, 183: -73.78957740000001, 184: -73.82217330144337, 185: -73.8550166, 186: -73.990468, 187: -74.1365318, 188: -73.95605400000001, 189: -73.9684725, 190: -73.97108902901994, 191: -73.7415208, 192: -73.88701970000001, 193: -73.945387, 194: -73.92208149999999, 195: -74.00958409999998, 196: -73.86220651513042, 197: -73.8309672, 198: -73.9141667, 199: -73.88349371727948, 200: -73.90477299999999, 201: -73.83615350000001, 202: -73.9502281671115, 203: -73.7354097, 204: -74.20807420000001, 205: -73.7606881, 206: -74.080202, 207: -73.89743100000001, 208: -73.809451, 209: -74.00283759999999, 210: -73.9445822, 211: -73.9987505, 212: -73.87020799999999, 213: -73.852145, 214: -74.087485, 215: -74.0060152, 216: -73.8190231, 217: -73.95345, 218: -73.746521, 219: -73.746521, 220: -73.905007, 221: -74.07763609999999, 222: -73.87951545688418, 223: -73.90374770000001, 224: -73.978561, 225: -73.94113505947442, 226: -73.93541529999999, 227: -74.007532, 228: -74.007532, 229: -73.96526737133506, 230: -73.983964, 231: -74.00930629999999, 232: -73.988904, 233: -73.96719495316776, 234: -73.99016259999999, 235: -73.910836, 236: -73.9641196, 237: -73.9641196, 238: -73.97541629999999, 239: -73.97541629999999, 240: -73.8865797057321, 241: -73.89245799999999, 242: -73.859981, 243: -73.9402214, 244: -73.9402214, 245: -73.9749245520036, 246: -74.002415, 247: -73.923735, 248: -73.881476, 249: -74.00558000000001, 250: -73.870101, 251: -74.13180940000001, 252: -73.81846740000002, 253: -73.77939599999999, 254: -73.86858199999999, 255: -73.95345, 256: -73.956272, 257: -73.9765441, 258: -73.85791309999999, 259: -73.859298, 260: -73.9054145, 261: -74.01261290000001, 262: -73.9482022, 263: -73.9482022, 264: 0.0, 265: 0.0}}

zonas_bor={1: 3, 2: 5, 3: 1, 4: 4, 5: 6, 6: 6, 7: 5, 8: 5, 9: 5, 10: 5, 11: 2, 12: 4, 13: 4, 14: 2, 15: 5, 16: 5, 17: 2, 18: 1, 19: 5, 20: 1, 21: 2, 22: 2, 23: 6, 24: 4, 25: 2, 26: 2, 27: 5, 28: 5, 29: 2, 30: 5, 31: 1, 32: 1, 33: 2, 34: 2, 35: 2, 36: 2, 37: 2, 38: 5, 39: 2, 40: 2, 41: 4, 42: 4, 43: 4, 44: 6, 45: 4, 46: 1, 47: 1, 48: 4, 49: 2, 50: 4, 51: 1, 52: 2, 53: 5, 54: 2, 55: 2, 56: 5, 57: 5, 58: 1, 59: 1, 60: 1, 61: 2, 62: 2, 63: 2, 64: 5, 65: 2, 66: 2, 67: 2, 68: 4, 69: 1, 70: 5, 71: 2, 72: 2, 73: 5, 74: 4, 75: 4, 76: 2, 77: 2, 78: 1, 79: 4, 80: 2, 81: 1, 82: 5, 83: 5, 84: 6, 85: 2, 86: 5, 87: 4, 88: 4, 89: 2, 90: 4, 91: 2, 92: 5, 93: 5, 94: 1, 95: 5, 96: 5, 97: 2, 98: 5, 99: 6, 100: 4, 101: 5, 102: 5, 103: 4, 104: 4, 105: 4, 106: 2, 107: 4, 108: 2, 109: 6, 110: 6, 111: 2, 112: 2, 113: 4, 114: 4, 115: 6, 116: 4, 117: 5, 118: 6, 119: 1, 120: 4, 121: 5, 122: 5, 123: 2, 124: 5, 125: 4, 126: 1, 127: 4, 128: 4, 129: 5, 130: 5, 131: 5, 132: 5, 133: 2, 134: 5, 135: 5, 136: 1, 137: 4, 138: 5, 139: 5, 140: 4, 141: 4, 142: 4, 143: 4, 144: 4, 145: 5, 146: 5, 147: 1, 148: 4, 149: 2, 150: 2, 151: 4, 152: 4, 153: 4, 154: 2, 155: 2, 156: 6, 157: 5, 158: 4, 159: 1, 160: 5, 161: 4, 162: 4, 163: 4, 164: 4, 165: 2, 166: 4, 167: 1, 168: 1, 169: 1, 170: 4, 171: 5, 172: 6, 173: 5, 174: 1, 175: 5, 176: 6, 177: 2, 178: 2, 179: 5, 180: 5, 181: 2, 182: 1, 183: 1, 184: 1, 185: 1, 186: 4, 187: 6, 188: 2, 189: 2, 190: 2, 191: 5, 192: 5, 193: 5, 194: 4, 195: 2, 196: 5, 197: 5, 198: 5, 199: 1, 200: 1, 201: 5, 202: 4, 203: 5, 204: 6, 205: 5, 206: 6, 207: 5, 208: 1, 209: 4, 210: 2, 211: 4, 212: 1, 213: 1, 214: 6, 215: 5, 216: 5, 217: 2, 218: 5, 219: 5, 220: 1, 221: 6, 222: 2, 223: 5, 224: 4, 225: 2, 226: 5, 227: 2, 228: 2, 229: 4, 230: 4, 231: 4, 232: 4, 233: 4, 234: 4, 235: 1, 236: 4, 237: 4, 238: 4, 239: 4, 240: 1, 241: 1, 242: 1, 243: 4, 244: 4, 245: 6, 246: 4, 247: 1, 248: 1, 249: 4, 250: 1, 251: 6, 252: 5, 253: 5, 254: 1, 255: 2, 256: 2, 257: 2, 258: 5, 259: 1, 260: 5, 261: 4, 262: 4, 263: 4, 264: 7, 265: 7}


# Distancia de Harvesine
def distance(lat1,lon1,lat2,lon2):   
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2  
    c = 2 * asin(sqrt(a))  
     
    # Radio de la tierra
    r = 6371
    
    # calculate the result 
    return(c * r) 


# Encontrar la zona mas cercana
def min_distance(lat,lon):
    minima=100000000
    for i in range(1,265):
        distancia=distance(lat,lon,zonas["latitude"][i],zonas["longitude"][i])
        if distancia<minima:
            minima=distancia
            posicion=i
    return posicion


def conversion_tiempo(hora):    
    hora = int(hora[0]) * 60 + int(hora[1])
    return hora


hora=[]
tipo_vehi = ''
l = None
sitio = None
fecha=''
fecha_hora=''
destino=None
lat=''
lon=''

for linea in sys.stdin:
    linea.strip()
    if '"' in linea: linea = linea.replace('"', '')
    try:
        # if 'csv' not in linea:
        l = linea.split(',')        
    except IndexError as e:
        pass
    
    if l:
        # sitio de recogida
        if (l[0].lower != 'vendorid') or (l[0].lower != 'pickup_datetime') or (r'\x00' not in l[0]):
            # fecha_hora = l[1].split()
            # fecha = fecha_hora[0].split('-')
            if (len(l) == 18): # yellow year 2019
                tipo_vehi = 'yellow'
                sitio = l[5]              
                precio = l[len(l)-2]
                destino = l[6]


            if (len(l) == 17): # Yellow 2017
                tipo_vehi = 'yellow'
                sitio = l[5]
                precio = l[len(l)-1]
                destino = l[6] 


            if len(l) == 20: # green year 2019
                tipo_vehi = 'green'
                sitio=l[7]
                precio = l[len(l)-4]
                destino = l[8]
 


                
            if  len(l) == 19 or len(l) == 21 :
                tipo_vehi = 'green'
                sitio=l[7]                  
                precio = l[len(l)-3]
                destino = l[8]

            try:
                fecha_hora = l[1].split()
                fecha = fecha_hora[0].split('-')
                longitud=l[5]
                latitud=l[6]              
                hora=fecha_hora[1].split(':')[0]
                # hora=[hora[0],hora[1]]
                if ((fecha[0] == '2016') or (fecha[0] == '2015')) and (len(l) == 19):
                    tipo_vehi = 'yellow'
                    precio = l[len(l)-3]   
                    lat = l[10]
                    lon = l[9]                
                
                if (fecha[0] == '2016') and (len(l) == 21):
                    tipo_vehi = 'green'
                    precio = l[len(l)-3]
                    lat = l[8]
                    lon = l[7]        
                    
   
                if (fecha[0] == '2015') and (len(l) == 21) or (len(l)==23):
                    tipo_vehi = 'green'
                    precio = l[len(l)-3]
                    lat = l[8]
                    lon = l[7]      

                    
                if ((fecha[0] == '2014') or (fecha[0] == '2013') or (fecha[0] == '2012') or (fecha[0] == '2011')  or (fecha[0] == '2010')  or (fecha[0] == '2009') ) and (len(l) == 18):
                    tipo_vehi = 'yellow'
                    precio = l[len(l)-1]
                    lat = l[10]
                    lon = l[9]      
                    

                    
                if ((fecha[0] == '2014') or (fecha[0] == '2013')) and (len(l) == 22):
                    tipo_vehi = 'green'
                    precio = l[len(l)-5]
                    lat = l[8]
                    lon = l[7]  
                      
                # print lat, lon, latitud, longitud, hora, sitio, destino
                try:
                    if (sitio is None and destino is None) or (sitio.isdigit()==False and destino.isdigit()==False) :
                        try:
                            sitio = str(min_distance(float(latitud),float(longitud)))
                            destino = str(min_distance(float(lat),float(lon)))
                        except:
                            sitio = '265'
                            destino = '265'
                        sitio= zonas_bor[int(sitio)]
                        destino=zonas_bor[int(destino)]
                        print '%s,%s' % (sitio,destino)
                except:
                    pass           
            except IndexError as e:
                pass
            
