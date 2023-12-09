import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Plotter:
    def __init__(self, data_frame):
        self.df = data_frame

    def visualize_nulls(self):
        plt.figure(figsize=(10, 6))
        sns.heatmap(self.df.isnull(), cbar=False, cmap='viridis')
        plt.title('Null Values Heatmap')
        plt.show()

class DataFrameTransform:
    def __init__(self, data_frame):
        self.df = data_frame

    def check_nulls(self):
        return self.df.isnull().sum()

    def drop_nulls(self, threshold=0.5):
        # Drop columns with null values exceeding the threshold
        self.df = self.df.dropna(thresh=len(self.df) * threshold, axis=1)
        return self.df

    def impute_nulls(self, strategy='median'):
        # Get only numeric columns
        numeric_columns = self.df.select_dtypes(include=['number']).columns

        # Impute null values for numeric columns using specified strategy
        if strategy == 'median':
            self.df[numeric_columns] = self.df[numeric_columns].fillna(self.df[numeric_columns].median())
        elif strategy == 'mean':
            self.df[numeric_columns] = self.df[numeric_columns].fillna(self.df[numeric_columns].mean())
        # Add additional conditions for other strategies as needed

        # For non-numeric columns, fill with a specific value or impute differently
        non_numeric_columns = set(self.df.columns) - set(numeric_columns)
        for col in non_numeric_columns:
            # Fill with a specific value or apply a different imputation strategy
            self.df[col].fillna('unknown', inplace=True)  # Replace 'unknown' with your chosen strategy

        return self.df