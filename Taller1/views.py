from .forms import buscadorReto1Form, buscadorReto2Form, buscadorReto3Form
from django.shortcuts import render
import paramiko
from json_response import JsonResponse
import time
from datetime import datetime
import json
import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
from folium.plugins import HeatMap
import plotly.graph_objects as go
import plotly.offline as opy

# Create your views here.

def conexionHadoop(reto, arg1, arg2, arg3=None, arg4=None):      
    print('LLego conec')
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    sleeptime = 0.001
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect('172.24.99.72', username='bigdata03', password='big2020')
    ssh.connect('172.24.99.93', username='bigdata03', password='big2020')
    #bigdata03126108

    session = ssh.get_transport().open_session()
    # Forward local agent
    paramiko.agent.AgentRequestHandler(session)
    if reto == 1:
        arg1 = arg1.split(':')
        arg2 = arg2.split(':')
        session.exec_command("hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_1.py -mapper 'python mapper_1.py {0} {1} {2} {3}' -file /home/bigdata03/taller1/reducer-1.py -reducer 'python reducer-1.py' -input miniTaxis -output result_{4}_{5}".format(arg1[0], arg1[1], arg2[0], arg2[1], reto, timestamp))
    if reto == 2:
        arg1 = str(arg1)
        arg2 = str(arg2)
        session.exec_command("hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_2.py -mapper 'python mapper_2.py {0} {1}' -file /home/bigdata03/taller1/reducer-2.py -reducer 'python reducer-2.py' -input miniTaxis -output result_{2}_{3}".format(arg1, arg2, reto, timestamp))
    if reto == 3:
        print('entro eje R3')
        arg1 = arg1.split(':')
        arg2 = arg2.split(':')
        arg3 = str(arg3)
        arg4 = str(arg4)
        var = "hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_3.py -mapper 'python mapper_3.py {0} {1} {2} {3} {4}' -file /home/bigdata03/taller1/reducer-3.py -reducer 'python reducer-3.py {5}' -input miniTaxis -output result_{6}_{7}".format(arg1[0], arg1[1], arg2[0], arg2[1], arg3, arg4, reto, timestamp)
        print(var)
        session.exec_command("hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_3.py -mapper 'python mapper_3.py {0} {1} {2} {3} {4}' -file /home/bigdata03/taller1/reducer-3.py -reducer 'python reducer-3.py {5}' -input miniTaxis -output result_{6}_{7}".format(arg1[0], arg1[1], arg2[0], arg2[1], arg3, arg4, reto, timestamp))
    while True:
        if session.exit_status_ready():
            break
        time.sleep(sleeptime)
    #stdin, stdout, stderr = ssh.exec_command("hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_1.py -mapper 'python mapper_1.py' -file /home/bigdata03/taller1/reducer.py -reducer 'python reducer.py' -input miniTaxis -output result06")
    #session.close()
    ssh.close()
    #for line in stdout:
    #    print(line.strip('\n'))
    return ('result_'+str(reto)+'_'+str(timestamp))
    
def resultadoHadoop(nombre_archivo):
    #conexionHadoop()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect('172.24.99.72', username='bigdata03', password='big2020')
    
    ssh.connect('172.24.99.93', username='bigdata03', password='big2020')
    #hadoop_ejec = "hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_1.py -mapper 'python mapper_1.py' -file /home/bigdata03/taller1/reducer-1.py -reducer 'python reducer-1.py' -input miniTaxis -output result06 && hadoop fs -cat result06/part*"
    #stdin, stdout, stderr = ssh.exec_command("hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_1.py -mapper 'python mapper_1.py' -file /home/bigdata03/taller1/reducer.py -reducer 'python reducer.py' -input miniTaxis -output result06")

    session = ssh.get_transport().open_session()
    # Forward local agent
    paramiko.agent.AgentRequestHandler(session)

    session.exec_command("hadoop fs -cat "+nombre_archivo+"/part-00000")       
    #stdin, stdout, stderr = ssh.exec_command("hadoop fs -ls result13")
    sleeptime = 0.001
    outdata = ''
    
    while True:
        while session.recv_ready():         
            outdata += session.recv(1000).decode('utf-8')
        if session.exit_status_ready():
            break
        time.sleep(sleeptime)

    ssh.close()
    
    outdata = outdata.replace(r'\t', '')
    outdata = outdata.replace("'", '"')
    return outdata

def decodificarLugar(idLugar):
    f = open("Script/mapReduce/Reuters/taxis/taxi_zone.csv")	
    destino = None	
    for ciudad in f.readlines():	
        if (idLugar in ciudad):	
            destino = ciudad.split(',')[2]
            break
    return destino

def decodificarLugar_df(idLugar):
    f = open("Script/mapReduce/Reuters/taxis/taxi_zone.csv")	
    destino = None	
    for ciudad in f.readlines():	
        if (idLugar in ciudad):	
            latitud, longitud = ciudad.split(',')[6], ciudad.split(',')[7]
            break
    return latitud, longitud

