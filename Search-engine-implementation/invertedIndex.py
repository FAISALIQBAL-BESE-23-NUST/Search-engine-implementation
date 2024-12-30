import os
import pandas as pd
from collections import defaultdict

def create_inverted_index(lexicon_dir, forward_index_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List all lexicon and forward index files
    lexicon_files = sorted([f for f in os.listdir(lexicon_dir) if f.endswith('_lexicon.csv')])
    forward_files = sorted([f for f in os.listdir(forward_index_dir) if f.endswith('_forward.csv')])

    # Process each chunk
    for lexicon_file, forward_file in zip(lexicon_files, forward_files):
        print(f"Processing {lexicon_file} with {forward_file}...")

        # Read the lexicon file
        lexicon_path = os.path.join(lexicon_dir, lexicon_file)
        lexicon_df = pd.read_csv(lexicon_path)
        word_ids = lexicon_df["Word ID"].tolist()

        # Initialize inverted index
        inverted_index = defaultdict(set)  # Use a set to avoid duplicate DocIDs

        # Read the forward index file
        forward_path = os.path.join(forward_index_dir, forward_file)
        forward_df = pd.read_csv(forward_path)

        # Build the inverted index
        for _, row in forward_df.iterrows():
            doc_id = row["DocID"]
            word_ids_in_doc = eval(row["WordIDs"])  # Convert string back to list
            for word_id in word_ids_in_doc:
                inverted_index[word_id].add(doc_id)  # Add doc_id to the set

        # Prepare the inverted index data for saving
        inverted_data = {
            "Word ID": [],
            "Document IDs": []
        }
        for word_id in sorted(inverted_index.keys()):
            inverted_data["Word ID"].append(word_id)
            inverted_data["Document IDs"].append(list(inverted_index[word_id]))  # Convert set back to list

        # Save the inverted index to a CSV file
        inverted_df = pd.DataFrame(inverted_data)
        output_file = os.path.join(output_dir, f"{os.path.splitext(lexicon_file)[0]}_inverted.csv")
        inverted_df.to_csv(output_file, index=False)
        print(f"Inverted index for {lexicon_file} saved to {output_file}")

    print("All inverted indices processed and saved.")

# Directory paths
lexicon_directory = "Lexiconall"
forward_index_directory = "ForwardIndex"
output_directory = "InvertedIndex"

# Run the function
create_inverted_index(lexicon_directory, forward_index_directory, output_directory)
