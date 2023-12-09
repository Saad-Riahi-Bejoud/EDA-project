import pandas as pd

class DataFrameInfo:
    def __init__(self, df):
        self.df = df

    def describe_columns(self):
        return self.df.dtypes

    def extract_statistical_values(self):
        return self.df.describe()

    def count_distinct_values(self, categorical_columns):
        return self.df[categorical_columns].nunique()

    def print_dataframe_shape(self):
        print("DataFrame Shape:", self.df.shape)

    def count_null_values(self):
        return self.df.isnull().sum()

    def percentage_null_values(self):
        return (self.df.isnull().mean() * 100).round(2)