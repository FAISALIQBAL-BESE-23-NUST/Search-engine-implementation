import os
import pandas as pd

def process_forward_index(dataset_dir, lexicon_dir, output_dir):
    """
    Process dataset chunks and their corresponding lexicon chunks to create a forward index.
    The forward index maps DocIDs (row numbers) to Word IDs for each document.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List all dataset chunks and lexicon chunks
    dataset_files = [f for f in os.listdir(dataset_dir) if f.endswith('.csv')]
    lexicon_files = [f for f in os.listdir(lexicon_dir) if f.endswith('_lexicon.csv')]
    dataset_files.sort()  # Ensure the files are processed in the correct order
    lexicon_files.sort()

    # Check if the number of dataset chunks matches the number of lexicon chunks
    if len(dataset_files) != len(lexicon_files):
        print("Mismatch between dataset chunks and lexicon chunks. Please check the directories.")
        return

    # Process each dataset chunk with its corresponding lexicon
    for dataset_file, lexicon_file in zip(dataset_files, lexicon_files):
        print(f"Processing {dataset_file} with {lexicon_file}...")

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
            forward_df = pd.DataFrame(forward_index)
            forward_file = os.path.join(output_dir, f"{os.path.splitext(dataset_file)[0]}_forward.csv")
            forward_df.to_csv(forward_file, index=False)
            print(f"Forward index for {dataset_file} saved to {forward_file}")

        except Exception as e:
            print(f"Error processing {dataset_file} with {lexicon_file}: {e}")

    print("All forward indices processed and saved.")

# Directories
dataset_dir = "DatasetChunks"
lexicon_dir = "Lexiconall"
output_dir = "ForwardIndex"

# Run the function
process_forward_index(dataset_dir, lexicon_dir, output_dir)
