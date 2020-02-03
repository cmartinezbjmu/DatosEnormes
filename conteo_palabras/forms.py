from django import forms
#from Script import read_news

class ContadorPalabras(forms.Form):
    nombre_archivo = forms.CharField(help_text='Introduce aquí el nomrbre del archivo', required=True)
    

