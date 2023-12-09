import pandas as pd
import numpy as np

class DataTransform:
    def __init__(self, data_frame):
        self.df = data_frame

    def convert_date_columns(self, date_columns):
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        return self.df

    def convert_numeric_columns(self, numeric_columns):
        for col in numeric_columns:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        return self.df

    def convert_to_categorical(self, categorical_columns):
        for col in categorical_columns:
            self.df[col] = self.df[col].astype('category')
        return self.df

    def remove_excess_symbols(self, columns_with_symbols):
        for col in columns_with_symbols:
            self.df[col] = np.where(
                self.df[col].apply(lambda x: isinstance(x, str)),
                self.df[col].astype(str).str.replace('[^0-9]', '', regex=True),
                self.df[col]
            )
        return self.df

