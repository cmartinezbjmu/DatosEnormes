from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from conteo_palabras.forms import ContadorPalabras, topNPalabrasForm, topNPalabrasFormR4, topNPalabrasFormR5, topNPalabrasFormR6, topNPalabrasFormR7
from django.urls import reverse_lazy
from django.contrib import messages
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from io import BytesIO
from base64 import b64encode
from django.template.loader import get_template
import urllib


from bs4 import BeautifulSoup
## Eliminar caracteres especiales
from nltk.tokenize import RegexpTokenizer
## Conteo de palabras
from collections import Counter

def capturar_noticias(**kwargs):    
    # Ruta de los archivos
    path='Dataset/'
    grupo_noticias = []
    palabras_noticia = dict()
    frecuencia_palabra_noticia = dict()
    
    argumentos = kwargs.get('archivos', None)
    top = kwargs.get('top', 1)
    #for i in sys.argv[2:len(sys.argv)]:     
    total_palabras = 0
    with open(path + argumentos, 'rb') as f:
        s = BeautifulSoup(f, 'html.parser')
        palabras = []
        for j in s.find_all('body'):
            total_palabras += len(contar_palabras(j.text))
            palabras.append(j.text)
            grupo_noticias.append(j.text)
        palabras_noticia.update({argumentos:len(contar_palabras(palabras))})
        frecuencia_palabra_noticia.update({argumentos:Counter(contar_palabras(palabras))})

    f.close()
    return grupo_noticias

def contar_palabras(noticia):
    ## Eliminar stop words
    tokenizer = RegexpTokenizer(r'\w+')
    lista_palabras = []
    for i in noticia:
        frases = tokenizer.tokenize(i)
        lista_palabras.extend(frases)
    return lista_palabras

def contadorPalabras(request):
    form = ContadorPalabras(request.POST or None)
    if form.is_valid():              
        nombre_archivo = form.cleaned_data['nombre_archivo']
        noticias = capturar_noticias(archivos=nombre_archivo)
        lista_palabras = contar_palabras(noticias)
        messages.success(request, 'La cantidad de palabras del archivo ' + nombre_archivo + ' es: ' + str(len(lista_palabras)))
    context = {
        'form': form        
    }

    return render(request, 'contador_palabras.html', context)

def cantPalabrasArchivo(request):    
    form = ContadorPalabras(request.POST or None)
    if form.is_valid():
        nombre_archivo = form.cleaned_data['nombre_archivo']
        noticias = capturar_noticias(archivos=nombre_archivo)
        lista_palabras = contar_palabras(noticias)
        frecuencia_palabras = Counter(lista_palabras)
        top_palabras = frecuencia_palabras.most_common(len(frecuencia_palabras))
        # Crea nube de palabras
        imag_uri = nubePalabras(top_palabras)
        
        context = {
            #'frecuencia_palabras': frecuencia_palabras.items
            'imag_uri': imag_uri,
            'nombre_archivo': nombre_archivo
        }
        return render(request, 'frecuencia_palabras.html', context)
        
    context = {
        'form': form,        
    }
    
    return render(request, 'contador_palabras.html', context)

def nubePalabras(palabras_top):
    frecuentes_diccionario = dict(palabras_top)
    wordcloud = WordCloud(background_color="white")
    wordcloud.generate_from_frequencies(frequencies=frecuentes_diccionario)    
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    #plt.show()
    figure = plt.gcf()    
    buf = BytesIO()
    figure.savefig(buf, format='png', transparent=True, quality=100, dpi=200)
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    imag_src = b64encode(image_png)
    image_out = imag_src.decode('utf-8')
    #imag_uri = 'data:image/png;base64,{}'.format(urllib.parse.quote(imag_src))

    return image_out

#def frecuencia_palabra_noticia():
    

def max_palabra_archivo(palabra, archivos, frecuencia_palabra_noticia):
    max = 0
    for archivo in archivos: 
        if frecuencia_palabra_noticia[archivo][palabra] > max:
            nombre_archivo = archivo
            max = frecuencia_palabra_noticia[archivo][palabra]
    return nombre_archivo

def topNPalabras(request):
    form = topNPalabrasForm(request.POST or None)
    if form.is_valid():
        nombre_archivo = 'reut2-000.sgm'
        top = form.cleaned_data['no_palabras']
        noticias = capturar_noticias(archivos=nombre_archivo)
        lista_palabras = contar_palabras(noticias)
        frecuencia_palabras = Counter(lista_palabras)
        top_palabras = frecuencia_palabras.most_common(int(top))
        # Crea nube de palabras
        imag_uri = nubePalabras(top_palabras)

        context = {
            'top_palabras': top_palabras,
            'nombre_archivo': nombre_archivo,
            'top': top,
            'imag_uri': imag_uri
        }
        return render(request, 'top_n_palabras_result.html', context)
        
    context = {
        'form': form,        
    }
    
    return render(request, 'top_n_palabras.html', context)


