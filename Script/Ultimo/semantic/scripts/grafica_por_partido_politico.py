import plotly.graph_objects as go
import networkx as nx
import pandas as pd
from scripts.network_similary_politics import relaciones_politicas_map


def lista_politicos(relaciones_politicas):
    id_politicos = 0
    nombres_politicos = []
    filtrado = []
    influencers = dict()
    influencers_sin_relaciones = []
    for influencer in relaciones_politicas:
        if len(relaciones_politicas[influencer]) == 0:
            influencers_sin_relaciones.append(influencer)
        else:
            politicos = list(dict.fromkeys(relaciones_politicas[influencer]))
            for politico in range(len(politicos)):
                if politicos[politico] == influencer:
                    id_influencer = politico
                    influencers[influencer]=[politico, id_politicos]
                filtrado.append([id_politicos, politicos[politico]])
                nombres_politicos.append(politicos[politico])
                id_politicos += 1

    for i in influencers_sin_relaciones:
        del relaciones_politicas[i]
    return relaciones_politicas, influencers, filtrado, nombres_politicos

def crear_posiciones_random(filtrado):
    G = nx.random_geometric_graph(300, 0.8)
    posicion = []
    i = len(filtrado)
    j = 0
    for edge in G.edges():
        x0, y0 = G.nodes[edge[1]]['pos']
        if j < i:
            posicion.append((x0, y0))
            j += 1
    return posicion

def igualar_posicion_repetidos(posicion, filtrado):
    persona = None
    for i in filtrado:
        persona = i[1]
        for j in filtrado:
            if persona == j[1]:
                if (i[0] != j[0]) and (i[0] < j[0]):
                    posicion[j[0]] = posicion[i[0]]
    return posicion

def dataframe(posicion, filtrado):
    df = pd.DataFrame(filtrado,columns=['id', 'politico'])
    df['posicion'] = posicion
    posiciones_todos = posicion
    return df

def posiciones_influencers(relaciones_politicas, influencers, posicion):
    for influencer in relaciones_politicas:
        politicos = list(dict.fromkeys(relaciones_politicas[influencer]))
        for influ in influencers:
            if influ == influencer:
                id_influencer = influencers[influ][1]
                posicion_influencer = posicion[id_influencer]
                influencers[influ].append(posicion_influencer)
    return influencers

def posiciones_politicos_relacionados(relaciones_politicas, influencers, posicion):
    cantidad = []
    cuenta = 0
    influenciadores = []
    for influencer in relaciones_politicas:
        influenciadores.append(influencer)
        destino = []
        politicos = list(dict.fromkeys(relaciones_politicas[influencer]))            
        for politico in range(len(politicos)):
            id_influencer = influencers[influencer][0]
            posicion_influencer = influencers[influencer][2]
            if politico == id_influencer:
                cantidad.append(len(politicos)-1)
                cuenta += 1
            else:
                cantidad.append(1)
                destino.append(posicion[cuenta])
                cuenta += 1
        influencers[influencer].append(destino)
    return influencers, cantidad, influenciadores

def contador_repeticiones_politicos(filtrado, influenciadores, cantidad, df):
    for p in filtrado:
        if influenciadores.count(p[1]) == 0:
            count = df['politico'].to_string(index=False).count(p[1])
            if count > 1:
                cantidad[p[0]] = count
    df['cantidad'] = cantidad
    return df, cantidad

def preparacion_grafica(relaciones_politicas, influencers, posicion):
    edge_x = []
    edge_y = []
    

    for influencer in relaciones_politicas:
        posicion_influencer = influencers[influencer][2]
        for edge in influencers[influencer][3]:
            x0, y0 = edge
            x1, y1 = posicion_influencer[0], posicion_influencer[1] 
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node in posicion:
            x, y = node
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))
    return edge_trace, node_trace

def labels_politicos(nombres_politicos, node_trace, cantidad):
    node_trace.marker.color = cantidad
    for i in range(len(cantidad)):
        nombres_politicos[i] = nombres_politicos[i] + " (" + str(cantidad[i]) + ")"
    node_trace.text = nombres_politicos
    return node_trace

def crear_figura(edge_trace, node_trace):
    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    #fig.show()
    return fig

def crear_network_map(politicos):
    relaciones_politicas = relaciones_politicas_map(politicos)
    relaciones_politicas, influencers, filtrado, nombres_politicos = lista_politicos(relaciones_politicas)
    posicion = crear_posiciones_random(filtrado)
    posicion = igualar_posicion_repetidos(posicion, filtrado)
    df = dataframe(posicion, filtrado)
    influencers = posiciones_influencers(relaciones_politicas, influencers, posicion)
    influencers, cantidad, influenciadores = posiciones_politicos_relacionados(relaciones_politicas, influencers, posicion)
    df, cantidad = contador_repeticiones_politicos(filtrado, influenciadores, cantidad, df)
    edge_trace, node_trace = preparacion_grafica(relaciones_politicas, influencers, posicion)
    node_trace = labels_politicos(nombres_politicos, node_trace, cantidad)
    fig = crear_figura(edge_trace, node_trace)
    return fig