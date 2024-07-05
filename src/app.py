import pathlib
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df01 = pd.read_excel(DATA_PATH.joinpath('experimento.xlsx'), sheet_name='Hoja1')
grades = df01["NIVEL"].sort_values().unique()
subjets = df01["ASIGNATURA"].sort_values().unique()


# print(df01)
# mask01=df01[df01["NIVEL"]=="1MEDIO"]
# print(mask01)

app = Dash(__name__)
server=app.server

app.layout = html.Div(
    children=[

html.Div(
            children=[
                html.H1(
                    children="Gráficas Rendimientos 1° Semestre 2024", className="header-title"
                ),
                html.P(
                    children=(
                        "Análisis del rendimiento por nivel y asignatura"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),


html.Div(children=[
html.Div(
    children=[
        html.Div(children="NIVEL", className="menu-title"),
        dcc.Dropdown(
            id='level', 
            options=[ 
                {"label": nivel, "value": nivel} 
                for nivel in grades
            ],
            value="1MEDIO",
            clearable=False,
            
        ),
    ]),
html.Div(
    children=[
        html.Div(children="ASIGNATURA", className="menu-title"),
        dcc.Dropdown(
            id='subject',
            options=[
                {"label": asignatura, "value": asignatura}
                for asignatura in subjets
            ],
            value="LENGUAJE",
            clearable=False,
                ),
    
]),
],
className="menu",
),

html.Div(children=[
    dcc.Graph( id='grafica', config={"displayModeBar": False}, className="card")
],
className="wrapper",
),
    ])


@app.callback(
        Output('grafica', 'figure'),
        Input('level', 'value'),
        Input('subject','value')
        )

def update_charts(nivel,asignatura):

    mask01 = df01.query(
        "NIVEL == @nivel and ASIGNATURA == @asignatura")
        
    trace01 = px.bar(mask01, x='CURSO', y=['Matrícula','Promovidos','Reprobados'], barmode='group')

    return trace01


if __name__ == '__main__':
    app.run_server(debug=True)