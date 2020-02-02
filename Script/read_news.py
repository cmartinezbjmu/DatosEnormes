# -- coding: utf-8 --
"""
Created on Fri Jan 31 10:29:30 2020

@author: David.Ocampo
"""
### Manejo de html
from bs4 import BeautifulSoup
### Manejo de tablas
import pandas as pd
# Herramienta para análisis de lenguaje
import nltk 
#nltk.download('punkt')
# Stop words
#nltk.download('stopwords')
from nltk.corpus import stopwords
## Conteo de palabras
from collections import Counter
## Manejo de archivos
import os
## Comandos del sistema
import sys
## Eliminar caracteres especiales
from nltk.tokenize import RegexpTokenizer
# sistema de date & time
from datetime import datetime


## Funciones

def capturar_noticias():
    # Ruta de los archivos
    path='../Dataset/'
    grupo_noticias = []
    palabras_noticia = dict()
    frecuencia_palabra_noticia = dict()
    for i in sys.argv[2:len(sys.argv)]:     
        total_palabras = 0
        with open(path + i, 'rb') as f:
            s = BeautifulSoup(f, 'html.parser')
            palabras = []
            for j in s.find_all('body'):
                total_palabras += len(contar_palabras(j.text))
                palabras.append(j.text)
                grupo_noticias.append(j.text)
            palabras_noticia.update({i:len(contar_palabras(palabras))})
            frecuencia_palabra_noticia.update({i:Counter(contar_palabras(palabras))})
        f.close()
    print(palabras_noticia)

    #import json

    # as requested in comment
    #exDict = {'exDict': 1}

    #with open('file.txt', 'w') as file:
    #    file.write(json.dumps(frecuencia_palabra_noticia)) # use `json.loads` to do the reverse

    #print(frecuencia_palabra_noticia)
    return grupo_noticias, palabras_noticia, frecuencia_palabra_noticia

def contar_palabras(noticia):
    ## Eliminar stop words
    tokenizer = RegexpTokenizer(r'\w+')
    lista_palabras = []
    for i in noticia:
        frases = tokenizer.tokenize(i)
        lista_palabras.extend(frases)
    return lista_palabras

def max_palabra_archivo(palabra):
    max = 0
    for archivo in sys.argv[2:len(sys.argv)]: 
        if frecuencia_palabra_noticia[archivo][palabra] > max:
            nombre_archivo = archivo
            max = frecuencia_palabra_noticia[archivo][palabra]
    return nombre_archivo

noticias, palabras_noticia, frecuencia_palabra_noticia = capturar_noticias()
lista_palabras = contar_palabras(noticias)


## --------------------------------------

# Resultado reto b
frecuencia_palabras = Counter(lista_palabras)
print(len(lista_palabras))

## --------------------------------------

# Palabras más comunes 
N = sys.argv[1]

# Resultado reto c, d, e y f
# Cantidad de palabras en el top N
top_palabras = frecuencia_palabras.most_common(int(N))
print(top_palabras)

## --------------------------------------

print('Resultado reto G')

palabra_buscar = 'the'
print('El archivo que contiene más veces la palabra ' + palabra_buscar + ' es: ' + max_palabra_archivo(palabra_buscar))

archivo_max_palabras = max(palabras_noticia, key=palabras_noticia.get)
print('Archivo con mayor cantidad de palabras: ' + archivo_max_palabras)

# Crea el archivo para el almacenamiento de respuestas

fw = open("resultado-"+ datetime.now().strftime("%d-%m-%Y_%I-%M") + ".txt","a+")
fw.write("Para el archivo " + sys.argv[2] + " las " + sys.argv[1] + " palabras más frecuentes son: \n")
for palabra in top_palabras:
    fw.write(str(palabra[0]) + ':' + str(palabra[1]) + '\n')
fw.write('\n')
fw.close()
print('=' * 60)
