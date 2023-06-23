from dash import Dash, dcc, Output, Input,html  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from Charts import *




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
            style={'width': '100%', 'display': 'inline-block'},
            id="map")
histograph = dcc.Graph(figure=HistChart(),
            style={'width': '50%', 'display': 'inline-block'})
scattergraph = dcc.Graph(figure=ScatterChart()
                         ,
            style={'width': '50%', 'display': 'inline-block'})

linegraph = dcc.Graph(figure={},
            style={'width': '50%', 'display': 'inline-block'},
            id="line")

piegraph = dcc.Graph(
    figure=PieChart(),
    style={'width': '50%', 'display': 'inline-block'}
)



checkbox=dcc.Checklist(
    ['Low', 'Mid', 'High'],
    ['Low', 'Mid', 'High'],
    inline=True,
    id="checklist"
)


dropdown = dcc.Dropdown(options=['Baja Intensidad', 'Media Intensidad', 'Alta Intensidad'],
                        value='Baja Intensidad',  # valor inicialmente desplegado
                        clearable=False)


# Personalizar layout
#app.layout = dbc.Container([mytitle,dbc.Row([piegraph,linegraph]),mapgraph,dropdown,scattergraph,histograph])



app.layout = html.Div([
    mytitle,
    checkbox,
    html.Div([
        piegraph,
        linegraph
    ]),

    html.Div([
        mapgraph,

        
    ]),

    html.Div([
        histograph,
        scattergraph
    ])
])





@app.callback(
    [Output("line", "figure"), Output("map", "figure")],
    Input("checklist", "value")
)
def update_by_checklist(intensities):
    df_earthquakes = pd.read_csv('all_week.csv',skipfooter=3, engine='python')
    
    low_threshold = 3.0
    high_threshold = 5.5
    
    df_earthquakes['intensity'] = pd.cut(df_earthquakes['mag'], bins=[-float('inf'), low_threshold, high_threshold, float('inf')], labels=['Low', 'Mid', 'High'])
    
    intensity_counts = df_earthquakes['intensity'].value_counts()
    df_intensity = intensity_counts.reset_index()
    
    
    
    
    df_mag = pd.merge(df_earthquakes[['intensity','mag','time']], df_intensity, on='intensity')
    df_lat = pd.merge(df_earthquakes[['latitude', 'longitude', 'intensity','mag']], df_intensity, on='intensity')
    
    
    
    
    filtered_df_mag = df_mag[df_mag['intensity'].isin(intensities)]
    
    filtered_df_lat = df_lat[df_mag['intensity'].isin(intensities)]
    
    fig1 = px.line(
        filtered_df_mag,
        x="time",
        y="mag",
        line_group="intensity",
        color="intensity",
        title='Magnitud de los Terremotos ocurridos entre el 9 junio y el 16 de junio',
        markers=True,
        height=300
    )
    fig2=px.scatter_geo(filtered_df_lat, lat="latitude", lon="longitude",color="mag",
                     color_continuous_scale=px.colors.cyclical.IceFire, size_max=15)
    
    return fig1,fig2




# Ejecutar
if __name__=='__main__':
    app.run_server(port=8053, debug=True)

