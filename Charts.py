import plotly.express as px
import pandas as pd
def PieChart():
    df_earthquakes = pd.read_csv('all_week.csv',skipfooter=3, engine='python')
    # Pie chart de intensidades.
    low_threshold = 3.0
    high_threshold = 5.5

    df_earthquakes['intensity'] = pd.cut(df_earthquakes['mag'], bins=[-float('inf'), low_threshold, high_threshold, float('inf')], labels=['Low', 'Mid', 'High'])

    intensity_counts = df_earthquakes['intensity'].value_counts()
            
    df_intensity = intensity_counts.reset_index()
    df_intensity.columns = ['Intensity', 'Count']
    df_intensity = intensity_counts.reset_index()
    df_intensity.columns = ['Intensity', 'Count']

    fig = px.pie(df_intensity, 
                values='Count', 
                names='Intensity', 
                title='Earthquake Intensity Distribution', 
                color_discrete_sequence=px.colors.sequential.RdBu,
                height=300)

    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig  

def HistChart():
    
    
   # Leer el archivo CSV y crear el dataframe df_earthquakes
    df_earthquakes = pd.read_csv('all_week.csv', skipfooter=3, engine='python')

    # Convertir la columna 'time' en formato de fecha y extraer el componente de fecha
    df_earthquakes['time'] = pd.to_datetime(df_earthquakes['time'])
    df_earthquakes['date'] = df_earthquakes['time'].dt.date

    # Calcular la cantidad de terremotos por día
    daily_counts = df_earthquakes['date'].value_counts().sort_index()

    # Crear un nuevo dataframe con las fechas y la cantidad de terremotos
    df_daily_counts = pd.DataFrame({'date': daily_counts.index, 'count': daily_counts.values})

    # Crear el histograma utilizando Plotly
    fig = px.histogram(df_daily_counts, x='date', y='count', nbins=len(daily_counts), height=300)

    # Personalizar el diseño del histograma
    fig.update_layout(
        title='Cantidad de terremotos por día',
        xaxis_title='Fecha',
        yaxis_title='Cantidad de terremotos',
    )
    return fig

def ScatterChart():
    df_earthquakes = pd.read_csv('all_week.csv', skipfooter=3, engine='python')
    fig = px.scatter(df_earthquakes, x="mag", y="depth", 
                 title="placeholder",
                 color="mag", height=300)
 
    fig.update_traces(
        marker=dict(size=8, symbol="cross"),
        selector=dict(mode="markers"),
    )
    return fig      


def LineChart():
    
    
    
    
    df_earthquakes = pd.read_csv('all_week.csv',skipfooter=3, engine='python')
    
    low_threshold = 3.0
    high_threshold = 5.5
    
    df_earthquakes['intensity'] = pd.cut(df_earthquakes['mag'], bins=[-float('inf'), low_threshold, high_threshold, float('inf')], labels=['Low', 'Mid', 'High'])
    
    intensity_counts = df_earthquakes['intensity'].value_counts()
    df_intensity = intensity_counts.reset_index()
    
    df_merged = pd.merge(df_earthquakes[['intensity','mag','time']], df_intensity, on='intensity')
    

    fig = px.line(df_merged, x="time", y="mag", line_group="intensity",color="intensity",  title='Magnitud de los Terremotos ocurridos entre el 9 junio y el 16 de junio', markers=True, height=300)
    return fig      