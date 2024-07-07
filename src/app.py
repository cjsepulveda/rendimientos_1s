import pathlib
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df01 = pd.read_excel(DATA_PATH.joinpath('data_level_grade.xlsx'), sheet_name='DATA')

grades = df01["NIVEL"].sort_values().unique()
subjetsALL = df01["ASIGNATURA"].unique()

mask01 = df01[df01["NIVEL"]=="1MEDIO"]
mask02 = df01[df01["NIVEL"]=="2MEDIO"]
mask03 = df01[df01["NIVEL"]=="3MEDIO"]
mask04 = df01[df01["NIVEL"]=="4MEDIO"]

subjets1M = mask01["ASIGNATURA"].unique()
subjets2M = mask02["ASIGNATURA"].unique()
subjets3M = mask03["ASIGNATURA"].unique()
subjets4M = mask04["ASIGNATURA"].unique()

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
            className='dropdown',
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

# callback para cambiar lista depegable segun nivel
@app.callback(
    Output('subject', 'options'),
    Output('subject', 'value'),
    Input('level', 'value')
    )
# función para cambiar opciones de lista despegable asignaturas segun el nivel y valor inicial
def set_subject_options(selected_level):

    options_level = [{'label': i, 'value': i} 
                    for i in all_options[selected_level]]
    
    options_value = all_options[selected_level][0]

    return options_level, options_value

# callback para filtrar gráfico segun nivel y asignatura
@app.callback(
        Output('grafica', 'figure'),
        Input('level', 'value'),
        Input('subject','value')
        )

# función para grafico segun nivel y asignatura
def update_charts(nivel,asignatura):

    select_nivel_subject = df01.query(
        "NIVEL == @nivel and ASIGNATURA == @asignatura")
        
    trace01 = px.bar(select_nivel_subject, x='CURSO', y=['MB','B','S','I','P'],
                     title= 'Rendimientos estudiantes',
                     width=1200, height=400,
                     labels={'value':'Porcentaje estudiantes','variable':'Categorías','CURSO':'Cursos'},
                     barmode='group',
                     color_discrete_map={'MB':'blue','B':'green','S':'orange','I':'tomato','P':'gold'},
                     template="simple_white",
                     text_auto='.0%',
                     range_y=[0,1],
                     )
    
    trace01.update_yaxes(tickformat=".1%", tickfont_weight='bold',title_font_weight='bold')
    trace01.update_xaxes(tickfont_weight='bold')
    trace01.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    trace01.update_layout(
                         hoverlabel_font_color='white',
                         uniformtext_minsize=5,
                         uniformtext_mode='show',
                         title_font_weight='bold'
                         )
    
    return trace01


if __name__ == '__main__':
    app.run_server(debug=True)