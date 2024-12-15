import pandas as pd
from collections import defaultdict
import re
import chardet

def build_forward_index(dataset, specific_fields=None):
    """
    Build a forward index mapping each document index to the list of terms it contains.
    
    :param dataset: The input dataset (Pandas DataFrame).
    :param specific_fields: Optional list of specific fields to consider for the forward index.
    :return: A dictionary mapping document indices to lists of terms.
    """
    forward_index = {}

    for index, row in dataset.iterrows():
        # Combine specific fields or all fields into a single string
        row_text = " ".join(row[specific_fields].astype(str)) if specific_fields else " ".join(row.astype(str))
        # Normalize the text (convert to lowercase and extract words)
        words = re.findall(r'\w+', row_text.lower(), re.UNICODE)
        # Map the document index to the list of words (terms)
        forward_index[index] = words

    return forward_index

def save_forward_index_to_csv(forward_index, output_file):
    """
    Save the forward index to a CSV file.
    
    :param forward_index: The forward index dictionary.
    :param output_file: The file path to save the forward index.
    """
    # Convert forward index to a DataFrame for easier saving
    forward_index_df = pd.DataFrame({
        "Document_Index": list(forward_index.keys()),
        "Terms": [",".join(terms) for terms in forward_index.values()]
    })
    
    # Save the DataFrame to a CSV file
    forward_index_df.to_csv(output_file, index=False)
    print(f"Forward index saved to {output_file}")

def main():
    # File paths
    input_csv = "medium_articles.csv"  # Replace with your dataset path
    output_csv = "forward_index.csv"   # The output file for the forward index

    print("Loading dataset...")
    try:
        with open(input_csv, 'rb') as f:
            result = chardet.detect(f.read(10000))  # Detect file encoding
            encoding = result['encoding']
        dataset = pd.read_csv(input_csv, encoding=encoding)
    except FileNotFoundError:
        print(f"Error: File '{input_csv}' not found.")
        return

    # Build the forward index
    print("Building forward index...")
    forward_index = build_forward_index(dataset)

    # Save the forward index to a CSV file
    print("Saving forward index to CSV...")
    save_forward_index_to_csv(forward_index, output_csv)

if __name__ == "__main__":
    main()
