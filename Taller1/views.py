from django.shortcuts import render
import paramiko
from json_response import JsonResponse
import time
import json
import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
from folium.plugins import HeatMap

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
    session.exec_command("hadoop fs -cat result22/part-00000")
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

def tabla(request):
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


    context = {
        'datos': datos,
        'imagen': base_map._repr_html_()
    }

    return render(request, 'taller1/reto_1.html', context)