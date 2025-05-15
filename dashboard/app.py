import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from components.filters import create_filters
from components.charts import (
    create_price_trend_chart,
    create_price_distribution_chart,
    create_map_chart
)

# Загрузка данных
df = pd.read_parquet('../data/processed/flights_processed.parquet')

# Инициализация приложения
app = dash.Dash(__name__, assets_folder='assets')

# Layout приложения
app.layout = html.Div([
    html.H1('Анализ цен на авиабилеты', className='header'),
    
    # Секция фильтров
    html.Div(
        create_filters(df),
        className='filters-section'
    ),
    
    # Основные графики
    html.Div([
        html.Div(
            create_price_trend_chart(df),
            className='chart-container'
        ),
        html.Div(
            create_price_distribution_chart(df),
            className='chart-container'
        )
    ], className='row'),
    
    # Карта
    html.Div(
        create_map_chart(df),
        className='map-container'
    ),
    
    # Скрытый div для хранения данных
    html.Div(id='filtered-data', style={'display': 'none'})
], className='app-container')

# Callback для фильтрации данных
@app.callback(
    Output('filtered-data', 'children'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('destination-dropdown', 'value'),
     Input('price-range', 'value')]
)
def filter_data(start_date, end_date, destinations, price_range):
    filtered = df[
        (df['departure_at'] >= start_date) &
        (df['departure_at'] <= end_date) &
        (df['price'] >= price_range[0]) &
        (df['price'] <= price_range[1])
    ]
    
    if destinations:
        filtered = filtered[filtered['destination'].isin(destinations)]
    
    return filtered.to_json(date_format='iso', orient='split')

# Callbacks для обновления графиков
@app.callback(
    Output('price-trend-chart', 'figure'),
    [Input('filtered-data', 'children')]
)
def update_trend_chart(filtered_data):
    filtered_df = pd.read_json(filtered_data, orient='split')
    fig = px.line(
        filtered_df.groupby(['departure_at', 'destination'])['price'].mean().reset_index(),
        x='departure_at',
        y='price',
        color='destination'
    )
    fig.update_layout(title='Динамика цен (фильтрованная)')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
