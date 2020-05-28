import pandas as pd
import plotly.express as px
from SPARQLWrapper import SPARQLWrapper, JSON


def buscar_relaciones_politicas(politico):
    query = """PREFIX dbpedia-owl: <http://dbpedia.org/ontology/> \
                SELECT * WHERE { \
                ?name <http://dbpedia.org/ontology/party> ?party . \
                <http://es.dbpedia.org/resource/%s> <http://dbpedia.org/ontology/party> ?party . \
                ?name rdfs:label ?Nombre . \
            }""" % (politico)

    sparql = SPARQLWrapper("http://es.dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)

    result = sparql.query().convert()
    return result["results"]["bindings"]

def consulta_sparkql(politico):
    politicos = []
    partidos = []
    resultados = buscar_relaciones_politicas(politico)
    for resultado in resultados:
        politicos.append(resultado["Nombre"]['value'])
        partidos.append(resultado["party"]["value"].split("/")[4])
    return politicos, partidos

def crear_treemap(politicos, partidos, influencer):
    data = []
    for i in range(len(politicos)):
        data.append([politicos[i], partidos[i], 1])
    df = pd.DataFrame(data,columns=['politico', 'partidos', 'cantidad'])
    df["influencer"] = influencer
    fig = px.treemap(df, path=['influencer', 'partidos', 'politico'], values='cantidad')
    return fig

def crear_figura_treemap_network(politico):
    politico = politico.split('(')[0]
    politico = politico.strip()
    politico = politico.replace(' ', '_')
    politicos, partidos = consulta_sparkql(politico)
    fig = crear_treemap(politicos, partidos, politico)
    return fig