import pandas as pd
from collections import defaultdict
import re

def build_lexicon(dataset, specific_fields=None):
    """
    Build a lexicon mapping each term to its metadata (row indices where it appears).

    :param dataset: The input dataset (Pandas DataFrame).
    :param specific_fields: Optional list of specific fields to consider for lexicon creation.
    :return: A dictionary mapping terms to metadata (list of row indices).
    """
    lexicon = defaultdict(set)  # Use a set for faster duplicate handling

    for index, row in dataset.iterrows():
        # Concatenate specific fields or all fields
        row_text = " ".join(row[specific_fields].astype(str) if specific_fields else row.astype(str))

        # Normalize the text and extract words
        words = re.findall(r'\w+', row_text.lower(), re.UNICODE)

        # Add terms to the lexicon
        for word in words:
            lexicon[word].add(index)

    # Convert sets to lists for final output
    return {word: list(indices) for word, indices in lexicon.items()}

def build_lexicon_from_csv(file_path, specific_fields=None, chunksize=5000):
    """
    Build a lexicon from a large CSV file by processing it in chunks.

    :param file_path: Path to the input CSV file.
    :param specific_fields: Optional list of specific fields to consider for lexicon creation.
    :param chunksize: Number of rows to process in each chunk.
    :return: A dictionary mapping terms to metadata (list of row indices).
    """
    lexicon = defaultdict(set)

    # Process the file in chunks
    for chunk in pd.read_csv(file_path, chunksize=chunksize, encoding='ISO-8859-1'):
        partial_lexicon = build_lexicon(chunk, specific_fields)
        for word, indices in partial_lexicon.items():
            lexicon[word].update(indices)

    # Convert sets to lists for final output
    return {word: list(indices) for word, indices in lexicon.items()}

def save_lexicon_to_csv(lexicon, output_file):
    """
    Save the lexicon to a CSV file.

    :param lexicon: The lexicon dictionary mapping terms to metadata.
    :param output_file: Path to the output CSV file.
    """
    lexicon_df = pd.DataFrame({
        "Term": list(lexicon.keys()),
        "Metadata": [",".join(map(str, indices)) for indices in lexicon.values()]
    })

    lexicon_df.to_csv(output_file, index=False)
    print(f"Lexicon saved to {output_file}")

def main():
    # File paths
    input_csv = "medium_articles.csv"  # Replace with the path to your dataset
    output_csv = "lexicon.csv"         # The output file for the lexicon

    # Build lexicon from CSV in chunks
    print("Building lexicon...")
    lexicon = build_lexicon_from_csv(input_csv, specific_fields=None)

    # Save the lexicon to CSV
    print("Saving lexicon to CSV...")
    save_lexicon_to_csv(lexicon, output_csv)

if __name__ == "__main__":
    main()
