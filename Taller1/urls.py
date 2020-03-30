from django.urls import path
from .views import reto1, reto2, reto3, retoA, retoB, retoC

urlpatterns = [
    path('reto_1/', reto1, name='reto1'),
    path('reto_2/', reto2, name='reto2'),
    path('reto_3/', reto3, name='reto3'),
    path('reto_a/', retoA, name='retoA'),
    path('reto_b/', retoB, name='retoB'),
    path('reto_c/', retoC, name='retoC'),
]