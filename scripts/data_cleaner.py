import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataCleaner:
    def __init__(self):
        self.price_columns = ['price', 'flight_duration']
        self.date_columns = ['flight_date', 'booking_date']
        
    def clean_data(self, raw_df):
        """
        Очищает и преобразует сырые данные
        
        Args:
            raw_df (pd.DataFrame): Сырой DataFrame
            
        Returns:
            pd.DataFrame: Очищенный DataFrame
        """
        try:
            # Копируем данные
            df = raw_df.copy()
            
            # 1. Удаление дубликатов
            initial_count = len(df)
            df = self._remove_duplicates(df)
            logging.info(f"Удалено {initial_count - len(df)} дубликатов")
            
            # 2. Обработка пропусков
            df = self._handle_missing_values(df)
            
            # 3. Преобразование типов
            df = self._convert_types(df)
            
            # 4. Добавление новых признаков
            df = self._add_features(df)
            
            return df
            
        except Exception as e:
            logging.error(f"Ошибка при очистке данных: {str(e)}")
            return pd.DataFrame()
    
    def _remove_duplicates(self, df):
        """Удаление дубликатов"""
        return df.drop_duplicates(
            subset=['flight_number', 'flight_date', 'booking_date'],
            keep='first'
        )
    
    def _handle_missing_values(self, df):
        """Обработка пропущенных значений"""
        # Заполнение медианными значениями
        for col in self.price_columns:
            if col in df.columns:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                logging.info(f"Пропуски в {col} заполнены медианой: {median_val}")
        
        # Удаление записей с пропущенными датами
        for col in self.date_columns:
            if col in df.columns:
                df = df.dropna(subset=[col])
        
        return df
    
    def _convert_types(self, df):
        """Преобразование типов данных"""
        # Даты
        for col in self.date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        # Числовые колонки
        for col in self.price_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def _add_features(self, df):
        """Добавление новых признаков"""
        if 'flight_date
