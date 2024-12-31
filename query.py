import csv
from math import log10

# Increase CSV field size limit
# Increase field size limit to handle large files
csv.field_size_limit(10000000)  

# List of stop words to filter out
STOP_WORDS = {
    "a", "an", "the", "is", "am", "are", "and", "or", "of", "on", "in", "to", 
    "with", "for", "from", "by", "it", "this", "that", "was", "were", "has", 
    "have", "had", "be", "not", "as", "at", "but"
}

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

# Function to fetch the top documents for a multi-word query
def fetch_top_documents(query, lexicon, inverted_index, forward_index, dataset_file):
    # Split the query into individual words and remove stop words
    words = [word.strip().lower() for word in query.split() if word.strip().lower() not in STOP_WORDS]
    if not words:
        print("Your query contains only stop words or is empty.")
        return []

    # Process each word and calculate cumulative scores for documents
    doc_scores = {}
    total_documents = len(forward_index)  # Total number of documents in the dataset

    for word in words:
        # Step 1: Get Word ID from lexicon
        if word not in lexicon:
            print(f"The word '{word}' is not in the lexicon. Skipping.")
            continue
        word_id = lexicon[word]

        # Step 2: Get document IDs from inverted index
        if word_id not in inverted_index:
            print(f"No documents found for the word '{word}'. Skipping.")
            continue
        doc_ids = inverted_index[word_id]

        # Step 3: Get weights (term frequencies) from the forward index
        for doc_id in doc_ids:
            details = forward_index.get(doc_id, "")
            if details:
                # Split the details string to find the word ID and weight pairs
                pairs = details.split(',')
                for pair in pairs:
                    wid, tf = map(int, pair.split(':'))
                    if wid == word_id:  # Match the Word ID
                        # Calculate TF-IDF score
                        idf = log10(total_documents / len(doc_ids))
                        tf_idf = tf * idf
                        if doc_id in doc_scores:
                            doc_scores[doc_id] += tf_idf
                        else:
                            doc_scores[doc_id] = tf_idf

    # Step 4: Sort documents by their cumulative TF-IDF scores in descending order
    sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    # Step 5: Fetch links from the dataset for the top documents
    dataset = []
    with open(dataset_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dataset.append(row)

    top_docs = []
    for doc_id, score in sorted_docs[:5]:  # Limit to top 5 results
        # Adjusting doc_id to fetch the (doc_id + 2)th row from the dataset
        row_num = doc_id
        if row_num < len(dataset):  # Ensure row_num is within bounds
            link = dataset[row_num]['url']  # Fetch the URL
            top_docs.append((link, score))

    return top_docs

# Main program
def main():
    lexicon_file = 'Lexicon.csv'
    inverted_index_file = 'InvertedIndex.csv'
    forward_index_file = 'ForwardIndex.csv'
    dataset_file = 'CleanedSubDataset.csv'

    # Load data
    print("Loading lexicon...")
    lexicon = read_lexicon(lexicon_file)
    print("Loading inverted index...")
    inverted_index = read_inverted_index(inverted_index_file)
    print("Loading forward index...")
    forward_index = read_forward_index(forward_index_file)

    # Repeated search loop
    while True:
        # User input
        query = input("\nEnter your search query (type 'exit' to quit): ")
        if query.strip().lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        # Fetch top documents
        print("Fetching top documents...")
        top_docs = fetch_top_documents(query, lexicon, inverted_index, forward_index, dataset_file)

        # Display results
        if not top_docs:
            print("No results found.")
        else:
            print("Top documents:")
            for link, score in top_docs:
                print(f"Link: {link}, TF-IDF Score: {score:.4f}")

# Run the program
if __name__ == "__main__":
    main()
