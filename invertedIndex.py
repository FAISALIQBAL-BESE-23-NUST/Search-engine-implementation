import csv
import pandas as pd
import re
from collections import defaultdict

# Function to read lexicon from a file and create a dictionary (Word -> WordID)
def read_lexicon(lexicon_file):
    lexicon = {}
    with open(lexicon_file, 'r', encoding='utf-8', errors='ignore') as f:  # Specify encoding and error handling
        reader = csv.reader(f)
        next(reader)  # Skip the header row (if present)
        for row in reader:
            if len(row) == 2:
                word, word_id = row
                try:
                    # Try to convert WordID to an integer
                    lexicon[word] = int(word_id)
                except ValueError:
                    print(f"Skipping invalid row: {row}")  # Handle invalid rows gracefully
    return lexicon

# Function to read the dataset from a CSV file
def read_dataset(dataset_file):
    return pd.read_csv(dataset_file)

# Function to generate an inverted index
def generate_inverted_index(dataset, lexicon):
    inverted_index = defaultdict(list)
    
    # Process each document
    for doc_id, row in dataset.iterrows():
        title, tags, authors, text = row['title'], row['tags'], row['authors'], row['text']
        
        # Combine all fields to process the entire document text
        full_text = f"{title} {tags} {authors} {text}"
        
        # Split the text into words and clean each word
        words = full_text.split()
        
        # Normalize words by removing non-alphabetic characters
        for word in words:
            # Clean the word by removing non-alphabetical characters
            cleaned_word = re.sub(r'[^a-zA-Z]', '', word).lower()  # Remove non-alphabetical chars and lower the case
            
            # If the cleaned word exists in the lexicon, add the document ID to the inverted index
            if cleaned_word in lexicon:
                word_id = lexicon[cleaned_word]
                if doc_id not in inverted_index[word_id]:
                    inverted_index[word_id].append(doc_id)
    
    return inverted_index

# Function to save the inverted index to a CSV file
def write_inverted_index(inverted_index, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["WordID", "DocIDs"])  # Header
        for word_id, doc_ids in inverted_index.items():
            # Convert doc_ids list to a comma-separated string
            writer.writerow([word_id, ",".join(map(str, doc_ids))])

# Main function to read files and process them
def main(lexicon_file, dataset_file, output_file):
    # Read the lexicon and dataset
    lexicon = read_lexicon(lexicon_file)
    dataset = read_dataset(dataset_file)

    # Generate the inverted index
    inverted_index = generate_inverted_index(dataset, lexicon)

    # Write the inverted index to the output CSV
    write_inverted_index(inverted_index, output_file)
    print(f"Inverted index generated and saved to {output_file}")


lexicon_file = 'Lexicon.csv'  
dataset_file = 'ExtractedCleanedColumns.csv'  
output_file = 'InvertedIndex.csv'  
main(lexicon_file, dataset_file, output_file)
