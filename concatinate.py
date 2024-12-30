import pandas as pd
import sys

def print_progress(progress, total):
    """
    Print progress as a percentage.

    Parameters:
    progress (int): Current progress count.
    total (int): Total count.
    """
    percent = (progress / total) * 100
    sys.stdout.write(f"\rProgress: {percent:.2f}%")
    sys.stdout.flush()

def append_authors_to_columns(cleaned_file, root_words_file, output_file):
    """
    Append the 'authors' column from one CSV file to the 'root_word' and 'derived_words' columns of another CSV file.

    Parameters:
    cleaned_file (str): Path to the cleaned dataset CSV file (contains 'authors').
    root_words_file (str): Path to the root and derived words CSV file (contains 'root_word' and 'derived_words').
    output_file (str): Path to save the updated dataset.

    Returns:
    pd.DataFrame: Updated DataFrame with authors added to the root_word and derived_words columns.
    """
    # Load the datasets
    cleaned_df = pd.read_csv(cleaned_file)
    root_words_df = pd.read_csv(root_words_file)

    # Check if authors column exists
    if 'authors' not in cleaned_df.columns:
        raise ValueError("The 'authors' column is not present in the cleaned dataset.")

    # Check if root_word and derived_words columns exist
    if 'root_word' not in root_words_df.columns or 'derived_words' not in root_words_df.columns:
        raise ValueError("The 'root_word' or 'derived_words' column is not present in the root words dataset.")

    # Get the authors column
    authors = cleaned_df['authors'].dropna().tolist()

    # Add authors to the root_word and derived_words columns
    total_authors = len(authors)
    for idx, author in enumerate(authors, start=1):
        # Create a new row to add the author to both root_word and derived_words
        new_row = pd.DataFrame({'root_word': [author], 'derived_words': [author]})
        root_words_df = pd.concat([root_words_df, new_row], ignore_index=True)
        print_progress(idx, total_authors)

    print("\nAppending complete.")

    # Save the updated DataFrame to a new CSV file
    root_words_df.to_csv(output_file, index=False)

    return root_words_df

# Example usage
cleaned_csv = "output_no_repetitions.csv"  # Path to the cleaned dataset
root_words_csv = "root_and_derived_words.csv"  # Path to the root and derived words file
output_csv = "updated_with_authors.csv"  # Desired output file path

# Append authors to root_word and derived_words columns
updated_df = append_authors_to_columns(cleaned_csv, root_words_csv, output_csv)

# Print confirmation
print("Updated DataFrame saved to:", output_csv)
