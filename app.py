# importacion de librerias para construir la gui en el navegador
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_daq as daq

import pandas as pd
import numpy as np
import time

import plotly.express as px

import Backtracking
import Opt
import Vegas


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


def distancia( punto1, punto2):
    return np.sqrt(np.power(punto1[0]-punto2[0],2) + np.power(punto1[1]-punto2[1],2))

puntosAleatorios = pd.DataFrame(
    np.random.randint(0, 50, (5, 2)),
    columns=['X', 'Y']
)

inicio_all = np.random.randint(0, 5 - 1)

def distancia_total(dataframe):
    sum_distancia = 0
    for i in range(len(dataframe)-1):
        sum_distancia += distancia(dataframe.iloc[i], dataframe.iloc[i+1])

    return sum_distancia


# obtiene los parametros de entrada para generar los gráficos
def parametros():
    return html.Div(
        children=[
            html.P(
                'Ingrese el número de nodos'
            ),
            dcc.Input(
                id='entrada-nodo',
                value=5,
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
        html.Div(id='header')
    ]
)


@app.callback(
    Output(component_id='header', component_property='children'),
    Input(component_id='submit-nodos', component_property='n_clicks'),
    State(component_id='entrada-nodo', component_property='value')
)

def firstRender(n_clicks, nodos):
    global puntosAleatorios
    puntosAleatorios = pd.DataFrame(
        np.random.randint(0, 50, (nodos, 2)),
        columns=['X', 'Y']
    )
    global inicio_all
    inicio_all = np.random.randint(0, nodos - 1)
    return html.Div(
        children=[
            # tabs que contendran cada una de las soluciones
            dcc.Tabs(
                id='tabs',
                # valor por defecto
                value='tab-1',
                children=[
                    dcc.Tab(label='OPT', value='tab-1'),
                    dcc.Tab(label='Backtracking', value='tab-2'),
                    dcc.Tab(label='Las Vegas', value='tab-3'),
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
    ],

)


# funcion encargada de renderizar el tab seleccionado
def renderizacion(tab):

    nodos = puntosAleatorios.shape[0]

    if tab == 'tab-2':
        # instancia de solucion del método backtracking
        grafo_back = Backtracking.Backtracking(puntosAleatorios)
        # generacion de número aleatorio que representa al índice del dataframe que se utilizara
        inicio = inicio_all
        # se marca el inicio del algoritmo
        tiempoInicio = time.time()
        solucion_back, expandidos = grafo_back.backtracking(grafo_back.dato, inicio)
        # se marca el inicio del algoritmo
        tiempoFinal = time.time()
        fig_back = []
        print("TOTAL")
        print(solucion_back)
        print("PARCIALES")
        for i in range(0, len(solucion_back)-1):
            print(solucion_back['ruta'][i])
            fig_back.append(px.line(solucion_back['ruta'][i], x='X', y='Y', title='Gráfico del camino solución', markers=True))
            return [

                html.Div(
                children=[
                    html.Div(
                        style={'display': 'flex', 'flex-direction': 'row'},
                        children=[
                            html.Div(
                                children=[
                                    html.H5('Camino solución'),
                                    dash_table.DataTable(
                                        solucion_back['ruta'][i].to_dict('records'),
                                        [{"name": row, 'id': row} for row in solucion_back['ruta'][i].columns],
                                        style_header={
                                            'backgroundColor': 'white',
                                            'fontWeight': 'bold'
                                        },
                                    ),
                                ],
                                style={
                                    "width": 200,
                                    'margin-left': 100,
                                    'margin-right': 100
                                }
                            ),
                            html.Div(
                                children=[
                                    html.H5('Grafo final'),
                                    dash_table.DataTable(solucion_back['ruta'][i].to_dict('records'),
                                                         [{"name": row, 'id': row} for row in
                                                          solucion_back['ruta'][i].columns]),
                                ],
                                style={
                                    "width": 300,
                                    'margin-left': 100,
                                    'margin-right': 100
                                }
                            ),
                            html.Div(
                                id="card-1",
                                children=[
                                    html.H5("Tiempo de ejecución (s)"),
                                    daq.LEDDisplay(
                                        id="operator-led",
                                        value=tiempoFinal - tiempoInicio,
                                        color="black",
                                        size=20
                                    ),
                                ],
                                style={
                                    'margin-left': 100,
                                    'margin-right': 100
                                }
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    dcc.Graph(
                                        id='grafo-camino',
                                        figure=fig_back[i],
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ) for i in range(0, len(solucion_back)-1)]
    elif tab == 'tab-1':
        # instancia de solucion del método backtracking
        grafo_opt = Opt.Opt(puntosAleatorios)
        # generacion de número aleatorio que representa al índice del dataframe que se utilizara
        inicio = inicio_all
        # se marca el inicio del algoritmo
        tiempoInicio = time.time()
        solucion_opt = grafo_opt.ruta2Optima(grafo_opt.dato, inicio)
        print("SOLUCION OPT")
        print(solucion_opt)
        # se marca el inicio del algoritmo
        tiempoFinal = time.time()
        fig_opt = px.line(solucion_opt['ruta'], x='X', y='Y', title='Gráfico del camino solución', markers=True)
        return html.Div(
            children=[
                html.Div(
                    style={'display': 'flex', 'flex-direction': 'row'},
                    children=[
                        html.Div(
                            children=[
                                html.H5('Camino solución'),
                                dash_table.DataTable(
                                    solucion_opt['ruta'].to_dict('records'),
                                    [{"name": row, 'id': row} for row in solucion_opt['ruta'].columns],
                                    style_header={
                                        'backgroundColor': 'white',
                                        'fontWeight': 'bold'
                                    },
                                ),
                            ],
                            style={
                                "width": 200,
                                'margin-left': 100,
                                'margin-right': 100
                            }
                        ),
                        html.Div(
                            children=[
                                html.H5('Grafo final'),
                                dash_table.DataTable(solucion_opt['ruta'].to_dict('records'),
                                                     [{"name": row, 'id': row} for row in solucion_opt['ruta'].columns]),
                            ],
                            style={
                                "width": 300,
                                'margin-left': 100,
                                'margin-right': 100
                            }
                        ),
                        html.Div(
                            id="card-1",
                            children=[
                                html.H5("Tiempo de ejecución (s)"),
                                daq.LEDDisplay(
                                    id="operator-led",
                                    value=tiempoFinal-tiempoInicio,
                                    color="black",
                                    size=20
                                ),
                            ],
                            style={
                                'margin-left': 100,
                                'margin-right': 100
                            }
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id='grafo-camino',
                                    figure=fig_opt,
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
    elif tab == 'tab-3':
        # creamos una instancia del objeto que contendrá la solución
        grafo = Vegas.Vegas(puntosAleatorios)
        # generacion de número aleatorio que representa al índice del dataframe que se utilizara
        indiceAleatorio = inicio_all
        # se marca el inicio del algoritmo
        tiempoInicio = time.time()
        # llamamos a nuestra funcion recursiva que resolverá el problema por el método de Las Vegas
        grafo.vegas(tiempoInicio, grafo.dato['X'][indiceAleatorio], grafo.dato['Y'][indiceAleatorio], 0)
        # tiempo final
        tiempoFinal = time.time()
        # traemos el dataframe generado que renderizaremos
        df = grafo.dato
        # traemos el camino generado
        camino = grafo.caminoSolucion
        aux = pd.DataFrame(columns=['X', 'Y'])
        aux = aux.append({'X': grafo.caminoSolucion['X'][0], 'Y': grafo.caminoSolucion['Y'][0]}, ignore_index=True)
        print("AUX")
        print(aux)
        camino = pd.concat([camino, aux], axis=0)
        print("CAMINO")
        print(camino)
        fig = px.line(camino, x='X', y='Y', title='Gráfico del camino solución', markers=True)

        return html.Div(
            children=[
                html.Div(
                    style={'display': 'flex', 'flex-direction': 'row'},
                    children=[
                        html.Div(
                            children=[
                                html.H5('Camino solución'),
                                dash_table.DataTable(
                                    camino.to_dict('records'),
                                    [{"name": row, 'id': row} for row in camino.columns],
                                    style_header={
                                        'backgroundColor': 'white',
                                        'fontWeight': 'bold'
                                    },
                                ),
                            ],
                            style={
                                "width": 200,
                                'margin-left': 100,
                                'margin-right': 100
                            }
                        ),
                        html.Div(
                            children=[
                                html.H5('Grafo final'),
                                dash_table.DataTable(df.to_dict('records'),
                                                     [{"name": row, 'id': row} for row in df.columns]),
                            ],
                            style={
                                "width": 300,
                                'margin-left': 100,
                                'margin-right': 100
                            }
                        ),
                        html.Div(
                            id="card-1",
                            children=[
                                html.H5("Tiempo de ejecución (s)"),
                                daq.LEDDisplay(
                                    id="operator-led",
                                    value=tiempoFinal-tiempoInicio,
                                    color="black",
                                    size=20
                                ),
                            ],
                            style={
                                'margin-left': 100,
                                'margin-right': 100
                            }
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id='grafo-camino',
                                    figure=fig,
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )



# con esto podemos levantar la aplicación en el navegador
if __name__ == "__main__":
    app.run_server(debug=True)