def topNPalabrasR4(request):
    form = topNPalabrasFormR4(request.POST or None)
    if form.is_valid():
        nombre_archivo = form.cleaned_data['nombre_archivo']
        top = form.cleaned_data['no_palabras']
        noticias = capturar_noticias(archivos=nombre_archivo)
        lista_palabras = contar_palabras(noticias)
        frecuencia_palabras = Counter(lista_palabras)
        top_palabras = frecuencia_palabras.most_common(int(top))
        # Crea nube de palabras
        imag_uri = nubePalabras(top_palabras)

        context = {
            'top_palabras': top_palabras,
            'nombre_archivo': nombre_archivo,
            'top': top,
            'imag_uri': imag_uri
        }
        return render(request, 'top_n_palabras_result.html', context)
        
    context = {
        'form': form,        
    }
    
    return render(request, 'top_n_palabras.html', context)


def topNPalabrasR5(request):
    form = topNPalabrasFormR5(request.POST or None)
    if form.is_valid():
        nombre_archivo = []
        top_palabras = []
        nombre_archivo.append(form.cleaned_data['nombre_archivo'])
        nombre_archivo.append(form.cleaned_data['nombre_archivo2'])
        top = form.cleaned_data['no_palabras']

        for i in nombre_archivo:
            noticias = capturar_noticias(archivos=i)
            lista_palabras = contar_palabras(noticias)
            frecuencia_palabras = Counter(lista_palabras)
            top_palabras.append(frecuencia_palabras.most_common(int(top)))
        
        
        # Crea nube de palabras
        imag_uri1 = nubePalabras(top_palabras[0])
        imag_uri2 = nubePalabras(top_palabras[1])
        
        context = {
            'top_palabras': top_palabras[0],
            'top_palabras2': top_palabras[1],
            'nombre_archivo': nombre_archivo[0],
            'nombre_archivo2': nombre_archivo[1],
            'top': top,
            'imag_uri1': imag_uri1,
            'imag_uri2': imag_uri2,
        }
        return render(request, 'top_n_palabras_result_r5.html', context)
        
    context = {
        'form': form,        
    }
    
    return render(request, 'top_n_palabras.html', context)


def topNPalabrasR6(request):
    form = topNPalabrasFormR6(request.POST or None)
    if form.is_valid():
        nombre_archivo = []
        top_palabras = []
        nombre_archivo.append(form.cleaned_data['nombre_archivo'])
        nombre_archivo.append(form.cleaned_data['nombre_archivo2'])
        nombre_archivo.append(form.cleaned_data['nombre_archivo3'])
        top = form.cleaned_data['no_palabras']

        for i in nombre_archivo:
            noticias = capturar_noticias(archivos=i)
            lista_palabras = contar_palabras(noticias)
            frecuencia_palabras = Counter(lista_palabras)
            top_palabras.append(frecuencia_palabras.most_common(int(top)))
        
        # Crea nube de palabras
        imag_uri1 = nubePalabras(top_palabras[0])
        imag_uri2 = nubePalabras(top_palabras[1])
        imag_uri3 = nubePalabras(top_palabras[2])
        
        context = {
            'top_palabras': top_palabras[0],
            'top_palabras2': top_palabras[1],
            'top_palabras3': top_palabras[2],
            'nombre_archivo': nombre_archivo[0],
            'nombre_archivo2': nombre_archivo[1],
            'nombre_archivo3': nombre_archivo[2],
            'top': top,
            'imag_uri1': imag_uri1,
            'imag_uri2': imag_uri2,
            'imag_uri3': imag_uri3,
        }
        return render(request, 'top_n_palabras_result_r6.html', context)
        
    context = {
        'form': form,        
    }
    
    return render(request, 'top_n_palabras.html', context)



def topNPalabrasR7(request):
    form = topNPalabrasFormR7(request.POST or None)
    if form.is_valid():
        nombre_archivo = []
        nombre_archivo.append(form.cleaned_data['nombre_archivo'])
        nombre_archivo.append(form.cleaned_data['nombre_archivo2'])
        nombre_archivo.append(form.cleaned_data['nombre_archivo3'])
        palabra = form.cleaned_data['palabra']

        cantidad_palabras = 0
        frecuencia_palabra_noticia = dict()
        for i in nombre_archivo:
            noticias = capturar_noticias(archivos=i)
            lista_palabras = contar_palabras(noticias)
            frecuencia_palabra_noticia.update({i:Counter(contar_palabras(lista_palabras))})
            if len(lista_palabras) >= cantidad_palabras:
                cantidad_palabras = len(lista_palabras)
                archivo = i

        nombre_archivo = max_palabra_archivo(palabra, nombre_archivo, frecuencia_palabra_noticia)

        context = {
            'nombre_archivo': archivo,
            'palabra': palabra,
            'archivo2': nombre_archivo
        }
        return render(request, 'top_n_palabras_result_r7.html', context)
        
    context = {
        'form': form,        
    }
    
    return render(request, 'buscador_palabras.html', context)