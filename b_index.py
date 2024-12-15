import pandas as pd
from collections import defaultdict
import re
import chardet

def build_backward_index(dataset, specific_fields=None):
    """
    Build a backward index mapping each term to the list of document indices where it appears.
    
    :param dataset: The input dataset (Pandas DataFrame).
    :param specific_fields: Optional list of specific fields to consider for the backward index.
    :return: A dictionary mapping terms to lists of document indices.
    """
    backward_index = defaultdict(set)

    for index, row in dataset.iterrows():
        # Combine specific fields or all fields into a single string
        row_text = " ".join(row[specific_fields].astype(str)) if specific_fields else " ".join(row.astype(str))
        # Normalize the text (convert to lowercase and extract words)
        words = re.findall(r'\w+', row_text.lower(), re.UNICODE)
        # Map each word to the current document index
        for word in words:
            backward_index[word].add(index)

    # Convert sets to lists for final output
    return {word: list(indices) for word, indices in backward_index.items()}

def save_backward_index_to_csv(backward_index, output_file):
    """
    Save the backward index to a CSV file.
    
    :param backward_index: The backward index dictionary.
    :param output_file: The file path to save the backward index.
    """
    # Convert backward index to a DataFrame for easier saving
    backward_index_df = pd.DataFrame({
        "Term": list(backward_index.keys()),
        "Document_Indices": [",".join(map(str, indices)) for indices in backward_index.values()]
    })
    
    # Save the DataFrame to a CSV file
    backward_index_df.to_csv(output_file, index=False)
    print(f"Backward index saved to {output_file}")

def main():
    # File paths
    input_csv = "medium_articles.csv"  # Replace with your dataset path
    output_csv = "backward_index.csv"  # The output file for the backward index

    print("Loading dataset...")
    try:
        with open(input_csv, 'rb') as f:
            result = chardet.detect(f.read(10000))  # Detect file encoding
            encoding = result['encoding']
        dataset = pd.read_csv(input_csv, encoding=encoding)
    except FileNotFoundError:
        print(f"Error: File '{input_csv}' not found.")
        return

    # Build the backward index
    print("Building backward index...")
    backward_index = build_backward_index(dataset)

    # Save the backward index to a CSV file
    print("Saving backward index to CSV...")
    save_backward_index_to_csv(backward_index, output_csv)

if __name__ == "__main__":
    main()
