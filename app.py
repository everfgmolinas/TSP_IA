# importacion de librerias para construir la gui en el navegador
import dash
from dash import html, dcc

# aqui creamos una instancia de la aplicación para ir trabajando
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# aqui le damos un título a la aplicación
app.title = 'TSP-Resolucion'

# definicion de funciones útiles
def app_title():
    return html.H3(
        'Problema del vendedor viajero',
        style={
            'textAlign':'center'
        }
    )

def tabulaciones():
    return html.Div(
        id='tabs',
        className='tabs',
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Parámetros del problema",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Muestra de resultados",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ]
    )

# aqui definimos el diseño de la aplicacion
app.layout = html.Div(
    children=[
        # le daremos un título general al cuerpo de la aplicacion
        app_title(),
        html.Div(
            id="app-container",
            children=[
                tabulaciones(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
    ]
)

# con esto podemos levantar la aplicación en el navegador
if __name__ == "__main__":
    app.run_server(debug=True)