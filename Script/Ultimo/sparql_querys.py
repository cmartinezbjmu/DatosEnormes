from SPARQLWrapper import SPARQLWrapper, JSON

politicos = ["Sergio_Fajardo", "Álvaro_Uribe", "Armando_Benedetti", "Juan_Fernando_Cristo", "Luis_Fernando_Velasco",
            "Germán_Navas_Talero", "Angélica_Lozano", "Gustavo_Petro", "Roy_Barreras", "Gustavo_Bolívar",
            "María_José_Pizarro", "Jorge_Enrique_Robledo", "Iván_Duque_Márquez", "Claudia_López_Hernández",
            "Jorge_Iván_Ospina", "Daniel_Quintero"]
periodistas = ["Félix_de_Bedout", "Mábel_Lara", "Gilberto_Tobón_Sanín", "Yolanda_Ruiz", "Camila_Zuluaga", "Gonzalo_Guillén", "María_Jimena_Duzán", "Vicky_Dávila"]

def buscar_relaciones_politicas(politico):
    query = """PREFIX dbpedia-owl: <http://dbpedia.org/ontology/> \
                SELECT * WHERE { \
                ?name <http://dbpedia.org/ontology/party> ?party . \
                <http://es.dbpedia.org/resource/{}> <http://dbpedia.org/ontology/party> ?party . \
                ?name rdfs:label ?Nombre . \
            }""".format(politico)

    sparql = SPARQLWrapper("http://es.dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)

    result = sparql.query().convert()
    return result["results"]["bindings"]


#for politico in politicos:
p = []
partido = []
resultados = buscar_relaciones_politicas()
for resultado in resultados:
    #print(resultado)
    p.append(resultado["Nombre"]['value'])
    partido.append(resultado["party"]["value"].split("/")[4])
    #print(resultado["Nombre"]["value"])
    #print(resultado["party"]["value"].split("/")[4])

print(p)
#print(len(partido))

import plotly.express as px
fig = px.treemap(
    names = ["Polo_Democrático_Alternativo", "Movimiento_Progresistas"],
    parents = ["", "Polo_Democrático_Alternativo"]
)
#fig.show()

