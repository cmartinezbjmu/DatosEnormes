from django.shortcuts import render
import paramiko
from json_response import JsonResponse
import time
import json
import plotly as py
import plotly.graph_objs as go
import plotly.offline as opy
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

# Create your views here.

def conexionHadoop():
    sleeptime = 0.001
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect('172.24.99.72', username='bigdata03', password='big2020')
    ssh.connect('172.24.99.93', username='bigdata03', password='bigdata03126108')

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
    
    ssh.connect('172.24.99.93', username='bigdata03', password='bigdata03126108')
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
    f = open("Script/mapReduce/Reuters/taxis/taxi_zone_lookup.csv")	
    destino = None	
    for ciudad in f.readlines():	
        if (idLugar in ciudad):	
            destino = ciudad.split(';')[1]	
            break
    return destino


def tabla(request):
    datos = resultadoHadoop()
    datos = json.loads(datos)

    for llave, valor in datos.items():
        datos[llave] = '{} ({})'.format(decodificarLugar(valor.split(',')[0]).replace('\n', ''), valor.split(',')[1])
    
    data = dict (
    type = 'choropleth',
    locations = ['NV','CA','NY'],
    locationmode='USA-states',
    z=[10,20,30])

    lyt = dict(geo=dict(scope='usa'))
    map = go.Figure(data=[data], layout = lyt)
    imagen = opy.plot(map, auto_open=False, output_type='div')

    fp = "Script/mapReduce/Reuters/taxis/taxi_zones/taxi_zones.shp"
    map_df = gpd.read_file(fp)
    print(map_df.head())
    context = {
        'datos': datos,
        #'imagen': map_df
    }

    return render(request, 'taller1/reto_1.html', context)
