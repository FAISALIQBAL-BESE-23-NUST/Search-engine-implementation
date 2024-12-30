import pandas as pd
import re

def clean_text_column(text):
    """
    Clean a text column by replacing punctuation marks with spaces and converting to lowercase.

    Parameters:
    text (str): The text to clean.

    Returns:
    str: Cleaned text.
    """
    if pd.isnull(text):
        return text
    # Replace punctuation with spaces and convert to lowercase
    return re.sub(r'[\W_]+', ' ', text).lower()

def clean_list_column(column):
    """
    Clean a column containing lists represented as strings by removing punctuation marks and converting to lowercase.

    Parameters:
    column (str): The column value to clean.

    Returns:
    str: Cleaned list as a string.
    """
    if pd.isnull(column):
        return column
    # Remove brackets, clean individual elements, and convert to lowercase
    column = re.sub(r'[\[\]\'"\s]+', ' ', column)
    return re.sub(r'[\W_]+', ' ', column).lower()

def clean_and_extract_columns(input_file, output_file, extracted_file):
    """
    Load a CSV file, clean specific columns, save the cleaned dataset, and extract cleaned columns to a separate file.

    Parameters:
    input_file (str): Path to the input CSV file.
    output_file (str): Path to save the cleaned CSV file.
    extracted_file (str): Path to save the extracted cleaned columns.

    Returns:
    pd.DataFrame: The cleaned and extracted DataFrame.
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

    # Extract and save cleaned columns
    extracted_df = df[['title', 'tags', 'authors', 'text']]
    extracted_df.to_csv(extracted_file, index=False)

    return extracted_df

# Example usage
input_csv = "first_50000_rows.csv"  # Replace with your input file path
output_csv = "cleaned_dataset.csv"  # Replace with your desired output file path
extracted_csv = "extracted_cleaned_columns.csv"  # Replace with your desired extracted file path

# Clean the dataset and extract columns
extracted_data = clean_and_extract_columns(input_csv, output_csv, extracted_csv)
