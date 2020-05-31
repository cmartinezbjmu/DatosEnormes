from sematch.semantic.similarity import EntitySimilarity
import plotly.express as px
entity_sim = EntitySimilarity()

#politicos = ['Sergio_Fajardo', 'Álvaro_Uribe', 'Armando_Benedetti']#, 'Vicky_Dávila', 'Luis_Fernando_Velasco']
#similitud = entity_sim.similarity('http://dbpedia.org/resource/Álvaro_Uribe',
#                            'http://dbpedia.org/resource/Sergio_Fajardo')
#print(similitud)     

def similitud_influencers():

    politicos = ['Sergio_Fajardo', 'Álvaro_Uribe', 'Armando_Benedetti', 'Juan_Fernando_Cristo', 'Luis_Fernando_Velasco',
                'Germán_Navas_Talero', 'Angélica_Lozano', 'Gustavo_Petro', 'Roy_Barreras', 'Gustavo_Bolívar',
                'María_José_Pizarro', 'Jorge_Enrique_Robledo', 'Iván_Duque_Márquez', 'Claudia_López_Hernández',
                'Jorge_Iván_Ospina', 'Daniel_Quintero', 'Félix_de_Bedout', 'Mábel_Lara', 'Gilberto_Tobón_Sanín', 
                'Yolanda_Ruiz', 'Camila_Zuluaga', 'Gonzalo_Guillén', 'María_Jimena_Duzán', 'Vicky_Dávila']

    #politicos = ['Sergio_Fajardo', 'Álvaro_Uribe']

    similitudes = []
    for persona in politicos:
        similitud = []
        for i in range(len(politicos)):            
            similitud.append(entity_sim.similarity('http://dbpedia.org/resource/{}'.format(persona),
                                            'http://dbpedia.org/resource/{}'.format(politicos[i])))
        similitudes.append(similitud)
    
    data=similitudes
    fig = px.imshow(data,
                    labels=dict(x="Influencers", y="Influencers", color="Similitud"),
                    x=politicos,
                    y=politicos
                )
    fig.update_xaxes(side="top")
    return fig
