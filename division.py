import pandas as pd

def load_first_50000_rows(input_file, output_file=None):
    """
    Load the first 50,000 rows of a CSV file and optionally save them to a new file.

    Parameters:
    input_file (str): Path to the input CSV file.
    output_file (str, optional): Path to save the first 50,000 rows to a new CSV file. Default is None.

    Returns:
    pd.DataFrame: DataFrame containing the first 50,000 rows of the input file.
    """
    # Load only the first 50,000 rows
    df = pd.read_csv(input_file, nrows=50000)

    # Optionally save to a new CSV file
    if output_file:
        df.to_csv(output_file, index=False)

    return df

# Example usage
input_csv = "medium_articles.csv"  # Replace with your input file path
output_csv = "first_50000_rows.csv"  # Replace with your desired output file path

# Load and optionally save the first 50,000 rows
data = load_first_50000_rows(input_csv, output_csv)