def generateBaseMap(default_location=[40.693943, -73.985880], default_zoom_start=11):
    base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map

def reto1(request):
    form = buscadorReto1Form(request.POST or None)
    if form.is_valid():
        seleccion = form.cleaned_data['seleccion']
        hora_ini = form.cleaned_data['horaInicio']
        hora_fin = form.cleaned_data['horaFin']

        if seleccion == '1':
            nombre_archivo = conexionHadoop(1, hora_ini, hora_fin)
            datos = resultadoHadoop(nombre_archivo)
        else:
            hora_ini = '00:00'
            hora_fin = '02:00'
            nombre_archivo = 'result22'
            datos = resultadoHadoop(nombre_archivo)
        datos = json.loads(datos)
        datos_mapa = datos.copy()
        for llave, valor in datos.items():
            datos[llave] = '{} ({})'.format(decodificarLugar(valor.split(',')[0]).replace('\n', ''), valor.split(',')[1])
            
        diccionario = dict()
        lat = []
        log = []
        amout = []
        #print(datos_mapa)
        for llave, valor in datos_mapa.items():
            latitud, longitud = decodificarLugar_df(valor.split(',')[0])
            lat.append(float(latitud))
            log.append(float(longitud.replace('\n', '')))
            amout.append(int(valor.split(',')[1]))

        diccionario['latitud'] = lat
        diccionario['longitud'] = log
        diccionario['valor'] = amout
        datos_df = pd.DataFrame(diccionario)
        base_map = generateBaseMap()
        HeatMap(data=datos_df[['latitud', 'longitud', 'valor']].groupby(['latitud', 'longitud']).sum().reset_index().values.tolist(), radius=8, max_zoom=10).add_to(base_map)
        base_map.add_child(folium.ClickForMarker(popup='valor'))

        context = {
            'datos': datos,
            'imagen': base_map._repr_html_(),
            'hora_ini': hora_ini,
            'hora_fin': hora_fin,
        }

        return render(request, 'taller1/reto_1.html', context)
    context = {
        'form': form,        
    }

    return render(request, 'taller1/buscadores/reto_1_search.html', context)

def reto2(request):
    form = buscadorReto2Form(request.POST or None)
    if form.is_valid():

        seleccion = form.cleaned_data['seleccion']
        dia = form.cleaned_data['dia']
        mes = form.cleaned_data['mes']

        if seleccion == '1':
            nombre_archivo = conexionHadoop(2, dia, mes)
            datos = resultadoHadoop(nombre_archivo)
        else:
            dia = '0'
            mes = '01'
            nombre_archivo = 'test02'
            datos = resultadoHadoop(nombre_archivo)
        
        dias = {'0': 'Lunes', '1': 'Martes', '2': 'Miercoles', '3': 'Jueves', '4': 'Viernes', '5': 'Sábado', '6': 'Domingo'}
        meses = {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'}
        datos = json.loads(datos)
        datos_yellow = []
        datos_green = []
        keys = list(datos)

        if 'green' in keys:
            datos_green = datos['green'].split(',')
            green_prom = round(float(datos_green[2]), 2)
        else:
            datos_green = ['NA', 'NA', 'NA', 'NA']
            green_prom = 'NA'
        if 'yellow' in keys:
            datos_yellow = datos['yellow'].split(',')
            yellow_prom = round(float(datos_yellow[2]), 2)
        else:
            datos_yellow = ['NA', 'NA', 'NA', 'NA']
            yellow_prom = 'NA'
        
        # Grafica
        precios = ['Precio max', 'Precio min', 'Precio prom']
        
        dia_nom = dias[dia]
        mes_nom = meses[mes]
        fig = go.Figure()
        if 'yellow' in keys:
            fig.add_trace(go.Bar(
                x=precios,
                y=[float(datos_yellow[0]), float(datos_yellow[1]), round(float(datos_yellow[2]), 2)],
                name='Yellow (' + datos_yellow[3] + ')',
                marker_color='yellow'
            ))
        if 'green' in keys:
            fig.add_trace(go.Bar(
                x=precios,
                y=[float(datos_green[0]), float(datos_green[1]), round(float(datos_green[2]), 2)],
                name='Green (' + datos_green[3] + ')',
                marker_color='green',
            ))

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Precio máximo, mínimo y promedio de los viajes en los días {} de {} entre (2009 - 2019)".format(dia_nom, mes_nom), barmode='group', xaxis_tickangle=0)
        div = opy.plot(fig, auto_open=False, output_type='div')

        context = {
            'green_max': datos_green[0],
            'green_min': datos_green[1],
            'green_prom': green_prom,
            'green_cant': datos_green[3],
            'yellow_max': datos_yellow[0],
            'yellow_min': datos_yellow[1],
            'yellow_prom': yellow_prom,
            'yellow_cant': datos_yellow[3],
            'imagen': div
        }

        return render(request, 'taller1/reto_2.html', context)
    
    context = {
        'form': form,        
    }

    return render(request, 'taller1/buscadores/reto_2_search.html', context)

def reto3(request):
    form = buscadorReto3Form(request.POST or None)
    if form.is_valid():
        seleccion = form.cleaned_data['seleccion']
        hora_ini = form.cleaned_data['horaInicio']
        hora_fin = form.cleaned_data['horaFin']
        dia = form.cleaned_data['dia']
        topN = form.cleaned_data['topN']

        if seleccion == '1':
            nombre_archivo = conexionHadoop(3, hora_ini, hora_fin, dia, topN)
            print(nombre_archivo)
            datos = resultadoHadoop(nombre_archivo)
        else:
            # Preprocesados
            hora_ini = '07:00'
            hora_fin = '09:00'
            topN = '3'
            dia = '2'
            nombre_archivo = 'test03_7-9-2-3'
            datos = resultadoHadoop(nombre_archivo)
        
        salida = dict()
        lugares = []
        valores = []
        datos = datos.strip()
        datos = datos.replace(r'\t', '')
        datos = datos.split('\n')
        for lugar in datos:
            lugares.append(decodificarLugar(lugar.split(',')[0]))
            valores.append(lugar.split(',', 1)[0])

        cant = len(lugares)
        s = 0
        for valor in valores:
            salida[lugares[s]] = json.loads(valor)
            s = s + 1
            if s == cant:
                break
        salida = {'Lincoln Square East': {10: 5, 5: 80}, 'Lenox Hill East': {7: 9, 2: 150, 1: 50}}
        
        # Grafica
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        valor_in = [0,0,0,0,0,0,0,0,0,0,0,0]
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=meses,
            y=valor_in,
            name='',
        ))
        for lugar, valores in salida.items():
            clave = []
            valor = []
            mes = []
            for k, v in sorted(valores.items()):
                valores[int(k)] = valores.pop(k)
            for k, v in sorted(valores.items()):
                clave.append(k)
                valor.append(v)
            for i in clave:
                #print(meses[i-1])
                mes.append(meses[i-1])
            fig.add_trace(go.Bar(
                x=mes,
                y=valor,
                name=lugar,
            ))

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Top {} de mayor demanda en el días {} durante la franja horaria {} {}".format(topN, dia, hora_ini, hora_fin), barmode='group', xaxis_tickangle=0)
        div = opy.plot(fig, auto_open=False, output_type='div')

        context = {
            'datos': salida,
            'imagen': div,
        }

        return render(request, 'taller1/reto_3.html', context)

    context = {
        'form': form,        
    }

    return render(request, 'taller1/buscadores/reto_3_search.html', context)


