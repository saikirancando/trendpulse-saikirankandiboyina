"""Task 3: Load, analyze, and explore cleaned trend data."""

import numpy as np
import pandas as pd
from pathlib import Path


def load_and_explore():
    """Load and explore the cleaned CSV file."""
    df = pd.read_csv("data/trends_clean.csv")
    
    print(f"Loaded data: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    avg_score = df['score'].mean()
    avg_comments = df['num_comments'].mean()
    print(f"\nAverage score   : {avg_score:,.0f}")
    print(f"Average comments: {avg_comments:,.0f}")
    
    return df


def basic_analysis(df):
    """Perform basic analysis using NumPy."""
    print("\n--- NumPy Stats ---")
    
    scores = df['score'].values
    
    # Score statistics
    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)
    highest_score = np.max(scores)
    lowest_score = np.min(scores)
    
    print(f"Mean score   : {mean_score:,.0f}")
    print(f"Median score : {median_score:,.0f}")
    print(f"Std deviation: {std_score:,.0f}")
    print(f"Max score    : {highest_score:,.0f}")
    print(f"Min score    : {lowest_score:,.0f}")
    
    # Category with most stories
    category_counts = df['category'].value_counts()
    most_common_category = category_counts.idxmax()
    most_common_count = category_counts.max()
    print(f"\nMost stories in: {most_common_category} ({most_common_count} stories)")
    
    # Story with most comments
    max_comments_idx = df['num_comments'].idxmax()
    max_comments_story = df.loc[max_comments_idx]
    title = max_comments_story['title']
    comments = int(max_comments_story['num_comments'])
    print(f"\nMost commented story: \"{title}\"  — {comments:,} comments")
    
    return mean_score


def add_new_columns(df, avg_score):
    """Add engagement and is_popular columns."""
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    df['is_popular'] = df['score'] > avg_score
    return df


def save_result(df):
    """Save the analyzed DataFrame to CSV."""
    output_file = Path("data/trends_analysed.csv")
    df.to_csv(output_file, index=False)
    print(f"\nSaved to {output_file}")


def main():
    """Execute the analysis pipeline."""
    try:
        df = load_and_explore()
        avg_score = basic_analysis(df)
        df = add_new_columns(df, avg_score)
        save_result(df)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
