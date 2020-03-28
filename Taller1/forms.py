from django import forms
import os

CHOICES = (('1', 'Ejecutar en Hadoop'),('2', 'Consultar datos preprocesados'),)
CHOICES_DIA = (('0', 'Lunes'),('1', 'Martes'),('2', 'Miercoles'),('3', 'Jueves'),('4', 'Viernes'),('5', 'Sábado'),('6', 'Domingo'))
CHOICES_MES = (('01', 'Enero'),('02', 'Febrero'),('03', 'Marzo'),('04', 'Abril'),('05', 'Mayo'),('06', 'Junio'),('07', 'Julio'),('08', 'Agosto'),('09', 'Septiembre'),('10', 'Octubre'),('11', 'Noviembre'),('12', 'Diciembre'))

class buscadorReto1Form(forms.Form):
    seleccion = forms.ChoiceField(label="Selección", choices=CHOICES)
    horaInicio = forms.CharField(label='Hora inicio (hh:mm):',max_length=15, initial='00:00')
    horaFin = forms.CharField(label='Hora fin (hh:mm):',max_length=15, initial='02:00')

class buscadorReto2Form(forms.Form):
    seleccion = forms.ChoiceField(label="Selección", choices=CHOICES)
    dia = forms.ChoiceField(label="Día", choices=CHOICES_DIA)
    mes = forms.ChoiceField(label="Mes", choices=CHOICES_MES)

class buscadorReto3Form(forms.Form):
    seleccion = forms.ChoiceField(label="Selección", choices=CHOICES)
    horaInicio = forms.CharField(label='Hora inicio (hh:mm):',max_length=15, initial='07:00')
    horaFin = forms.CharField(label='Hora fin (hh:mm):',max_length=15, initial='09:00')
    dia = forms.ChoiceField(label="Día", choices=CHOICES_DIA)
    topN = forms.CharField(label='Top N:',max_length=2, initial='5')