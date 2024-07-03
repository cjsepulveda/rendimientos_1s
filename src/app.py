import pathlib
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df = pd.read_excel(DATA_PATH.joinpath('experimento.xlsx'), sheet_name='Hoja1')

trace5 = px.bar(df, x='CURSO', y=['Matrícula','Promovidos','Reprobados'], barmode='group')


#fig = go.Figure(data=[
 #   go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
  #  (name='LA Zoo', x=animals, y=[12, 18, 29])
# ])

app = dash.Dash()
server=app.server

app.layout = html.Div(children=[
    html.H1(children='Reporte 1° Medios Año 2024'),
    html.Div(children='Graficas'),
    dcc.Graph(figure=trace5)
])


if __name__ == '__main__':
    app.run_server(debug=True)