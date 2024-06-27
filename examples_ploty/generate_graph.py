import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go

# Generar una base de datos aleatoria
np.random.seed(42)
n_nodes = 10
nodes = [f'Node_{i}' for i in range(n_nodes)]
edges = [(np.random.choice(nodes), np.random.choice(nodes)) for _ in range(n_nodes * 2)]

# Crear un DataFrame con los nodos y aristas
df_nodes = pd.DataFrame(nodes, columns=['Node'])
df_edges = pd.DataFrame(edges, columns=['Source', 'Target'])

# Crear el grafo
G = nx.from_pandas_edgelist(df_edges, 'Source', 'Target')

# Añadir atributos a los nodos
for node in G.nodes():
    G.nodes[node]['group'] = np.random.randint(1, 4)

# Generar las posiciones de los nodos
pos = nx.spring_layout(G)

# Crear el trazo de las aristas
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

# Crear el trazo de los nodos
node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers+text',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=10,
        color=[],
        colorbar=dict(
            thickness=15,
            title='Grupo',
            xanchor='left',
            titleside='right'
        )
    )
)

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += [x]
    node_trace['y'] += [y]

    node_info = f'ID: {node}<br>Grupo: {G.nodes[node]["group"]}'
    node_trace['text'] += [node_info]
    node_trace['marker']['color'] += [G.nodes[node]['group']]

# Crear la figura
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<br>Grafo Aleatorio con Plotly y NetworkX',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="Python code by Plotly",
                        showarrow=False,
                        xref="paper", yref="paper")],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.show()
