import os
import pandas as pd
import json
from collections import defaultdict

def create_barrels_with_metadata(lexicon_dir, inverted_index_dir, dataset_dir, output_file):
    # Track progress
    print("Starting barrel creation...")

    # Initialize the barrel data
    barrel_data = []

    # Step 1: Iterate through each chunk of the inverted index
    inverted_files = sorted([f for f in os.listdir(inverted_index_dir) if f.endswith('_inverted.csv')])
    lexicon_files = sorted([f for f in os.listdir(lexicon_dir) if f.endswith('_lexicon.csv')])

    for inv_file, lex_file in zip(inverted_files, lexicon_files):
        print(f"Processing inverted index chunk: {inv_file} with lexicon: {lex_file}...")

        # Load inverted index and lexicon
        inv_path = os.path.join(inverted_index_dir, inv_file)
        lex_path = os.path.join(lexicon_dir, lex_file)
        inverted_df = pd.read_csv(inv_path)
        lexicon_df = pd.read_csv(lex_path)

        # Create a dictionary to map WordID to words
        word_map = dict(zip(lexicon_df["Word ID"], lexicon_df["Word"]))

        # Step 2: Process each WordID in the inverted index
        for _, row in inverted_df.iterrows():
            word_id = row["Word ID"]
            doc_ids = eval(row["Document IDs"])

            word = word_map.get(word_id, "Unknown")

            # Collect document-specific metadata for this WordID
            document_info = []

            for doc_id in doc_ids:
                # Locate the dataset chunk containing this DocID
                dataset_chunk_file = f"dataset_chunk_{doc_id // 1000}.csv"  # Adjust based on chunk naming
                dataset_chunk_path = os.path.join(dataset_dir, dataset_chunk_file)

                if os.path.exists(dataset_chunk_path):
                    dataset_df = pd.read_csv(dataset_chunk_path)

                    # Find the row corresponding to the DocID
                    doc_row = dataset_df[dataset_df["DocID"] == doc_id]

                    if not doc_row.empty:
                        doc_row = doc_row.iloc[0]
                        text = doc_row["Text"]
                        author = doc_row["Author"]
                        title = doc_row["Title"]
                        url = doc_row["URL"]
                        tags = doc_row["Tags"]

                        # Calculate frequencies
                        text_freq = text.lower().split().count(word) if pd.notna(text) else 0
                        author_freq = author.lower().split().count(word) if pd.notna(author) else 0
                        title_freq = title.lower().split().count(word) if pd.notna(title) else 0
                        url_freq = url.lower().split().count(word) if pd.notna(url) else 0
                        tags_freq = tags.lower().split().count(word) if pd.notna(tags) else 0

                        # Add document info
                        document_info.append({
                            "DocID": doc_id,
                            "Positions": [],  # Assuming position extraction happens elsewhere
                            "TextFreq": text_freq,
                            "AuthorFreq": author_freq,
                            "TitleFreq": title_freq,
                            "URLFreq": url_freq,
                            "TagsFreq": tags_freq
                        })

            # Step 3: Append the aggregated data to the barrel
            barrel_data.append({
                "Word": word,
                "WordID": word_id,
                "DocumentInfo": json.dumps(document_info)
            })

        print(f"Finished processing {inv_file}.")

    # Step 4: Save the barrel to a CSV file
    print("Saving the barrel to CSV...")
    barrel_df = pd.DataFrame(barrel_data)
    barrel_df.to_csv(output_file, index=False)
    print(f"Barrel saved to {output_file}.")

# Directory paths
lexicon_directory = "E:/dsapro/Lexicon"
inverted_index_directory = "E:/dsapro/InvertedIndex"
dataset_directory = "E:/dsapro/DatasetChunks"
output_file_path = "E:/dsapro/Barrel.csv"

# Run the function
create_barrels_with_metadata(lexicon_directory, inverted_index_directory, dataset_directory, output_file_path)
