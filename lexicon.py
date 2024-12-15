import pandas as pd
from collections import defaultdict
import re
import chardet

def build_lexicon(dataset, specific_fields=None):
    lexicon = defaultdict(set)
    for index, row in dataset.iterrows():
        row_text = " ".join(row[specific_fields].astype(str)) if specific_fields else " ".join(row.astype(str))
        words = re.findall(r'\w+', row_text.lower(), re.UNICODE)
        for word in words:
            lexicon[word].add(index)
    return {word: list(indices) for word, indices in lexicon.items()}

def save_lexicon_to_csv(lexicon, output_file):
    chunk_size = 50000
    for i in range(0, len(lexicon), chunk_size):
        chunk = list(lexicon.items())[i:i + chunk_size]
        chunk_df = pd.DataFrame({
            "Word": [word for word, indices in chunk],
            "Row_Indices": [",".join(map(str, indices)) for _, indices in chunk]
        })
        chunk_df.to_csv(output_file, mode='a', index=False, header=(i == 0))
    print(f"Lexicon saved to {output_file}")

def main():
    input_csv = "medium_articles.csv"
    output_csv = "lexicon.csv"

    print("Loading dataset...")
    try:
        with open(input_csv, 'rb') as f:
            result = chardet.detect(f.read(10000))
            encoding = result['encoding']
        dataset = pd.read_csv(input_csv, encoding=encoding)
    except FileNotFoundError:
        print(f"Error: File '{input_csv}' not found.")
        return

    print("Building lexicon...")
    lexicon = build_lexicon(dataset)

    print("Saving lexicon to CSV...")
    save_lexicon_to_csv(lexicon, output_csv)

if __name__ == "__main__":
    main()
