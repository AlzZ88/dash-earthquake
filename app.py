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
            className="dark-mode",
            style={'width': '100%', 'display': 'inline-block',
                   
                    },
            id="map")
histograph = dcc.Graph(figure=HistChart(),
            style={'width': '50%', 'display': 'inline-block', })
scattergraph = dcc.Graph(
    id="scatter-plot",
    #figure=ScatterChart(),
            style={'width': '50%', 'display': 'inline-block'})

linegraph = dcc.Graph(figure={},
            style={'width': '100%', 'display': 'inline-block',},
            id="line")

piegraph = dcc.Graph(
    #figure=PieChart(),
    figure={},
    id="pie-chart",
    style={'width': '40%', 'display': 'inline-block'}
)
bargraph = dcc.Graph(
    #figure=PieChart(),
    figure={},
    id="bar-chart",
    style={'width': '50%', 'display': 'inline-block'}
)

bubblemap = dcc.Graph(
    figure={},
    style={'width': '100%', 'display': 'inline-block'},id="bubble-map"
)

checkbox=dcc.Checklist(
    ['Low', 'Mid', 'High'],
    ['Low', 'Mid', 'High'],
    inline=True,
    id="checklist"
)


depth_checklist = dcc.Checklist(
    ["Low", "Mid", "High"], ["Low", "Mid", "High"], inline=True, id="depth_checklist"
)

dropdown = dcc.Dropdown(options=['Baja Intensidad', 'Media Intensidad', 'Alta Intensidad'],
                        value='Baja Intensidad',  # valor inicialmente desplegado
                        clearable=False)

df_earthquakes = pd.read_csv("earthquake_data_fix.csv", skipfooter=3, engine="python")
df_earthquakes["date_time"] = pd.to_datetime(
    df_earthquakes["date_time"], format="%d-%m-%Y %H:%M"
)



dropdown_options = [{"label": "All Countries", "value": "All Countries"}] + [
    {"label": country, "value": country}
    for country in sorted(df_earthquakes["country"].unique())
]

dropdown1 = dcc.Dropdown(
    options=dropdown_options, value="All Countries", id="country-dropdown"
)

range_slider = dcc.RangeSlider(
    min=2001,
    max=2023,
    step=1,
    value=[2001, 2023],
    marks={year: str(year) for year in range(2001, 2024)},
    id="years-slider",
)

max_mag = df_earthquakes["magnitude"].max()
min_mag = df_earthquakes["magnitude"].min()


magnitude_slider = dcc.Slider(
    min=min_mag, max=max_mag, step=0.5, value=7.0, id="magnitude-slider"
)

# Personalizar layout
#app.layout = dbc.Container([mytitle,dbc.Row([piegraph,linegraph]),mapgraph,dropdown,scattergraph,histograph])



app.layout = html.Div(
    
    
    children=[
    mytitle,
    dcc.Markdown(children='## Resumen'),
    #checkbox,
    html.Div([
        piegraph,
        magnitude_slider,
        
    ]),
    dcc.Markdown(children='## Magnitud'),
    html.Div([
        #mapgraph,
        
        dropdown1,
        linegraph,
        bubblemap,
        #
        range_slider
        
    ]),
    dcc.Markdown(children='## Profundidad'),
    html.Div([
        depth_checklist,
        scattergraph,
        bargraph,
    ]),

    
],
    style={
        "background-color": "#1a1a1a",
        "color": "#ffffff",
    }
    
    
    
    )






