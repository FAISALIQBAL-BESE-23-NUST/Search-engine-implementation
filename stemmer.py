import pandas as pd
from nltk.stem import PorterStemmer
from collections import defaultdict
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

def find_root_and_derived_words(input_file, output_file):
    """
    Process a CSV file to find root words and their derived words from specified columns.

    Parameters:
    input_file (str): Path to the input CSV file.
    output_file (str): Path to save the processed CSV file with root and derived words.

    Returns:
    pd.DataFrame: DataFrame containing root words and their derived words.
    """
    # Load the cleaned dataset
    df = pd.read_csv(input_file)

    # Initialize the stemmer
    ps = PorterStemmer()

    # Initialize a dictionary to store root words and their derived words
    root_to_words = defaultdict(set)

    # Get the total number of rows to process
    total_rows = len(df)

    # Process the title, text, and tags columns
    for col in ['title', 'text', 'tags']:
        if col in df.columns:
            for idx, entry in enumerate(df[col].dropna(), 1):
                words = entry.split()  # Split the text into words
                for word in words:
                    root = ps.stem(word)  # Find the root word
                    root_to_words[root].add(word)  # Add the original word to the root's set of derived words
                # Update progress
                print_progress(idx, total_rows)

    print("\nProcessing complete.")

    # Prepare the root and derived words for output
    root_words = []
    derived_words = []
    for root, words in root_to_words.items():
        root_words.append(root)
        derived_words.append(', '.join(sorted(words)))

    # Create a DataFrame with the root and derived words
    result_df = pd.DataFrame({
        'root_word': root_words,
        'derived_words': derived_words
    })

    # Save the result to a CSV file
    result_df.to_csv(output_file, index=False)

    return result_df

# Example usage
input_csv = "extracted_cleaned_columns.csv"  # Replace with the path to the cleaned dataset
output_csv = "root_and_derived_words.csv"  # Replace with the desired output file path

# Find root and derived words
result = find_root_and_derived_words(input_csv, output_csv)
