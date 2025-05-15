import requests
import pandas as pd
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Загрузка переменных окружения
load_dotenv()

class FlightDataFetcher:
    def __init__(self):
        self.api_key = os.getenv('AVIASALES_API_KEY')
        self.base_url = "https://api.travelpayouts.com/v2/prices/latest"
        self.headers = {'x-access-token': self.api_key}
        
    def fetch_prices(self, origin, destinations, days=30):
        """
        Получает данные о ценах из API Aviasales
        
        Args:
            origin (str): Код города отправления (например, 'MOW')
            destinations (list): Список кодов городов назначения
            days (int): Количество дней для анализа (по умолчанию 30)
            
        Returns:
            pd.DataFrame: DataFrame с данными о ценах
        """
        try:
            params = {
                'currency': 'rub',
                'origin': origin,
                'destination': ','.join(destinations),
                'period_type': 'month',
                'page': 1,
                'limit': 1000,
                'show_to_affiliates': 'false'
            }
            
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json().get('data', [])
            logging.info(f"Получено {len(data)} записей")
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logging.error(f"Ошибка при получении данных: {str(e)}")
            return pd.DataFrame()

    def save_raw_data(self, df, output_dir='../data/raw'):
        """
        Сохраняет сырые данные в JSON файл
        
        Args:
            df (pd.DataFrame): DataFrame с данными
            output_dir (str): Директория для сохранения
        """
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{output_dir}/flights_{timestamp}.json"
        
        df.to_json(output_path, orient='records', indent=2)
        logging.info(f"Данные сохранены в {output_path}")

if __name__ == "__main__":
    fetcher = FlightDataFetcher()
    
    # Пример использования
    popular_destinations = ['LED', 'KZN', 'SVX', 'VOZ', 'UFA', 'AER', 'OVB']
    flight_data = fetcher.fetch_prices('MOW', popular_destinations)
    
    if not flight_data.empty:
        fetcher.save_raw_data(flight_data)
