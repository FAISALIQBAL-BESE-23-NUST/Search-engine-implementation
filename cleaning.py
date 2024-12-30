import pandas as pd
import re

def clean_text_column(text):
    """
    Clean a text column by replacing punctuation marks with spaces.

    Parameters:
    text (str): The text to clean.

    Returns:
    str: Cleaned text.
    """
    if pd.isnull(text):
        return text
    # Replace punctuation with spaces
    return re.sub(r'[\W_]+', ' ', text)

def clean_list_column(column):
    """
    Clean a column containing lists represented as strings by removing punctuation marks.

    Parameters:
    column (str): The column value to clean.

    Returns:
    str: Cleaned list as a string.
    """
    if pd.isnull(column):
        return column
    # Remove brackets and clean individual elements
    column = re.sub(r'[\[\]\'"\s]+', ' ', column)
    return re.sub(r'[\W_]+', ' ', column)

def clean_dataset(input_file, output_file):
    """
    Load a CSV file, clean specific columns, and save the cleaned dataset.

    Parameters:
    input_file (str): Path to the input CSV file.
    output_file (str): Path to save the cleaned CSV file.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    # Load the first 50,000 rows
    df = pd.read_csv(input_file, nrows=50000)

    # Clean specific columns
    if 'title' in df.columns:
        df['title'] = df['title'].apply(clean_text_column)

    if 'tags' in df.columns:
        df['tags'] = df['tags'].apply(clean_list_column)

    if 'authors' in df.columns:
        df['authors'] = df['authors'].apply(clean_list_column)

    if 'text' in df.columns:
        df['text'] = df['text'].apply(clean_text_column)

    # Save the cleaned dataset
    df.to_csv(output_file, index=False)

    return df

# Example usage
input_csv = "first_50000_rows.csv"  # Replace with your input file path
output_csv = "cleaned_dataset.csv"  # Replace with your desired output file path

# Clean the dataset
cleaned_data = clean_dataset(input_csv, output_csv)
