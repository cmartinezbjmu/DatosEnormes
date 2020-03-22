from django.shortcuts import render
import paramiko
from json_response import JsonResponse
import time

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
    session.exec_command("hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_1.py -mapper 'python mapper_1.py' -input miniTaxis -output result5")
    while True:
        if session.exit_status_ready():
            break
        time.sleep(sleeptime)
    #stdin, stdout, stderr = ssh.exec_command("hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_1.py -mapper 'python mapper_1.py' -file /home/bigdata03/taller1/reducer.py -reducer 'python reducer.py' -input miniTaxis -output result06")
    session.close()
    ssh.close()
    #for line in stdout:
    #    print(line.strip('\n'))
    
def resultadoHadoop(request):
    conexionHadoop()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('172.24.99.72', username='bigdata03', password='big2020')
    
    #ssh.connect('172.24.99.93', username='bigdata03', password='bigdata03126108')
    #hadoop_ejec = "hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_1.py -mapper 'python mapper_1.py' -file /home/bigdata03/taller1/reducer-1.py -reducer 'python reducer-1.py' -input miniTaxis -output result06 && hadoop fs -cat result06/part*"
    #stdin, stdout, stderr = ssh.exec_command("hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -file /home/bigdata03/taller1/mapper_1.py -mapper 'python mapper_1.py' -file /home/bigdata03/taller1/reducer.py -reducer 'python reducer.py' -input miniTaxis -output result06")
    stdin, stdout, stderr = ssh.exec_command("hadoop fs -cat result5/part*")
    #stdin, stdout, stderr = ssh.exec_command("hadoop fs -ls")
    resultado = []
    for line in stdout:
        print(line.strip('\n'))
    ssh.close()
    return JsonResponse({'Resultado': 'ok'})