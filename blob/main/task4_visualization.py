"""Task 4: Visualization for TrendPulse."""

import pandas as pd
import matplotlib.pyplot as plt


def visualize_data():
    """Create visualizations from the processed trend data."""
    df = pd.read_csv("processed_data.csv")
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # 1. Stories by category
    category_counts = df['category'].value_counts()
    axes[0].bar(category_counts.index, category_counts.values, color='steelblue')
    axes[0].set_title('Stories by Category', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Category')
    axes[0].set_ylabel('Count')
    axes[0].tick_params(axis='x', rotation=45)
    
    # 2. Score distribution
    axes[1].hist(df['score'], bins=20, color='coral', edgecolor='black')
    axes[1].set_title('Score Distribution', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Score (Upvotes)')
    axes[1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig("trend_visualization.png", dpi=100, bbox_inches='tight')
    print("Saved trend_visualization.png")


if __name__ == "__main__":
    visualize_data()
