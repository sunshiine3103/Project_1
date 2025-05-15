import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def create_filters(df):
    """Создает компоненты фильтрации"""
    return html.Div([
        html.Label('Диапазон дат:'),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=df['departure_at'].min(),
            max_date_allowed=df['departure_at'].max(),
            start_date=df['departure_at'].min(),
            end_date=df['departure_at'].max()
        ),
        
        html.Label('Направления:'),
        dcc.Dropdown(
            id='destination-dropdown',
            options=[{'label': i, 'value': i} for i in df['destination'].unique()],
            multi=True,
            placeholder="Выберите направления"
        ),
        
        html.Label('Диапазон цен:'),
        dcc.RangeSlider(
            id='price-range',
            min=df['price'].min(),
            max=df['price'].max(),
            step=1000,
            value=[df['price'].min(), df['price'].max()],
            marks={i: f'{i//1000}K' for i in range(
                int(df['price'].min()), 
                int(df['price'].max())+1, 
                5000
            }
        )
    ], className='filters-container')
