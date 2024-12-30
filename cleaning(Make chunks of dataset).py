import pandas as pd
import numpy as np
import re
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# Initialize NLTK tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Function for cleaning and normalizing text
def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase and strip extra spaces
    text = text.lower().strip()
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Break dataset into chunks of equal size
def break_into_chunks(dataframe, chunk_size, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    num_chunks = int(np.ceil(len(dataframe) / chunk_size))
    for i in range(num_chunks):
        chunk = dataframe.iloc[i * chunk_size:(i + 1) * chunk_size]
        chunk.to_csv(f"{output_dir}/chunk_{i+1}.csv", index=False)
    print(f"Dataset broken into {num_chunks} chunks in {output_dir}/")

# Main function to process the dataset
def process_dataset(input_file, chunk_size, output_dir):
    print("Loading dataset...")
    # Load the dataset
    #read only first 50k article
    df = pd.read_csv(input_file,nrows=50000)
    
    print("Dataset Overview:")
    print(df.info())
    print("Sample Data:")
    print(df.head())

    # Basic Cleaning: Remove duplicates and handle missing values
    print("\nPerforming basic cleaning...")
    df = df.drop_duplicates(subset=['title', 'text'], keep='first')
    df = df.dropna(subset=['title', 'text'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')  # Convert timestamps
    print(f"Cleaned dataset contains {len(df)} rows.")

    # Text Cleaning and Normalization
    print("\nCleaning and normalizing text...")
    tqdm.pandas()  # For progress bar with pandas
    df['clean_text'] = df['text'].progress_apply(clean_text)

    # Create derived fields for indexing
    print("\nCreating derived fields for indexing...")
    df['snippet'] = df['text'].str[:200]  # First 200 characters for preview
    df['word_count'] = df['clean_text'].apply(lambda x: len(x.split()))

    # Break the dataset into smaller chunks for processing
    print("\nBreaking dataset into smaller chunks...")
    break_into_chunks(df, chunk_size, output_dir)

    print(f"Processing complete. Data chunks are saved in {output_dir}/")

# Run the script
if __name__ == "__main__":
    # Input parameters
    input_file = "Dataset.csv"  # dataset fiel path
    chunk_size = 5000 # Adjust chunk size as needed
    output_dir = "DatasetChunks"

    # Process the dataset
    process_dataset(input_file, chunk_size, output_dir)
