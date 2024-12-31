import pandas as pd
import nltk
from nltk.stem import PorterStemmer

# Download necessary NLTK resources
nltk.download('punkt')

# Initialize the Porter Stemmer
ps = PorterStemmer()

# Load the root and derived lexicons
root_lexicon = pd.read_csv('root_lexicon.csv')  # Assuming columns are ['word', 'id']
derived_lexicon = pd.read_csv('derived_lexicon.csv')  # Assuming columns are ['word', 'id']

# Load the inverted index
inverted_index_file = 'inverted_index.csv'
# Load the forward index
forward_index_file = 'ForwardIndex2.csv'
# Load the main dataset
main_dataset_file = 'first_50000_rows.csv'

# Function to remove punctuation from words
def remove_punctuation_from_words(df, column_name='word'):
    import string
    translator = str.maketrans('', '', string.punctuation)
    df[column_name] = df[column_name].apply(lambda x: x.translate(translator) if isinstance(x, str) else x)
    return df

# Function to map root word and derived words to their Word IDs
def map_to_word_ids(root_words, file_path_root='root_lexicon.csv', file_path_derived='derived_lexicon.csv'):
    root_word_to_id = dict(zip(root_lexicon['word'].str.lower(), root_lexicon['id']))
    derived_word_to_id = dict(zip(derived_lexicon['word'].str.lower(), derived_lexicon['id']))
    
    root_word_ids = {root_word: root_word_to_id.get(root_word.lower()) for root_word in root_words}
    
    derived_word_ids_map = {}
    for root_word in root_words:
        root_word_clean = root_word.lower()
        root, derived_words = get_derived_words(root_word_clean)
        if derived_words:
            derived_word_ids = [derived_word_to_id.get(word.lower()) for word in derived_words]
            derived_word_ids_map[root_word] = derived_word_ids
        else:
            derived_word_ids_map[root_word] = []
    
    return root_word_ids, derived_word_ids_map

# Function to process the query: Tokenization and Stemming
def process_query(query):
    tokens = nltk.word_tokenize(query)
    root_words = [ps.stem(word.lower()) for word in tokens]
    return root_words

# Function to fetch root word and corresponding derived words from the CSV
def get_derived_words(root_query, file_path='root_and_derived_words.csv'):
    df = pd.read_csv(file_path)
    row = df[df['root_word'].str.lower() == root_query.lower()]
    if not row.empty:
        root_word = row['root_word'].values[0]
        derived_words = row['derived_words'].values[0].split(',')
        return root_word, derived_words
    else:
        return None, None

# Function to fetch document IDs from the inverted index using the root word ID
def get_doc_ids_from_inverted_index(root_word_id, inverted_index_file=inverted_index_file):
    inverted_index_df = pd.read_csv(inverted_index_file)
    doc_ids = inverted_index_df[inverted_index_df['root_word_id'] == root_word_id]['doc_ids'].tolist()
    if doc_ids:
        return eval(doc_ids[0])
    else:
        return None

# Function to process and map root and derived words with their IDs, and retrieve document IDs
def process_and_map_word_ids(query, file_path_root='root_lexicon.csv', file_path_derived='derived_lexicon.csv', file_path_root_derived='root_and_derived_words.csv'):
    root_words = process_query(query)
    root_word_ids, derived_word_ids_map = map_to_word_ids(root_words, file_path_root, file_path_derived)
    
    doc_ids_for_root_words = {}
    for root_word, root_word_id in root_word_ids.items():
        if root_word_id is not None:
            doc_ids = get_doc_ids_from_inverted_index(root_word_id)
            if doc_ids is not None:
                doc_ids_for_root_words[root_word] = doc_ids
            else:
                doc_ids_for_root_words[root_word] = []
    
    return root_word_ids, derived_word_ids_map, doc_ids_for_root_words

# Function to process the forward index and update weights
def process_forward_index(doc_ids_for_root_words, forward_index_file=forward_index_file):
    forward_index_df = pd.read_csv(forward_index_file)
    updated_forward_index = []
    
    for root_word, doc_ids in doc_ids_for_root_words.items():
        for doc_id in doc_ids:
            row = forward_index_df[forward_index_df['DocID'] == doc_id]
            if not row.empty:
                details = row['Details'].values[0]
                detail_pairs = details.split(",")
                detail_dict = {}
                for pair in detail_pairs:
                    derived_word_id, weight = pair.split(":")
                    detail_dict[int(derived_word_id)] = int(weight)
                
                if root_word in derived_word_ids_map:
                    for derived_word_id in derived_word_ids_map[root_word]:
                        if derived_word_id is not None:
                            if derived_word_id in detail_dict:
                                detail_dict[derived_word_id] += 1
                            else:
                                detail_dict[derived_word_id] = 1
                
                total_weight = sum(detail_dict.values())
                new_details = ",".join([f"{k}:{v}" for k, v in detail_dict.items()])
                updated_forward_index.append([doc_id, total_weight])
    
    return updated_forward_index

# Function to fetch URLs from the main dataset
def fetch_urls_from_dataset(doc_ids_with_weights, main_dataset_file=main_dataset_file):
    main_dataset = pd.read_csv(main_dataset_file)
    sorted_doc_ids = sorted(doc_ids_with_weights, key=lambda x: x[1], reverse=True)
    result_urls = []
    for doc_id, weight in sorted_doc_ids:
        row_number = doc_id + 1
        if row_number <= len(main_dataset):
            url = main_dataset.loc[row_number - 1, 'url']
            result_urls.append((doc_id, weight, url))
    return result_urls

# Example usage
query = input("Enter your search query: ")
root_word_ids, derived_word_ids_map, doc_ids_for_root_words = process_and_map_word_ids(query)
updated_forward_index = process_forward_index(doc_ids_for_root_words)

# Fetch URLs based on updated forward index
result_urls = fetch_urls_from_dataset(updated_forward_index)
print("\nURLs in Descending Order of Weight:")
for doc_id, weight, url in result_urls:
    print(f"DocID: {doc_id}, Weight: {weight}, URL: {url}")
