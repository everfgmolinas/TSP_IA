# importacion de librerias para construir la gui en el navegador
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np

import plotly.express as px


# estilos que serán utilizados
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# aqui creamos una instancia de la aplicación para ir trabajando
app = dash.Dash(
    __name__,
    # indicamos el path de donde consultar los estilos
    external_stylesheets=external_stylesheets,
)

# aqui le damos un título a la aplicación
app.title = 'TSP-Resolucion'

# definicion de funciones útiles


# título de la aplicacion
def titulo():
    return html.H3(
        'Problema del vendedor viajero',
        style={
            'textAlign': 'center'
        }
    )


# obtiene los parametros de entrada para generar los gráficos
def parametros():
    return html.Div(
        children=[
            html.P(
                'Ingrese el número de nodos'
            ),
            dcc.Input(
                id='entrada-nodo',
                value=20,
                type='number'
            ),
            html.Button(
                'aceptar',
                id='submit-nodos',
                className='btn btn-primary',
                n_clicks=0
            ),
        ]
    )



# aqui definimos el diseño de la aplicacion
app.layout = html.Div(
    children=[
        # le daremos un título general al cuerpo de la aplicacion
        titulo(),
        html.Br(),
        # aqui solicitaremos los parámetros para dar una solucion al problema
        parametros(),
        html.Br(),
        # tabs que contendran cada una de las soluciones
        dcc.Tabs(
            id='tabs',
            # valor por defecto
            value='tab-1',
            children=[
                dcc.Tab(label='Solución 1', value='tab-1'),
                dcc.Tab(label='Solución 2', value='tab-2'),
                dcc.Tab(label='Solución 3', value='tab-3'),
                dcc.Tab(label='Comparaciones', value='tab-4'),
            ]
        ),
        html.Br(),
        html.Div(id='contenido-tab')
    ]
)


# definimos el callback que se encarga de vincular el tab con cada contenido
@app.callback(
    Output(component_id='contenido-tab', component_property='children'),
    [
        Input(component_id='tabs', component_property='value'),
        Input(component_id='submit-nodos', component_property='n_clicks')
    ],
    State(component_id='entrada-nodo', component_property='value')
)


# funcion encargada de renderizar el tab seleccionado
def renderizacion(tab, n_clicks, nodos):

    # el par (nodos,2) da las dimensiones del array que generará numpy (fila,col)
    puntosAleatorios = pd.DataFrame(
        np.random.randint(0, 50, (nodos, 2)),
        columns=['X', 'Y']
    )
    # la columna marcado funciona para ver si el nodo en cuestion ya fue visitado
    grafo = puntosAleatorios.assign(marcado=False)

    fig = px.scatter(puntosAleatorios, x="X", y="Y", title='Nodos del grafo')

    if tab == 'tab-1':
        return html.Div(
            children=[
                html.H5('Tab-1'),
                html.Br(),
                dcc.Graph(
                    id='grafo-inicial',
                    figure=fig,
                )
            ]
        )
    elif tab == 'tab-2':
        return html.Div(
            children=[
                html.H5('Tab-2')
            ]
        )
    elif tab == 'tab-3':
        return html.Div(
            children=[
                html.H5('Tab-3')
            ]
        )
    elif tab == 'tab-4':
        return html.Div(
            children=[
                html.H5('Tab-4')
            ]
        )


# con esto podemos levantar la aplicación en el navegador
if __name__ == "__main__":
    app.run_server(debug=True)