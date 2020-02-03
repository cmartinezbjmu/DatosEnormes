from django.urls import path
from conteo_palabras.views import ContadorView

urlpatterns = [
    path('contar_palabras/', ContadorView.as_view(), name='cuenta_palabras')
]