import pandas as pd
from collections import defaultdict


def create_inverted_index(roots_file, root_lexicon_file, dataset_file, output_file):
    """
    Create an inverted index mapping root word IDs to document IDs based on derived words.

    Parameters:
    roots_file (str): Path to the roots and derived words file.
    root_lexicon_file (str): Path to the root words lexicon file.
    dataset_file (str): Path to the dataset containing text, title, authors, and tags.
    output_file (str): Path to save the inverted index.

    Returns:
    dict: Inverted index mapping root word IDs to document IDs.
    """
    # Load the roots and derived words mapping
    roots_df = pd.read_csv(roots_file)
    root_lexicon_df = pd.read_csv(root_lexicon_file)
    dataset_df = pd.read_csv(dataset_file)

    # Create a dictionary for root word lexicon
    root_word_to_id = dict(zip(root_lexicon_df['word'], root_lexicon_df['id']))

    # Create a mapping of derived words to root words
    derived_to_root = {}
    for _, row in roots_df.iterrows():
        root_word = row['root_word']
        derived_words = row['derived_words'].split(', ')
        for derived_word in derived_words:
            derived_to_root[derived_word] = root_word

    # Initialize the inverted index
    inverted_index = defaultdict(set)

    # Process each document in the dataset
    total_docs = len(dataset_df)
    for idx, row in dataset_df.iterrows():
        doc_id = idx + 1  # Assign the row number as the document ID
        combined_text = f"{row['text']} {row['title']} {row['authors']} {row['tags']}"
        words = combined_text.split()

        for word in words:
            if word in derived_to_root:  # Check if the word is a derived word
                root_word = derived_to_root[word]

                if root_word in root_word_to_id:  # Check if the root word has a word ID
                    root_word_id = root_word_to_id[root_word]
                    inverted_index[root_word_id].add(doc_id)

        # Print progress as a percentage
        progress = ((idx + 1) / total_docs) * 100
        print(f"\rProgress: {progress:.2f}%", end='')

    print("\nProcessing complete.")

    # Convert sets to sorted lists for consistent output
    inverted_index = {key: sorted(value) for key, value in inverted_index.items()}

    # Save the inverted index to a file
    inverted_index_df = pd.DataFrame([
        {'root_word_id': root_id, 'doc_ids': ', '.join(map(str, doc_ids))}
        for root_id, doc_ids in inverted_index.items()
    ])
    inverted_index_df.to_csv(output_file, index=False)

    return inverted_index

# Example usage
roots_csv = "updated_with_authors.csv"  # Path to the roots and derived words file
root_lexicon_csv = "root_lexicon.csv"  # Path to the root words lexicon file
dataset_csv = "extracted_cleaned_columns.csv"  # Path to the dataset containing document IDs and text
output_csv = "inverted_index.csv"  # Path to save the inverted index

# Create the inverted index
inverted_index = create_inverted_index(roots_csv, root_lexicon_csv, dataset_csv, output_csv)
