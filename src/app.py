import pathlib
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df01 = pd.read_excel(DATA_PATH.joinpath('experimento.xlsx'), sheet_name='Hoja1')

grades = df01["NIVEL"].sort_values().unique()
subjetsALL = df01["ASIGNATURA"].sort_values().unique()

mask01 = df01[df01["NIVEL"]=="1MEDIO"]
mask02 = df01[df01["NIVEL"]=="2MEDIO"]
mask03 = df01[df01["NIVEL"]=="3MEDIO"]
mask04 = df01[df01["NIVEL"]=="4MEDIO"]

subjets1M = mask01["ASIGNATURA"].sort_values().unique()
subjets2M = mask02["ASIGNATURA"].sort_values().unique()
subjets3M = mask03["ASIGNATURA"].sort_values().unique()
subjets4M = mask04["ASIGNATURA"].sort_values().unique()

# print(df01)
# mask01=df01[df01["NIVEL"]=="1MEDIO"]
# print(mask01)

app = Dash(__name__)
server=app.server

all_options = {
    '1MEDIO': subjets1M,
    '2MEDIO': subjets2M,
    '3MEDIO': subjets3M,
    '4MEDIO': subjets4M
}

app.layout = html.Div(
    children=[

html.Div(
            children=[
                html.H1(
                    children="Gráficas Rendimientos 1° Semestre 2024", className="header-title"
                )],
            className="header",
        ),


html.Div(children=[
html.Div(
    children=[
        html.Div(children='NIVEL', className='menu-title'),
        dcc.Dropdown(
            id='level', 
            options=[ 
                {'label': nivel, 'value': nivel}
                
                for nivel in all_options.keys()
                
            ],
            value='1MEDIO',
            clearable=False,
            className='dropdown'
        ),
    ]),
html.Div(
    children=[
        html.Div(children="ASIGNATURA", className="menu-title"),
        dcc.Dropdown(
            id='subject',
           # options=[
            #    {"label": asignatura, "value": asignatura}
                                
             #   for asignatura in all_options['1MEDIO']
            #],
            # value="LENGUAJE",
            clearable=False,
            className='dropdown'
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
    Output('subject', 'options'),
    Output('subject', 'value'),
    Input('level', 'value')
    )

def set_subject_options(selected_level):

    options_level = [{'label': i, 'value': i} 
                    for i in all_options[selected_level]]
    
    options_value = all_options[selected_level][0]

    return options_level, options_value


@app.callback(
        Output('grafica', 'figure'),
        Input('level', 'value'),
        Input('subject','value')
        )

def update_charts(nivel,asignatura):

    mask01 = df01.query(
        "NIVEL == @nivel and ASIGNATURA == @asignatura")
        
    trace01 = px.bar(mask01, x='CURSO', y=['Matrícula','Promovidos','Reprobados'],
                     title= 'Rendimientos estudiantes',
                     width=1024, height=400,
                     labels={'value':'Cantidad estudiantes','variable':'Categorías','CURSO':'Cursos'},
                     barmode='group',
                     color_discrete_map={'Matrícula':'blue','Promovidos':'green','Reprobados':'orange'},
                     template="simple_white",
                     )

    return trace01


if __name__ == '__main__':
    app.run_server(debug=True)