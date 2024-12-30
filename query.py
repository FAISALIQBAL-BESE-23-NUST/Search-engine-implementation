import csv
import sys

# Increase CSV field size limit
csv.field_size_limit(sys.maxsize)  # Increase field size limit to handle large files

# Function to read the lexicon
def read_lexicon(lexicon_file):
    lexicon = {}
    with open(lexicon_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) == 2:
                word, word_id = row
                try:
                    lexicon[word] = int(word_id)
                except ValueError:
                    continue  # Skip invalid rows
    return lexicon

# Function to read the inverted index
def read_inverted_index(inverted_index_file):
    inverted_index = {}
    with open(inverted_index_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) == 2:
                word_id, doc_ids = row
                doc_id_list = list(map(int, doc_ids.split(',')))
                inverted_index[int(word_id)] = doc_id_list
    return inverted_index

# Function to read the forward index
def read_forward_index(forward_index_file):
    forward_index = {}
    with open(forward_index_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) == 2:
                doc_id, details = row
                forward_index[int(doc_id)] = details
    return forward_index

# Function to fetch the links of top 5 documents
def fetch_top_documents(word, lexicon, inverted_index, forward_index, dataset_file):
    # Normalize the input word
    word = word.strip().lower()

    # Step 1: Get Word ID from lexicon
    if word not in lexicon:
        print(f"The word '{word}' is not in the lexicon.")
        return []

    word_id = lexicon[word]

    # Step 2: Get document IDs from inverted index
    if word_id not in inverted_index:
        print(f"No documents found for the word '{word}'.")
        return []

    doc_ids = inverted_index[word_id]

    # Step 3: Get weights from the forward index
    doc_weights = []
    for doc_id in doc_ids:
        details = forward_index.get(doc_id, "")
        if details:
            # Split the details string to find the word ID and weight pairs
            pairs = details.split(',')
            for pair in pairs:
                wid, weight = map(int, pair.split(':'))
                if wid == word_id:  # Match the Word ID
                    doc_weights.append((doc_id, weight))

    # Step 4: Sort documents by weight in descending order
    doc_weights.sort(key=lambda x: x[1], reverse=True)

    # Step 5: Fetch links from the dataset for top 5 documents
    dataset = []
    with open(dataset_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dataset.append(row)

    top_docs = []
    for doc_id, weight in doc_weights[:5]:
        # Adjusting doc_id to fetch the (doc_id + 2)th row from the dataset
        row_num = doc_id + 2  # Add 2 to the doc_id to match the dataset row
        if row_num <= len(dataset):  # Ensure row_num is within bounds
            link = dataset[row_num - 1]['url']  # Fetch the URL (adjust for 0-based index)
            top_docs.append((link, weight))

    return top_docs

# Main program
def main():
    lexicon_file = 'Lexicon.csv'
    inverted_index_file = 'InvertedIndex.csv'
    forward_index_file = 'ForwardIndex.csv'
    dataset_file = 'ExtractedCleanedColumns.csv'

    # Load data
    print("Loading lexicon...")
    lexicon = read_lexicon(lexicon_file)
    print("Loading inverted index...")
    inverted_index = read_inverted_index(inverted_index_file)
    print("Loading forward index...")
    forward_index = read_forward_index(forward_index_file)

    # User input
    word = input("Enter a word to search: ")

    # Fetch top documents
    print("Fetching top documents...")
    top_docs = fetch_top_documents(word, lexicon, inverted_index, forward_index, dataset_file)

    # Display results
    if not top_docs:
        print("No results found.")
    else:
        print("Top 5 documents:")
        for link, weight in top_docs:
            print(f"Link: {link}, Weight: {weight}")

# Run the program
if __name__ == "__main__":
    main()
