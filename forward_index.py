import pandas as pd
import nltk
import string
import sys

# Load datasets
main_dataset = pd.read_csv('extracted_cleaned_columns.csv')  # Columns: title, author, tags, text
derived_lexicon = pd.read_csv('derived_lexicon.csv')  # Columns: word, id

# Preprocessing and weights
column_weights = {'title': 4, 'authors': 3, 'tags': 2, 'text': 1}

# Function to preprocess text (tokenize, remove punctuation, lowercase)
def preprocess_text(text):
    translator = str.maketrans('', '', string.punctuation)
    tokens = nltk.word_tokenize(text.translate(translator).lower())
    return tokens

# Create word-to-ID mapping
word_to_id = dict(zip(derived_lexicon['word'].str.lower(), derived_lexicon['id']))

# Progress display function
def show_progress(current, total):
    progress = (current / total) * 100
    sys.stdout.write(f"\rProcessing: {progress:.2f}% complete")
    sys.stdout.flush()

# Build the forward index
forward_index = []
total_rows = len(main_dataset)

for idx, row in main_dataset.iterrows():
    word_weights = {}

    # Process each column and calculate weighted frequencies
    for column, weight in column_weights.items():
        if pd.notna(row[column]):  # Ensure the column isn't NaN
            tokens = preprocess_text(row[column])
            for token in tokens:
                if token in word_to_id:  # Check if word exists in derived_lexicon
                    word_id = word_to_id[token]
                    if word_id not in word_weights:
                        word_weights[word_id] = 0
                    word_weights[word_id] += weight  # Add weighted frequency

    # Construct the "Details" column
    details = ",".join([f"{word_id}:{weight}" for word_id, weight in word_weights.items()])

    # Append to forward index
    forward_index.append({'DocID': idx + 1, 'Details': details})

    # Update progress
    show_progress(idx + 1, total_rows)

# Convert forward index to DataFrame
forward_index_df = pd.DataFrame(forward_index)

# Save the forward index to a CSV file
forward_index_df.to_csv('ForwardIndex.csv', index=False)

print("\nForward Index created successfully and saved as 'ForwardIndex.csv'")
