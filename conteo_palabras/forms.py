from django import forms
import os

def listarArchivos():
    lista_archivos = []
    for archivo in os.listdir('Dataset/'):
        if archivo.endswith('.sgm'):
            lista_archivos.append(archivo)
    
    return sorted(lista_archivos)

LISTA_ARCHIVOS = [(archivo, archivo) for archivo in listarArchivos()]


class ContadorPalabras(forms.Form):
    nombre_archivo = forms.CharField(required=True, widget=forms.Select(choices=LISTA_ARCHIVOS))
    

class topNPalabrasForm(forms.Form):
    no_palabras = forms.CharField(required=True, widget=forms.NumberInput)

class topNPalabrasFormR4(forms.Form):
    nombre_archivo = forms.CharField(required=True, widget=forms.Select(choices=LISTA_ARCHIVOS))
    no_palabras = forms.CharField(required=True, widget=forms.NumberInput)

class topNPalabrasFormR5(forms.Form):
    nombre_archivo = forms.CharField(required=True, widget=forms.Select(choices=LISTA_ARCHIVOS))
    nombre_archivo2 = forms.CharField(required=True, widget=forms.Select(choices=LISTA_ARCHIVOS))
    no_palabras = forms.CharField(required=True, widget=forms.NumberInput)

class topNPalabrasFormR6(forms.Form):
    nombre_archivo = forms.CharField(required=True, widget=forms.Select(choices=LISTA_ARCHIVOS))
    nombre_archivo2 = forms.CharField(required=True, widget=forms.Select(choices=LISTA_ARCHIVOS))
    nombre_archivo3 = forms.CharField(required=True, widget=forms.Select(choices=LISTA_ARCHIVOS))
    no_palabras = forms.CharField(required=True, widget=forms.NumberInput)


class topNPalabrasFormR7(forms.Form):
    nombre_archivo = forms.CharField(required=True, widget=forms.Select(choices=LISTA_ARCHIVOS))
    nombre_archivo2 = forms.CharField(required=True, widget=forms.Select(choices=LISTA_ARCHIVOS))
    nombre_archivo3 = forms.CharField(required=True, widget=forms.Select(choices=LISTA_ARCHIVOS))
    palabra = forms.CharField(required=True, widget=forms.TextInput)