# Task 2: Load, clean, and process data from JSON files.

import json
import pandas as pd
from pathlib import Path


def load_json_from_data_folder():
    """Load the JSON file from the data/ folder into a Pandas DataFrame."""
    data_folder = Path("data")
    
    # Find the latest trends JSON file
    json_files = list(data_folder.glob("trends_*.json"))
    if not json_files:
        raise FileNotFoundError("No JSON files found in data/ folder")
    
    latest_file = sorted(json_files)[-1]
    
    with open(latest_file, "r", encoding="utf-8") as fh:
        raw_data = json.load(fh)
    
    df = pd.DataFrame(raw_data)
    print(f"Loaded {len(df)} rows from {latest_file.name}")
    return df


def clean_data(df):
    """Clean the data by fixing issues and removing low-quality entries."""
    initial_rows = len(df)
    
    # 1. Remove duplicates based on post_id
    df = df.drop_duplicates(subset=['post_id'], keep='first')
    after_duplicates = len(df)
    
    # 2. Drop rows with missing critical values
    df = df.dropna(subset=['post_id', 'title', 'score'])
    after_nulls = len(df)
    
    # 3. Fix data types - ensure score and num_comments are integers
    df['score'] = pd.to_numeric(df['score'], errors='coerce').astype('Int64')
    df['num_comments'] = pd.to_numeric(df['num_comments'], errors='coerce').astype('Int64')
    
    # 4. Remove low-quality stories (score < 5)
    df = df[df['score'] >= 5]
    after_low_scores = len(df)
    
    # 5. Strip extra whitespace from title column
    df['title'] = df['title'].str.strip()
    
    print(f"After removing duplicates: {after_duplicates}")
    print(f"After removing nulls: {after_nulls}")
    print(f"After removing low scores: {after_low_scores}")
    
    return df


def save_cleaned_data(df):
    """Save the cleaned DataFrame to CSV."""
    data_folder = Path("data")
    output_file = data_folder / "trends_clean.csv"
    
    df.to_csv(output_file, index=False)
    print(f"\nSaved {len(df)} rows to {output_file}")
    
    # Print summary by category
    print("\nStories per category:")
    category_summary = df['category'].value_counts().sort_index()
    for category, count in category_summary.items():
        print(f"  {category:<15} {count:>2}")


def main():
    """Execute the data cleaning pipeline."""
    try:
        # Load
        df = load_json_from_data_folder()
        
        # Clean
        df_clean = clean_data(df)
        
        # Save
        save_cleaned_data(df_clean)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()