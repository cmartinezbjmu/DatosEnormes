from django.urls import path
from .views import tabla

urlpatterns = [
    path('reto_1/', tabla, name='tabla'),
]