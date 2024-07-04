import pathlib
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df01 = pd.read_excel(DATA_PATH.joinpath('experimento.xlsx'), sheet_name='Hoja1')



app = Dash(__name__)
server=app.server

app.layout = html.Div(children=[
    html.Label('Nivel'),
        dcc.Dropdown(['1MEDIO', '2MEDIO'], '1MEDIO', id='nivel'),
        dcc.Dropdown(['LENGUAJE','MATEMÁTICA'],'LENGUAJE', id='subject'),
    html.H1(children='Reporte 1° Medios 2024'),
    html.Div(children='Graficas'),
    dcc.Graph( id='grafica')
])

@app.callback(
        Output('grafica', 'figure'),
        Input('nivel', 'value'),
        Input('subject','value')
        )

def update_charts(grade,sub):

    gr = grade
    s = sub

    mask01 = df01.query(
        "NIVEL == @gr and ASIGNATURA == @s")
        
    trace01 = px.bar(mask01, x='CURSO', y=['Matrícula','Promovidos','Reprobados'], barmode='group')

    return trace01


if __name__ == '__main__':
    app.run_server(debug=True)