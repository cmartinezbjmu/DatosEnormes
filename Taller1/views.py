from django.shortcuts import render
import paramiko
from json_response import JsonResponse
import time
import json
import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
from folium.plugins import HeatMap
import plotly.graph_objects as go
import plotly.offline as opy

# Create your views here.

def conexionHadoop():
    sleeptime = 0.001
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect('172.24.99.72', username='bigdata03', password='big2020')
    ssh.connect('172.24.99.93', username='bigdata03', password='big2020')
    #bigdata03126108

    session = ssh.get_transport().open_session()
    # Forward local agent
    paramiko.agent.AgentRequestHandler(session)
    session.exec_command("hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_1.py -mapper 'python mapper_1.py' -input miniTaxis -output result13")
    while True:
        if session.exit_status_ready():
            break
        time.sleep(sleeptime)
    #stdin, stdout, stderr = ssh.exec_command("hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_1.py -mapper 'python mapper_1.py' -file /home/bigdata03/taller1/reducer.py -reducer 'python reducer.py' -input miniTaxis -output result06")
    session.close()
    ssh.close()
    #for line in stdout:
    #    print(line.strip('\n'))
    
def resultadoHadoop():
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
    session.exec_command("hadoop fs -cat result200/part-00000")
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
    datos = resultadoHadoop()
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
        'imagen': base_map._repr_html_()
    }

    return render(request, 'taller1/reto_1.html', context)

def reto2(request):
    datos = resultadoHadoop()
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
    fig.update_layout(title_text="Costo de los días lunes del mes enero (2009 - 2019)", barmode='group', xaxis_tickangle=0)
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