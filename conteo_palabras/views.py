from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from conteo_palabras.forms import ContadorPalabras, topNPalabrasForm, topNPalabrasFormR4
from django.urls import reverse_lazy
from django.contrib import messages


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
    Numero = 10
    return grupo_noticias

def contar_palabras(noticia):
    ## Eliminar stop words
    tokenizer = RegexpTokenizer(r'\w+')
    lista_palabras = []
    for i in noticia:
        frases = tokenizer.tokenize(i)
        lista_palabras.extend(frases)
    return lista_palabras


class ContadorView(FormView):
    template_name='contador_palabras.html'
    form_class = ContadorPalabras

    def form_valid(self, form):        
        noticias = capturar_noticias(archivos='reut2-000.sgm')
        return super().form_valid(form)


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
        
        context = {
            'frecuencia_palabras': frecuencia_palabras.items
        }
        return render(request, 'frecuencia_palabras.html', context)
        
    context = {
        'form': form,        
    }
    
    return render(request, 'contador_palabras.html', context)


def topNPalabras(request):
    form = topNPalabrasForm(request.POST or None)
    if form.is_valid():
        nombre_archivo = 'reut2-000.sgm'
        top = form.cleaned_data['no_palabras']
        noticias = capturar_noticias(archivos=nombre_archivo)
        lista_palabras = contar_palabras(noticias)
        frecuencia_palabras = Counter(lista_palabras)
        top_palabras = frecuencia_palabras.most_common(int(top))
        
        context = {
            'top_palabras': top_palabras,
            'nombre_archivo': nombre_archivo,
            'top': top
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
        
        context = {
            'top_palabras': top_palabras,
            'nombre_archivo': nombre_archivo,
            'top': top
        }
        return render(request, 'top_n_palabras_result.html', context)
        
    context = {
        'form': form,        
    }
    
    return render(request, 'top_n_palabras.html', context)