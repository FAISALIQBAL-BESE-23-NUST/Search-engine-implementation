import pandas as pd

def remove_repetitions_in_column(input_file, output_file, column_name):
    """
    Remove repetitions in a specified column of a CSV file.

    Parameters:
    input_file (str): Path to the input CSV file.
    output_file (str): Path to save the updated CSV file.
    column_name (str): The name of the column to process.

    Returns:
    pd.DataFrame: DataFrame with repetitions removed from the specified column.
    """
    # Load the CSV file
    df = pd.read_csv(input_file)

    # Ensure the specified column exists
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the CSV file.")

    # Remove duplicates from the column
    df = df.drop_duplicates(subset=[column_name])

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    return df

# Example usage
input_csv = "author_file.csv"  # Path to the input CSV file
output_csv = "output_no_repetitions.csv"  # Desired output file path
column_to_process = "authors"  # Column to remove repetitions from

# Process the CSV file
updated_df = remove_repetitions_in_column(input_csv, output_csv, column_to_process)

# Print confirmation
print("Updated CSV saved to:", output_csv)
