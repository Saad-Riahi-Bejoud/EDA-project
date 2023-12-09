import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataFrameTransform:
    def __init__(self, df):
        self.df = df

    def identify_skewed_columns(self, skew_threshold=1):
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        skewness = self.df[numeric_columns].apply(lambda x: x.skew()).abs()
        skewed_columns = skewness[skewness > skew_threshold].index.tolist()
        return skewed_columns

    def find_best_transformation(self, column, transformations):
        original_skew = self.df[column].skew()

        best_transformation = None
        best_skewness = original_skew

        for transform in transformations:
            transformed_column = transform(self.df[column])
            skewness = transformed_column.skew()

            if skewness < best_skewness:
                best_skewness = skewness
                best_transformation = transform

        return best_transformation

    def reduce_skewness(self, skew_threshold=1, transformations=None):
        if transformations is None:
            transformations = [np.log1p, np.sqrt, np.reciprocal]

        skewed_columns = self.identify_skewed_columns(skew_threshold)

        for column in skewed_columns:
            original_data = self.df[column]

            # Apply the identified transformations
            best_transformation = None
            best_skewness = original_data.skew()

            for transform in transformations:
                try:
                    # Check for zero values before applying reciprocal transformation
                    if transform == np.reciprocal and (original_data == 0).any():
                        continue

                    transformed_column = transform(original_data)

                    # Check for division by zero or NaN values
                    if np.isnan(transformed_column).any() or np.isinf(transformed_column).any():
                        continue

                    skew = transformed_column.skew()

                    if abs(skew) < abs(best_skewness):
                        best_skewness = skew
                        best_transformation = transformed_column

                except (ValueError, ZeroDivisionError):
                    # Skip transformations that result in errors (e.g., log(0), reciprocal(0))
                    continue

            # Update the DataFrame with the best transformation
            if best_transformation is not None:
                self.df[column] = best_transformation

        return self.df
    def remove_outliers(self, columns):
        for col in columns:
            # Calculate the IQR (Interquartile Range)
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1

            # Define the upper and lower bounds for outliers
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Remove outliers based on the bounds
            self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]

        return self.df

    def save_copy(self, file_path):
        self.df.to_csv(file_path, index=False)


class Plotter:
    def __init__(self, df):
        self.df = df

    def visualize_outliers(self, columns):
        for col in columns:
            plt.figure(figsize=(10, 5))
            sns.boxplot(x=self.df[col])
            plt.title(f'Outliers Visualization: {col}')
            plt.xlabel(col)
            plt.show()
    def visualize_skewness(self, skewed_columns):
        for col in skewed_columns:
            sns.histplot(self.df[col], kde=True, label='Original', color='blue')
            plt.title(f'Skewness Visualization: {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.legend()
            plt.show()

    def visualize_transformation(self, column_name, original_data, transformed_data):
        if transformed_data is not None:
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            sns.histplot(original_data, kde=True, label='Original', color='blue')
            plt.title(f'Original Distribution: {column_name}')
            plt.xlabel(column_name)
            plt.ylabel('Frequency')
            plt.legend()

            plt.subplot(1, 2, 2)
            sns.histplot(transformed_data, kde=True, label='Transformed', color='green')
            plt.title(f'Transformed Distribution: {column_name}')
            plt.xlabel(column_name)
            plt.ylabel('Frequency')
            plt.legend()

            plt.tight_layout()
            plt.show()
        else:
            print(f'No valid transformation found for column: {column_name}')

        return transformed_data  # Return the transformed data if not None
    
    def visualize_data(self, columns=None):
        if columns is None:
            columns = self.df.columns

        sns.pairplot(self.df[columns])
        plt.suptitle("Pair Plot of Data", y=1.02)
        plt.show()