import pandas as pd
from collections import defaultdict
import re

def build_forward_index(dataset, specific_fields=None):
    """
    Build a forward index from a dataset (CSV file).
    
    :param dataset: The input dataset (Pandas DataFrame).
    :param specific_fields: Optional list of specific fields to consider for indexing.
    :return: A dictionary mapping Doc_IDs to lists of terms.
    """
    forward_index = {}

    for index, row in dataset.iterrows():
        # Combine specific fields or all fields into a single string
        row_text = " ".join(row[specific_fields].astype(str) if specific_fields else row.astype(str))
        # Normalize the text (convert to lowercase and extract words)
        terms = re.findall(r'\w+', row_text.lower(), re.UNICODE)
        
        # Add the terms to the forward index with Doc_ID as the key
        forward_index[index] = terms

    return forward_index

def save_forward_index_to_csv(forward_index, output_file):
    """
    Save the forward index to a CSV file.
    
    :param forward_index: The forward index dictionary.
    :param output_file: Path to the output CSV file.
    """
    try:
        # Convert the forward index to a DataFrame for saving
        forward_index_df = pd.DataFrame({
            "Doc_ID": list(forward_index.keys()),
            "Terms": [" ".join(terms) for terms in forward_index.values()]
        })
        
        # Save the DataFrame to a CSV file
        forward_index_df.to_csv(output_file, index=False)
        print(f"Forward index saved to {output_file}")
    except Exception as e:
        print(f"Error while saving forward index: {e}")

def main():
    # File paths
    input_csv = "medium_articles.csv"  # Path to the dataset
    output_csv = "forward_index.csv"  # Output file for forward index

    # Load the dataset
    print("Loading dataset...")
    try:
        dataset = pd.read_csv(input_csv, encoding='ISO-8859-1')
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
