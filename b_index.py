import pandas as pd
from collections import defaultdict
import re

def build_backward_index(dataset, specific_fields=None):
    """
    Build a backward index (inverted index) from a dataset.
    
    :param dataset: The input dataset (Pandas DataFrame).
    :param specific_fields: Optional list of specific fields to consider for building the index.
    :return: A dictionary mapping terms to lists of document indices (backward index).
    """
    backward_index = defaultdict(set)

    for index, row in dataset.iterrows():
        # Combine specific fields or all fields into a single string
        row_text = " ".join(row[specific_fields].astype(str) if specific_fields else row.astype(str))
        # Normalize the text (convert to lowercase and extract words)
        words = re.findall(r'\w+', row_text.lower(), re.UNICODE)
        
        # Map each word to the current row index
        for word in words:
            backward_index[word].add(index)

    # Convert sets to lists for the final output
    return {word: list(indices) for word, indices in backward_index.items()}

def save_backward_index_to_csv(backward_index, output_csv):
    """
    Save the backward index to a CSV file.
    
    :param backward_index: The backward index (dictionary mapping terms to document lists).
    :param output_csv: Path to save the CSV file.
    """
    # Convert backward index to a DataFrame
    backward_index_df = pd.DataFrame({
        "Term": list(backward_index.keys()),
        "Doc_Indices": [",".join(map(str, indices)) for indices in backward_index.values()]
    })

    # Save the DataFrame to a CSV file
    backward_index_df.to_csv(output_csv, index=False)
    print(f"Backward index saved to {output_csv}")

def main():
    # File paths
    input_csv = "medium_articles.csv"  # Replace with the path to your dataset
    output_csv = "backward_index.csv"  # The output file for the backward index

    # Load the dataset
    print("Loading dataset...")
    try:
        dataset = pd.read_csv(input_csv, encoding='ISO-8859-1')  # Adjust encoding if needed
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
