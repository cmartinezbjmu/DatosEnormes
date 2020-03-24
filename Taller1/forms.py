from django import forms
import os

class buscadorReto1Form(forms.Form):
    CHOICES = (('1', 'Correr en Hadoop'),('2', 'Consultar datos preprocesados'),)
    seleccion = forms.ChoiceField(label="Selección", choices=CHOICES)
    horaInicio = forms.CharField(label='Hora inicio:',max_length=15)
    horaFin = forms.CharField(label='Hora fin:',max_length=15)
