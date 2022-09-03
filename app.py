# importacion de librerias para construir la gui en el navegador
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

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
    return

# aqui definimos el diseño de la aplicacion
app.layout = html.Div(
    children=[
        # le daremos un título general al cuerpo de la aplicacion
        titulo(),
        # aqui solicitaremos los parámetros para dar una solucion al problema
        parametros(),
        # tabs que contendran cada una de las soluciones
        dcc.Tabs(
            id='tabs',
            # valor por defecto
            value='tab1',
            children=[
                dcc.Tab(label='Solución 1', value='tab-1'),
                dcc.Tab(label='Solución 2', value='tab-2'),
                dcc.Tab(label='Solución 3', value='tab-3'),
                dcc.Tab(label='Comparaciones', value='tab-4'),
            ]
        ),
        html.Div(id='contenido-tab')
    ]
)


# con esto podemos levantar la aplicación en el navegador
if __name__ == "__main__":
    app.run_server(debug=True)