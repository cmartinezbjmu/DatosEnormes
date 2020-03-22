from django.urls import path
from conteo_palabras.views import contadorPalabras, cantPalabrasArchivo, topNPalabras, topNPalabrasR4, topNPalabrasR5, topNPalabrasR6, topNPalabrasR7
from Taller1.views import resultadoHadoop

urlpatterns = [
    path('reto_1/', contadorPalabras, name='cuenta_palabras'),
    path('reto_2/', cantPalabrasArchivo, name='cant_palabras'),
    path('reto_3/', topNPalabras, name='top_n_palabras'),
    path('reto_4/', topNPalabrasR4, name='top_n_palabras'),
    path('reto_5/', topNPalabrasR5, name='top_n_palabras'),
    path('reto_6/', topNPalabrasR6, name='top_n_palabras'),
    path('reto_7/', topNPalabrasR7, name='top_n_palabras'),
    path('taller1/', resultadoHadoop, name='resultadoHadoop'),
]