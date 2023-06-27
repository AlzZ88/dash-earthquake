from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd


app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])


#################################
##<-- LECTURA DEL DATASET -->####
#################################

df_earthquakes = pd.read_csv("earthquake_data_fix.csv", skipfooter=3, engine="python")
df_earthquakes["date_time"] = pd.to_datetime(
    df_earthquakes["date_time"], format="%d-%m-%Y %H:%M"
)


####################################
##<-- CREACION GRAFICOS DASH -->####
####################################

scatter_plot = dcc.Graph(
    id="scatter-plot",
    style={"width": "50%", "display": "inline-block"},
)

line_chart = dcc.Graph(
    id="line-chart",
    style={
        "width": "100%",
        "display": "inline-block",
    },
)

pie_chart = dcc.Graph(
    id="pie-chart",
    style={"width": "40%", "display": "inline-block"},
)
bar_chart = dcc.Graph(
    id="bar-chart",
    style={"width": "50%", "display": "inline-block"},
)

bubble_map = dcc.Graph(
    id="bubble-map",
    style={"width": "100%", "display": "inline-block"},
)


##############################
##<-- COMPONENTES DASH -->####
##############################

depth_checklist = dcc.Checklist(
    ["Low", "Mid", "High"], ["Low", "Mid", "High"], inline=True, id="depth-checklist"
)

dropdown_options = [{"label": "All Countries", "value": "All Countries"}] + [
    {"label": country, "value": country}
    for country in sorted(df_earthquakes["country"].unique())
]

countries_dropdown = dcc.Dropdown(
    options=dropdown_options, value="All Countries", id="countries-dropdown"
)

years_slider = dcc.RangeSlider(
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


####################
##<-- LAYOUT -->####
####################


app.layout = html.Div(
    children=[
        dcc.Markdown(children="# Terremotos"),
        dcc.Markdown(children="## Resumen"),
        html.Div(
            [
                pie_chart,
                magnitude_slider,
            ]
        ),
        dcc.Markdown(children="## Magnitud"),
        html.Div(
            [
                countries_dropdown,
                line_chart,
                bubble_map,
                years_slider,
            ]
        ),
        dcc.Markdown(children="## Profundidad"),
        html.Div(
            [
                depth_checklist,
                scatter_plot,
                bar_chart,
            ]
        ),
    ],
    style={
        "background-color": "#1a1a1a",
        "color": "#ffffff",
    },
)


#######################
##<-- CALLBACKS -->####
#######################


@app.callback(
    Output("bubble-map", "figure"),
    Output("line-chart", "figure"),
    Input("countries-dropdown", "value"),
    Input("years-slider", "value"),
)
def update_bubble_map(selected_country, years_range):
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
        # size="magnitude",
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
        title=f"Earthquakes in {selected_country} from {years_range[0]} to {years_range[1]}",
        markers=True,
        height=300,
    )
    return fig, fig2


@app.callback(
    Output("bar-chart", "figure"),
    Input("countries-dropdown", "value"),
    Input("years-slider", "value"),
    Input("depth-checklist", "value"),
)
def update_bar_chart(selected_country, years_range, selected_depth):
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

    filtered_df["year"] = filtered_df["date_time"].dt.year

    df_counts_per_year_and_depth = (
        filtered_df.groupby(["year", "depth_label"]).size().reset_index(name="count")
    )

    df_rearranged_counts_per_year = df_counts_per_year_and_depth.pivot(
        index="year", columns="depth_label", values="count"
    )

    desired_order = ["Low", "Mid", "High"]

    selected_columns = [
        col
        for col in desired_order
        if col in selected_depth and col in df_rearranged_counts_per_year.columns
    ]

    df_rearranged_counts_per_year = df_rearranged_counts_per_year[selected_columns]

    if df_rearranged_counts_per_year.empty:
        fig = px.bar()
        fig.update_layout(
            title="Empty Bar Chart",
        )
    else:
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
    Input("depth-checklist", "value"),
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


##################
##<-- MAIN -->####
##################

if __name__ == "__main__":
    app.run_server(port=8053, debug=True)
