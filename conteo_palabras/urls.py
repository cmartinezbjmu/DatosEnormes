from django.urls import path
from conteo_palabras.views import ContadorView, contadorPalabras, cantPalabrasArchivo

urlpatterns = [
    path('reto_1/', contadorPalabras, name='cuenta_palabras'),
    path('reto_2/', cantPalabrasArchivo, name='cant_palabras'),
    
]