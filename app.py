from dash import Dash, dcc, Output, Input,html  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import date

from Charts import *
# Los componentes. Ya los conocen
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])



datepicker= html.Div([
    dcc.DatePickerRange(
        id='date-picker-range-1',
        start_date=date(2023, 6, 9),
        end_date=date(2023, 6, 16),
        end_date_placeholder_text='Fecha'
    ),
    html.Div(id="container-line")
])

mytitle = dcc.Markdown(children='# Terremotos')


mapgraph = dcc.Graph(figure={},
            style={'width': '100%', 'display': 'inline-block'})
histograph = dcc.Graph(figure=HistChart(),
            style={'width': '50%', 'display': 'inline-block'})
scattergraph = dcc.Graph(figure=ScatterChart()
                         ,
            style={'width': '50%', 'display': 'inline-block'})

linegraph = dcc.Graph(figure=LineChart(),
            style={'width': '50%', 'display': 'inline-block'}                      
)
piegraph = dcc.Graph(
    figure=PieChart(),
    style={'width': '50%', 'display': 'inline-block'}
)



checkbox=dcc.Checklist(
    ['Baja Intensidad', 'Media Intensidad', 'Alta Intensidad'],
    ['Baja Intensidad', 'Media Intensidad', 'Alta Intensidad'],
    inline=True
)


dropdown = dcc.Dropdown(options=['Baja Intensidad', 'Media Intensidad', 'Alta Intensidad'],
                        value='Baja Intensidad',  # valor inicialmente desplegado
                        clearable=False)









# Personalizar layout
#app.layout = dbc.Container([mytitle,dbc.Row([piegraph,linegraph]),mapgraph,dropdown,scattergraph,histograph])



app.layout = html.Div([
    mytitle,

    html.Div([
        piegraph,
        linegraph
    ]),

    html.Div([
        mapgraph,

        dropdown
    ]),

    html.Div([
        histograph,
        scattergraph
    ])
])












""" # Callback para interactuar desde el dropdown al gráfico
@app.callback(
    Output(linegraph, component_property='figu  re'),
    Input(datepicker, component_property='value')
)
def update_line(user_input):  # argumento desde el component_property del Input
    
    
    df_earthquakes = pd.read_csv('all_week.csv',skipfooter=3, engine='python')
    #start_date=pd.to.datetime[user_input]
    #end_date=pd.to.datetime[]

    
    
    config = {'scrollZoom': True}
    fig = px.line(df_earthquakes, x="time", y="mag", title='El hombre pie', markers=True)
    

    return fig  """


""" # Callback para interactuar desde el dropdown al gráfico
@app.callback(
    Output(histograph, component_property='figure'),
    Input(datepicker2, component_property='value')
)
def update_line(user_input):  # argumento desde el component_property del Input
    
    
    df_earthquakes = pd.read_csv('all_week.csv',skipfooter=3, engine='python')
    # Convertir la columna 'time' en formato de fecha y extraer el componente de fecha
    df_earthquakes['time'] = pd.to_datetime(df_earthquakes['time'])
    df_earthquakes['date'] = df_earthquakes['time'].dt.date

    # Calcular la cantidad de terremotos por día
    daily_counts = df_earthquakes['date'].value_counts().sort_index()

    # Crear el histograma utilizando Plotly
    fig = px.histogram(daily_counts, x='date', nbins=len(daily_counts))

    # Personalizar el diseño del histograma
    fig.update_layout(
        title='Cantidad de terremotos por día',
        xaxis_title='Fecha',
        yaxis_title='Cantidad de terremotos',
    )
    

    return fig
 """

@app.callback(
    Output(mapgraph, component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_map(user_input):  
    
    df_earthquakes = pd.read_csv('all_week.csv',skipfooter=3, engine='python')
    
    low_threshold = 3.0
    high_threshold = 5.5
    
    df_earthquakes['intensity'] = pd.cut(df_earthquakes['mag'], bins=[-float('inf'), low_threshold, high_threshold, float('inf')], labels=['Low', 'Mid', 'High'])
    
    intensity_counts = df_earthquakes['intensity'].value_counts()
    df_intensity = intensity_counts.reset_index()
    
    df_merged = pd.merge(df_earthquakes[['latitude', 'longitude', 'intensity','mag']], df_intensity, on='intensity')
    
    
    
    if user_input == 'Baja Intensidad':
        fig = px.scatter_geo(df_merged.loc[df_merged['intensity'] == 'Low'], lat="latitude", lon="longitude",color="mag",
                     color_continuous_scale=px.colors.cyclical.IceFire, size_max=15)

    elif user_input == 'Media Intensidad':
        fig = px.scatter_geo(df_merged.loc[df_merged['intensity'] == 'Mid'], lat="latitude", lon="longitude",color="mag",
                     color_continuous_scale=px.colors.cyclical.IceFire, size_max=15)

    elif user_input == 'Alta Intensidad':
        fig = px.scatter_geo(df_merged.loc[df_merged['intensity'] == 'High'], lat="latitude", lon="longitude",color="mag",
                     color_continuous_scale=px.colors.cyclical.IceFire, size_max=15)
    
    
    return fig 



# Ejecutar
if __name__=='__main__':
    app.run_server(port=8053, debug=True)

