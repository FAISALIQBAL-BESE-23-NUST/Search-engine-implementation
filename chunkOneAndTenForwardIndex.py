import os
import pandas as pd

def reprocess_forward_index(dataset_dir, lexicon_dir, output_dir, specific_pairs):
    """
    Reprocess specific dataset chunks with their correct lexicon chunks.
    """
    for dataset_file, lexicon_file in specific_pairs:
        print(f"Reprocessing {dataset_file} with {lexicon_file}...")

        dataset_path = os.path.join(dataset_dir, dataset_file)
        lexicon_path = os.path.join(lexicon_dir, lexicon_file)

        try:
            # Load the dataset chunk
            dataset_df = pd.read_csv(dataset_path)
            if dataset_df.empty:
                print(f"{dataset_file} is empty. Skipping.")
                continue

            # Load the lexicon chunk and create a word-to-ID mapping
            lexicon_df = pd.read_csv(lexicon_path)
            word_to_id = {row["Word"]: row["Word ID"] for _, row in lexicon_df.iterrows()}

            # Create the forward index
            forward_index = []
            for doc_id, row in dataset_df.iterrows():
                # Combine all text data in the row
                row_text = " ".join([str(row[col]) for col in dataset_df.columns if dataset_df[col].dtype == 'object'])
                words = row_text.split()

                # Map words to Word IDs
                word_ids = [word_to_id[word.lower()] for word in words if word.lower() in word_to_id]
                forward_index.append({"DocID": doc_id + 1, "WordIDs": word_ids})  # DocID starts from 1

            # Save the forward index to a CSV file
            forward_file = os.path.join(output_dir, f"{os.path.splitext(dataset_file)[0]}_forward.csv")
            forward_df = pd.DataFrame(forward_index)
            forward_df.to_csv(forward_file, index=False)
            print(f"Forward index for {dataset_file} reprocessed and saved to {forward_file}")

        except Exception as e:
            print(f"Error reprocessing {dataset_file} with {lexicon_file}: {e}")

# Directories
dataset_dir = "E:/dsapro/DatasetChunks"
lexicon_dir = "E:/dsapro/Lexicon"
output_dir = "E:/dsapro/ForwardIndex"

# Pairs of files to reprocess
specific_pairs = [
    ("chunk_1.csv", "chunk_1_lexicon.csv"),
    ("chunk_10.csv", "chunk_10_lexicon.csv")
]

# Run the reprocessing function
reprocess_forward_index(dataset_dir, lexicon_dir, output_dir, specific_pairs)
