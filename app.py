from dash import Dash, dcc, Output, Input,html  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import date
# Los componentes. Ya los conocen
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])



datepicker= html.Div([
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=date(2023, 6, 9),
        end_date=date(2023, 6, 16),
        end_date_placeholder_text='Fecha'
    ),
    html.Div(id="container-line")
])

mytitle = dcc.Markdown(children='# Terremotos')

linegraph = dcc.Graph(id="line", figure={})
mapgraph = dcc.Graph(figure={})




dropdown = dcc.Dropdown(options=['Baja Intensidad', 'Media Intensidad', 'Alta Intensidad'],
                        value='Baja Intensidad',  # valor inicialmente desplegado
                        clearable=False)

# Personalizar layout
app.layout = dbc.Container([mytitle, linegraph, datepicker,mapgraph,dropdown])








# Callback para interactuar desde el dropdown al gráfico
@app.callback(
    Output("container-line", "children"),
    Input("date-picker-range", 'date')
)
def update_line(user_input):  # argumento desde el component_property del Input
    
    
    df_earthquakes = pd.read_csv('all_week.csv',skipfooter=3, engine='python')
    #start_date=pd.to.datetime[user_input]
    #end_date=pd.to.datetime[]

    
    
    config = {'scrollZoom': True}
    fig = px.line(df_earthquakes, x="time", y="mag", title='El hombre pie', markers=True)
    

    return fig







@app.callback(
    Output(mapgraph, component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_map(user_input):  # argumento desde el component_property del Input
    df_earthquakes = pd.read_csv('all_week.csv',skipfooter=3, engine='python')
    
    low_threshold = 3.0
    high_threshold = 5.5

    df_earthquakes['intensity'] = pd.cut(df_earthquakes['mag'], bins=[-float('inf'), low_threshold, high_threshold, float('inf')], labels=['Low', 'Mid', 'High'])
    intensity_counts = df_earthquakes['intensity'].value_counts()

    df_intensity = intensity_counts.reset_index()
    
    


    
    if user_input == 'Baja Intensidad':
        
        fig = px.scatter_geo(df_earthquakes, lat="latitude", lon="longitude", color="mag", size="mag",
                     color_continuous_scale=px.colors.cyclical.IceFire, size_max=15)

    elif user_input == 'Media Intensidad':
        fig = px.scatter_geo(df_earthquakes, lat="latitude", lon="longitude", color="mag", size="mag",
                     color_continuous_scale=px.colors.cyclical.IceFire, size_max=15)

    elif user_input == 'Alta Intensidad':
        fig = px.scatter_geo(df_earthquakes, lat="latitude", lon="longitude", color="mag", size="mag",
                     color_continuous_scale=px.colors.cyclical.IceFire, size_max=15)

        #fig = px.scatter(data_frame=df, x="count", y="nation", color="medal",
        #                 symbol="medal")

    
    return fig  # objeto retornado se asigna al component_property del Output



# Ejecutar
if __name__=='__main__':
    app.run_server(port=8053, debug=True)

