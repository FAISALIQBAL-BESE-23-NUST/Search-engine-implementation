import csv
import pandas as pd
from collections import defaultdict

# Function to read lexicon from a file and create a dictionary (Word -> WordID)
def read_lexicon(lexicon_file):
    lexicon = {}
    with open(lexicon_file, 'r', encoding='utf-8') as f:  # Set encoding to utf-8
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

# Function to generate the forward index
def generate_forward_index(dataset, lexicon):
    forward_index = []

    # Iterate through the dataset and process each document
    for doc_id, row in dataset.iterrows():
        title, tags, authors, text = row['title'], row['tags'], row['authors'], row['text']
        
        # Ensure all columns are treated as strings (convert if necessary)
        title = str(title) if isinstance(title, str) else ""
        tags = str(tags) if isinstance(tags, str) else ""
        authors = str(authors) if isinstance(authors, str) else ""
        text = str(text) if isinstance(text, str) else ""

        # Create a dictionary to store word frequencies in each section
        word_count = defaultdict(lambda: {'n': 0, 'o': 0, 'p': 0, 'm': 0})
        
        # Count occurrences in title
        for word in title.split():
            if word in lexicon:
                word_count[word]['n'] += 1
        
        # Count occurrences in authors
        for word in authors.split():
            if word in lexicon:
                word_count[word]['o'] += 1
        
        # Count occurrences in tags
        for word in tags.split():
            if word in lexicon:
                word_count[word]['p'] += 1
        
        # Count occurrences in text
        for word in text.split():
            if word in lexicon:
                word_count[word]['m'] += 1
        
        # Create the details string with WordID:Weight pairs
        details = []
        for word, counts in word_count.items():
            # Calculate the weight
            weight = 4 * counts['n'] + 3 * counts['o'] + 2 * counts['p'] + counts['m']
            if weight > 0:  # Only include words with a non-zero weight
                if word in lexicon:  # Ensure the word is in lexicon before adding
                    word_id = lexicon[word]  # Get the word ID from the lexicon
                    details.append(f"{word_id}:{weight}")
        
        # Add the row to the forward index
        forward_index.append([doc_id, ",".join(details)])

    return forward_index

# Function to write the forward index to a CSV file
def write_forward_index(forward_index, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["DocID", "Details"])  # Header
        writer.writerows(forward_index)

# Main function to read files and process them
def main(lexicon_file, dataset_file, output_file):
    # Read the lexicon and dataset
    lexicon = read_lexicon(lexicon_file)
    dataset = read_dataset(dataset_file)

    # Generate the forward index
    forward_index = generate_forward_index(dataset, lexicon)

    # Write the forward index to the output CSV
    write_forward_index(forward_index, output_file)
    print(f"Forward index generated and saved to {output_file}")

# Example usage:
lexicon_file = 'Lexicon.csv'  
dataset_file = 'ExtractedCleanedColumns.csv'  
output_file = 'ForwardIndex.csv'
main(lexicon_file, dataset_file, output_file) 
