import plotly.express as px
import dash_core_components as dcc

def create_price_trend_chart(df):
    """График динамики цен"""
    fig = px.line(
        df.groupby(['departure_at', 'destination'])['price'].mean().reset_index(),
        x='departure_at',
        y='price',
        color='destination',
        title='Динамика цен по направлениям'
    )
    return dcc.Graph(figure=fig, id='price-trend-chart')

def create_price_distribution_chart(df):
    """Распределение цен"""
    fig = px.box(
        df,
        x='destination',
        y='price',
        title='Распределение цен по направлениям'
    )
    return dcc.Graph(figure=fig, id='price-distribution-chart')

def create_map_chart(df):
    """Карта направлений"""
    # Агрегируем данные для карты
    agg_df = df.groupby('destination').agg({
        'price': 'mean',
        'flight_number': 'count'
    }).reset_index()
    
    fig = px.scatter_geo(
        agg_df,
        locations='destination',
        locationmode='ISO-3',
        size='flight_number',
        color='price',
        hover_name='destination',
        projection='natural earth',
        title='Карта направлений'
    )
    return dcc.Graph(figure=fig, id='map-chart')