@app.callback(
    Output("bubble-map", "figure"),
    Output("line", "figure"),
    Input("country-dropdown", "value"),
    Input("years-slider", "value"),
)
def update_bubble_map(selected_country, years_range):
    max_value = df_earthquakes["magnitude"].max()

    # Select the minimum value from the column
    min_value = df_earthquakes["magnitude"].min()

    #print("Maximum value:", max_value)
    #print("Minimum value:", min_value)

    if selected_country == "All Countries":
        filtered_df = df_earthquakes[
            (
                df_earthquakes["date_time"].dt.year.between(
                    years_range[0], years_range[1]
                )
            )
        ]
    else:
        filtered_df = df_earthquakes[
            (df_earthquakes["country"] == selected_country)
            & (
                df_earthquakes["date_time"].dt.year.between(
                    years_range[0], years_range[1]
                )
            )
        ]

    fig = px.scatter_geo(
        filtered_df,
        lat="latitude",
        lon="longitude",
        color="magnitude",
        #size="magnitude",
        hover_data=["country", "date_time"],    
        color_continuous_scale=px.colors.sequential.Oranges,
        size_max=15,
    )

    title = (
        f"Earthquakes in {selected_country} from {years_range[0]} to {years_range[1]}"
    )

    fig.update_layout(title=title)

    fig2 = px.line(
        filtered_df,
        x="date_time",
        y="magnitude",
        line_group="country",
        color="country",
        title=f'Earthquakes in {selected_country} from {years_range[0]} to {years_range[1]}',
        markers=True,
        height=300
    )
    return fig,fig2


@app.callback(
    Output("bar-chart", "figure"),
    Input("depth_checklist", "value"),
)
def update_bar_chart(selected_depth):
    df_copy = df_earthquakes.copy()
    df_copy["year"] = df_copy["date_time"].dt.year

    df_counts_per_year_and_depth = (
        df_copy.groupby(["year", "depth_label"]).size().reset_index(name="count")
    )

    df_rearranged_counts_per_year = df_counts_per_year_and_depth.pivot(
        index="year", columns="depth_label", values="count"
    )

    desired_order = ["Low", "Mid", "High"]

    df_rearranged_counts_per_year = df_rearranged_counts_per_year[desired_order]

    selected_columns = [
        col for col in df_rearranged_counts_per_year.columns if col in selected_depth
    ]

    print(df_rearranged_counts_per_year.head())

    fig = px.bar(
        df_rearranged_counts_per_year,
        x=df_rearranged_counts_per_year.index,
        y=selected_columns,
        title="Number of Earthquakes per Year",
        labels={"x": "Year", "y": "Count"},
        barmode="stack",
    )

    return fig


@app.callback(
    Output("scatter-plot", "figure"),
    Input("depth_checklist", "value"),
)
def update_scatter_chart(selected_depth):
    filtered_df = df_earthquakes[(df_earthquakes["depth_label"].isin(selected_depth))]

    fig = px.scatter(
        filtered_df,
        x="depth",
        y="magnitude",
        title="Distribution of the earthquakes per depth label",
        color="depth_label",
    )

    fig.update_traces(
        marker=dict(size=8, symbol="cross"),
        selector=dict(mode="markers"),
    )

    return fig


@app.callback(
    Output("pie-chart", "figure"),
    Input("years-slider", "value"),
    Input("magnitude-slider", "value"),
)
def update_pie_chart(years_range, selected_magnitude):
    filtered_df = df_earthquakes[
        (df_earthquakes["date_time"].dt.year.between(years_range[0], years_range[1]))
        & (df_earthquakes["magnitude"] >= selected_magnitude)
    ]

    filtered_df = (
        filtered_df.groupby(["country"]).size().reset_index(name="count").head(5)
    )

    print(filtered_df)

    fig = px.pie(
        filtered_df,
        values="count",
        names="country",
        title="Earthquake Intensity Distribution",
        color_discrete_sequence=px.colors.sequential.RdBu,
        hover_data=["count"],
        labels={"count": "# of earthquakes"},
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")

    title = f"Top 5 earthquakes from {years_range[0]} to {years_range[1]} with mag >= {selected_magnitude}"

    fig.update_layout(title=title)

    return fig











""" 


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
 """


app.css.append_css({"external_url": "styles.css"})
# Ejecutar
if __name__=='__main__':
    app.run_server(port=8053, debug=True)

