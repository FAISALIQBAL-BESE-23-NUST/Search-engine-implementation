import pandas as pd
import os

def create_lexicon_barrels(lexicon_csv, output_dir, barrel_size=1000):
    """
    Create barrels for the lexicon.
    
    :param lexicon_csv: Path to the lexicon CSV file.
    :param output_dir: Directory to save the barrel files.
    :param barrel_size: Number of terms per barrel.
    """
    try:
        # Load the lexicon
        print("Loading lexicon CSV...")
        lexicon = pd.read_csv(lexicon_csv)

        # Ensure the CSV contains necessary columns
        if not {'Term', 'Metadata'}.issubset(lexicon.columns):
            raise ValueError("CSV file must contain columns {'Term', 'Metadata'}")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Partition the lexicon into barrels
        for i in range(0, len(lexicon), barrel_size):
            barrel = lexicon.iloc[i:i+barrel_size]
            barrel_file = os.path.join(output_dir, f"lexicon_barrel_{i // barrel_size}.csv")
            barrel.to_csv(barrel_file, index=False)
            print(f"Saved lexicon barrel to '{barrel_file}'")

    except Exception as e:
        print(f"Error while creating lexicon barrels: {e}")

def main():
    # File paths
    lexicon_csv = "lexicon.csv"   # Path to the lexicon file
    output_dir = "lexicon_barrels"  # Directory to save barrels

    # Barrel size (number of terms per barrel)
    barrel_size = 1000

    # Create lexicon barrels
    create_lexicon_barrels(lexicon_csv, output_dir, barrel_size)

if __name__ == "__main__":
    main()