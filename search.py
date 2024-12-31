import csv
import sys
from collections import defaultdict

# Increase CSV field size limit
csv.field_size_limit(10000000)  # Handle large files

# Function to read a lexicon (root or derived)
def read_lexicon(lexicon_file):
    lexicon = {}
    with open(lexicon_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) == 2:
                word, word_id = row
                try:
                    lexicon[word.strip().lower()] = int(word_id)
                except ValueError:
                    continue  # Skip invalid rows
    return lexicon

# Function to read the inverted index
def read_inverted_index(inverted_index_file):
    inverted_index = defaultdict(list)
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

# Function to process a multiword query
def process_query(query, root_lexicon, derived_lexicon):
    words = query.lower().split()
    word_ids = []
    for word in words:
        if word in root_lexicon:
            word_ids.append(root_lexicon[word])
        elif word in derived_lexicon:
            word_ids.append(derived_lexicon[word])
    return word_ids

# Function to fetch documents and calculate total weights for multiword queries
def fetch_documents(word_ids, inverted_index, forward_index):
    doc_weights = defaultdict(int)

    for word_id in word_ids:
        if word_id not in inverted_index:
            continue

        doc_ids = inverted_index[word_id]
        for doc_id in doc_ids:
            details = forward_index.get(doc_id, "")
            if details:
                pairs = details.split(',')
                for pair in pairs:
                    wid, weight = map(int, pair.split(':'))
                    if wid == word_id:
                        doc_weights[doc_id] += weight

    # Sort by weight in descending order
    sorted_docs = sorted(doc_weights.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs

# Function to fetch URLs from the dataset
def fetch_urls(dataset_file, sorted_docs):
    dataset = []
    with open(dataset_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dataset.append(row)

    results = []
    for doc_id, weight in sorted_docs:
        row_num = doc_id  # Convert 1-based docID to 0-based index
        if 0 <= row_num < len(dataset):
            url = dataset[row_num]['url']
            results.append((doc_id, weight, url))

    return results

# Main program
def main():
    root_lexicon_file = 'root_lexicon.csv'
    derived_lexicon_file = 'derived_lexicon.csv'
    inverted_index_file = 'inverted_index.csv'
    forward_index_file = 'ForwardIndex.csv'
    dataset_file = 'first_50000_rows.csv'

    # Load lexicons
    print("Loading root lexicon...")
    root_lexicon = read_lexicon(root_lexicon_file)

    print("Loading derived lexicon...")
    derived_lexicon = read_lexicon(derived_lexicon_file)

    # Load inverted and forward indexes
    print("Loading inverted index...")
    inverted_index = read_inverted_index(inverted_index_file)

    print("Loading forward index...")
    forward_index = read_forward_index(forward_index_file)

    # User input
    query = input("Enter your search query (multiword supported): ")

    # Process query
    print("Processing query...")
    word_ids = process_query(query, root_lexicon, derived_lexicon)

    if not word_ids:
        print("No valid words found in the query.")
        return

    # Fetch documents
    print("Fetching documents...")
    sorted_docs = fetch_documents(word_ids, inverted_index, forward_index)

    if not sorted_docs:
        print("No documents found for the query.")
        return

    # Fetch URLs
    print("Fetching URLs...")
    results = fetch_urls(dataset_file, sorted_docs)

    # Limit to top 10 results
    top_results = results[:10]

    # Display results
    print("\nTop documents:")
    for doc_id, weight, url in top_results:
        print(f"DocID: {doc_id}, Weight: {weight}, URL: {url}")

if __name__ == "__main__":
    main()
