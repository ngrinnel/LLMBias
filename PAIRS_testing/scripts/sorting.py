import pandas as pd
import numpy as np

def sort_words_by_category(input_csv, output_csv):
    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Replace '-inf' with a very large negative number for sorting
    df.replace(-np.inf, -1e9, inplace=True)

    # Create a new DataFrame with columns for each category's sorted words and their corresponding values
    sorted_words_values_df = pd.DataFrame()

    for column in df.columns[1:]:
        sorted_column = df.sort_values(by=column, ascending=False)
        sorted_words_values_df[f'{column}_words'] = sorted_column['Unnamed: 0'].reset_index(drop=True)
        sorted_words_values_df[f'{column}_values'] = sorted_column[column].reset_index(drop=True)

    # Revert the very large negative number back to '-inf'
    sorted_words_values_df.replace(-1e9, -np.inf, inplace=True)

    # Save the sorted DataFrame to a new CSV file
    sorted_words_values_df.to_csv(output_csv, index=False)

# Example usage
input_csv = 'window_pmi_scores_ernie.csv'  # Input CSV file path
output_csv = 'sorted_window_pmi_scores_ernie.csv'  # Output CSV file path

sort_words_by_category(input_csv, output_csv)
