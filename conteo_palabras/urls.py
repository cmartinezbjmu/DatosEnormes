from django.urls import path
from conteo_palabras.views import ContadorView, contadorPalabras

urlpatterns = [
    path('contar_palabras/', contadorPalabras, name='cuenta_palabras')
]