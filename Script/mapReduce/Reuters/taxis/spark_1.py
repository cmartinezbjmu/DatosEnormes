#!/usr/bin/env python

from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql import Row
import datetime
from pyspark.sql import functions as F
from pyspark.sql.utils import AnalysisException

sc = SparkContext('local')
spark = SparkSession(sc)
hora_in, hora_fin = '04:30:00', '05:00:00'
query1 = "SELECT hora,DOLocationID FROM taxis WHERE hora BETWEEN '%s' AND '%s'" % (hora_in, hora_fin)
query2 = "SELECT hora,dropoff_longitude,dropoff_latitude FROM taxis WHERE hora BETWEEN '%s' AND '%s'" % (hora_in, hora_fin)
df = spark.sparkContext
df = spark.read.csv("hdfs:///user/bigdata03/taxis/taller1.tar.bz2", header=True)

split_col = F.split(df['tpep_pickup_datetime'], ' ')
df = df.withColumn('hora', split_col.getItem(1))

df.createOrReplaceTempView("taxis")
sqlDF = spark.sql(query1)
# Extrae las horas
horas = sqlDF.rdd.flatMap(lambda row: row).map(lambda lugar: lugar, 1)..reduceByKey(lambda a, b: a + b)
horas.saveAsTextFile("hdfs:///user/bigdata03/taxis/result")
#    .map(lambda row: str(row).split()[1])
#    .map(lambda row: row.split(':')[0])\
#    .filter(lambda row: (int(row) >= franja_horaria[0]))\
#    .filter(lambda row: (int(row) <= franja_horaria[1]))


#print horas.take(15)

