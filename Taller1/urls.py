from django.urls import path
from .views import reto1, reto2, reto3

urlpatterns = [
    path('reto_1/', reto1, name='reto1'),
    path('reto_2/', reto2, name='reto2'),
    path('reto_3/', reto3, name='reto3'),
]