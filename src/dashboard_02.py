import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd

file_name = "experimento.xlsx" # Give Any Name / Existing Name


dfe = pd.read_excel(file_name, usecols=None, sheet_name='Hoja1') 


trace5 = go.Bar(x=dfe.CURSO, y=dfe.Promovidos)



## Importar la data
df = pd.read_csv('data.csv', delimiter = ';')

#Crear una tabla dinámica
pv = pd.pivot_table(df, index=['Name'], columns=["Status"], values=['Quantity'], aggfunc="sum", fill_value=0)

trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declinada')], name='Declinada')
# trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pendiente')], name='Pendiente')
# trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presentada')], name='Presentada')
# trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'ganada')], name='Ganada')

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Reporte 1° Medios 2024'),
    html.Div(children='''Promovidos.'''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace5],
            'layout':
            go.Layout(title='Promovidos 2° Medio', barmode='stack')
        })
])


if __name__ == '__main__':
    app.run_server(debug=True)