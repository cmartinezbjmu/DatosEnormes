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

def capturar_noticias(**kwargs):    
    # Ruta de los archivos
    path='../Dataset/'
    grupo_noticias = []
    palabras_noticia = dict()
    frecuencia_palabra_noticia = dict()
    if sys.argv:
        argumentos = sys.argv
    else:
        argumentos = kwargs.get('archivos', None)
        top = kwargs.get('top', 1)
        
    for i in argumentos[2:len(argumentos)]:     
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

frecuencia_palabras = Counter(lista_palabras)
# Resultado reto a
print("a) El archivo " + sys.argv[2] + " tiene " + str(len(lista_palabras)) + " palabras")

## --------------------------------------

# Resultado reto b

# print("b) Frecuencia de Palabras")
# for palabra in frecuencia_palabras:
#     print(palabra + ': ' + str(frecuencia_palabras[palabra]))

## --------------------------------------

# Palabras más comunes 
N = sys.argv[1]

# Resultado reto c, d, e y f
# Cantidad de palabras en el top N
top_palabras = frecuencia_palabras.most_common(int(N))
# print("c) Top " + str(N) + " de palabras")
# for palabras in top_palabras:
#     print(palabras)
# 
# print("d) Top " + str(N) + " de palabras en el archivo " + sys.argv[2])
# for palabras in top_palabras:
#     print(palabras)

print("e) Top " + str(N) + " de palabras en los archivos " + ' '.join(sys.argv[2:len(sys.argv)]))   
for palabras in top_palabras:
    print(palabras)

## --------------------------------------
# Resultado g
palabra_buscar = 'of'
archivo_max_palabras = max(palabras_noticia, key=palabras_noticia.get)
print('g) El archivo que contiene más veces la palabra ' + palabra_buscar + ' es: ' + max_palabra_archivo(palabra_buscar))
print('g) Archivo con mayor cantidad de palabras: ' + archivo_max_palabras)

# Crea el archivo para el almacenamiento de respuestas

fw = open("resultado-"+ datetime.now().strftime("%d-%m-%Y_%I-%M") + ".txt","a+")
fw.write("Para el archivo " + sys.argv[2] + " las " + sys.argv[1] + " palabras más frecuentes son: \n")
for palabra in top_palabras:
    fw.write(str(palabra[0]) + ':' + str(palabra[1]) + '\n')
fw.write('\n')
fw.close()
print('=' * 60)
