from django import forms
import os

class buscadorReto1Form(forms.Form):
    horaInicio = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    horaFin = forms.TimeField(widget=forms.TimeInput(format='%HH:%MM'))