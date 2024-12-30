import pandas as pd
import os
import string

# Function to load lexicon from chunks
def load_lexicon_chunks(lexicon_folder):
    """
    Load lexicon chunks into a single dictionary.
    Each chunk contains word_id and word.
    """
    lexicon = {}
    
    # Iterate through all lexicon chunk files
    for lexicon_file in os.listdir(lexicon_folder):
        if lexicon_file.endswith(".csv"):
            lexicon_path = os.path.join(lexicon_folder, lexicon_file)
            lexicon_df = pd.read_csv(lexicon_path)
            
            # Add each word and its word_id to the lexicon dictionary
            for _, row in lexicon_df.iterrows():
                lexicon[row['word']] = row['word_id']
    
    return lexicon


# Function to load the inverted index chunks
def load_inverted_index_chunks(inverted_index_folder):
    """
    Load inverted index chunks into a dictionary.
    Each entry contains word_id and a list of doc_ids.
    """
    inverted_index = {}
    
    # Iterate through all inverted index chunk files
    for index_file in os.listdir(inverted_index_folder):
        if index_file.endswith(".csv"):
            index_path = os.path.join(inverted_index_folder, index_file)
            index_df = pd.read_csv(index_path)
            
            # Add each word_id and its corresponding document IDs to the inverted index
            for _, row in index_df.iterrows():
                inverted_index[row['word_id']] = set(row['doc_ids'])  # Convert doc_ids to a set for uniqueness
    
    return inverted_index


# Function to clean and normalize query terms
def clean_query(query):
    """
    Clean the query text by removing punctuation and converting to lowercase.
    """
    # Remove punctuation and convert to lowercase
    query = query.lower()
    query = query.translate(str.maketrans('', '', string.punctuation))
    return query.split()  # Tokenize by whitespace


# Function to process the query
def process_query(query, lexicon, inverted_index):
    """
    Process the query and return the list of relevant document IDs.
    """
    # Clean and normalize the query terms
    query_terms = clean_query(query)
    
    # Initialize a list to store document IDs that match the query terms
    doc_ids = set()
    
    # Process each query term
    for term in query_terms:
        if term in lexicon:  # Check if the word exists in the lexicon
            word_id = lexicon[term]
            
            if word_id in inverted_index:  # Check if the word ID exists in the inverted index
                doc_ids.update(inverted_index[word_id])  # Add document IDs for this word to the result set
    
    # Return the set of document IDs that match the query
    return doc_ids


# Example usage
if __name__ == "__main__":
    # Define paths for lexicon and inverted index chunks
    lexicon_folder = "lexicon_chunks"  # Folder containing lexicon chunk CSVs
    inverted_index_folder = "inverted_index_chunks"  # Folder containing inverted index chunk CSVs

    # Load lexicon and inverted index chunks
    lexicon = load_lexicon_chunks(lexicon_folder)
    inverted_index = load_inverted_index_chunks(inverted_index_folder)
    
    # Process a query
    query = "example query terms"
    result_docs = process_query(query, lexicon, inverted_index)
    
    # Display the result document IDs
    print(f"Relevant Document IDs for the query '{query}':")
    print(result_docs)
