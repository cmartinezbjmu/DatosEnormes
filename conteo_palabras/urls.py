from django.urls import path
from conteo_palabras.views import ContadorView, contadorPalabras, cantPalabrasArchivo, topNPalabras, topNPalabrasR4, topNPalabrasR5

urlpatterns = [
    path('reto_1/', contadorPalabras, name='cuenta_palabras'),
    path('reto_2/', cantPalabrasArchivo, name='cant_palabras'),
    path('reto_3/', topNPalabras, name='top_n_palabras'),
    path('reto_4/', topNPalabrasR4, name='top_n_palabras'),
    path('reto_5/', topNPalabrasR5, name='top_n_palabras'),
    
]