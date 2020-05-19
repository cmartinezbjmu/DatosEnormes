from sematch.semantic.similarity import EntitySimilarity
entity_sim = EntitySimilarity()


politicos = ['Sergio_Fajardo', 'Álvaro_Uribe', 'Armando_Benedetti', 'Juan_Fernando_Cristo', 'Luis_Fernando_Velasco']
            #'Germán_Navas_Talero', 'Angélica_Lozano', 'Gustavo_Petro', 'Roy_Barreras', 'Gustavo_Bolívar',
            #'María_José_Pizarro', 'Jorge_Enrique_Robledo', 'Iván_Duque_Márquez', 'Claudia_López_Hernández',
            #'Jorge_Iván_Ospina', 'Daniel_Quintero', 'Félix_de_Bedout', 'Mábel_Lara', 'Gilberto_Tobón_Sanín', 
            #'Yolanda_Ruiz', 'Camila_Zuluaga', 'Gonzalo_Guillén', 'María_Jimena_Duzán', 'Vicky_Dávila']


similitud = entity_sim.similarity('https://query.wikidata.org/sparql/Q187413',
                            'https://query.wikidata.org/sparql/Q17478000')
print(similitud)                            

#similitudes = []
#for persona in politicos:
#    for i in range(len(politicos)):
#        if (i > politicos.index(persona)):
#            #print(persona, politicos[i])
#            #similitud = entity_sim.similarity('http://dbpedia.org/resource/{}'.format(persona),
#            #                            'http://dbpedia.org/resource/{}'.format(politicos[i]))                                      
#            #if similitud != 0.0:
#            similitudes.append([persona, politicos[i], similitud])



#print(similitudes)                        