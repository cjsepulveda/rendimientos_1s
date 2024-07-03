import pathlib
from dash import Dash, html, dcc
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df01 = pd.read_excel(DATA_PATH.joinpath('experimento.xlsx'), sheet_name='Hoja1')

trace01 = px.bar(df01, x='CURSO', y=['Matrícula','Promovidos','Reprobados'], barmode='group')

app = Dash(__name__)
server=app.server

app.layout = html.Div(children=[
    html.H1(children='Reporte 1° Medios 2024'),
    html.Div(children='Graficas'),
    dcc.Graph(figure=trace01)
])


if __name__ == '__main__':
    app.run_server(debug=True)