def retoA(request):
    datos = dict()
    lugares = ['Bronx', 'Brooklyn', 'EWR', 'Manhattan', 'Queens', 'Staten', 'Island', 'Unknown']

    for i in range(1,8):
        nombre_archivo = 'resultRa' + str(i)
        datos[i] = resultadoHadoop(nombre_archivo).replace('\n', '').replace('\t', '').split(' ')
        if len(datos[i]) > 2:
            datos[i][1] = round(float(datos[i][1]), 2)
            datos[i][2] = round(float(datos[i][2]), 2)
    
    # Grafica
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Precio pico', 'Precio promedio'],
        y=[datos[2][1], datos[2][2]],
        name='Brooklyn',
    ))

    fig.add_trace(go.Bar(
        x=['Precio pico', 'Precio promedio'],
        y=[datos[4][1], datos[4][2]],
        name='Manhattan',
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(title_text="Comparación de precios en horas pico y precio promedio en las diferentes zonas", barmode='group', xaxis_tickangle=0)
    div = opy.plot(fig, auto_open=False, output_type='div')



    context = {
        'datos': datos,
        'imagen': div,
    }
    return render(request, 'taller1/reto_a.html', context)

def retoB(request):
    nombre_archivo = 'resultRb'
    datos = resultadoHadoop(nombre_archivo)
    datos = datos.replace('\n', '').replace('\t', '').split(' ')
    datos = (datos[2].replace('[', '')+datos[3].replace(']', '')).split(',')    
    datos[0] = float(datos[0])
    datos[1] = float(datos[1])

    labels = ['Rutas tipicas','Rutas diferentes']
    values = [sum(datos),1-sum(datos)]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    div = opy.plot(fig, auto_open=False, output_type='div')

    context = {
        'imagen': div,
    }
    return render(request, 'taller1/reto_b.html', context)

def retoC(request):
    nombre_archivo = 'resultRc'
    datos = resultadoHadoop(nombre_archivo)
    datos = datos.replace('\n', '').replace('\t', '').split(' ')
    datos[0] = float(datos[0])
    datos[1] = float(datos[1])

    labels = ['Intrazona','Interzona']
    values = [datos[0],datos[1]]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    div = opy.plot(fig, auto_open=False, output_type='div')

    context = {
        'imagen': div,
    }
    return render(request, 'taller1/reto_c.html', context)