"""Task 4: Create visualizations from analyzed trend data."""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def setup():
    """Load data and create outputs folder."""
    df = pd.read_csv("data/trends_analysed.csv")
    outputs_folder = Path("outputs")
    outputs_folder.mkdir(exist_ok=True)
    return df, outputs_folder


def chart1_top_stories(df, outputs_folder):
    """Chart 1: Top 10 Stories by Score (horizontal bar chart)."""
    top_10 = df.nlargest(10, 'score')[['title', 'score']].reset_index(drop=True)
    
    # Shorten titles longer than 50 characters
    top_10['title_short'] = top_10['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
    
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(top_10)), top_10['score'].values, color='steelblue')
    plt.yticks(range(len(top_10)), top_10['title_short'].values, fontsize=9)
    plt.xlabel('Score')
    plt.title('Top 10 Stories by Score')
    plt.tight_layout()
    plt.savefig(outputs_folder / 'chart1_top_stories.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("✓ Saved chart1_top_stories.png")


def chart2_categories(df, outputs_folder):
    """Chart 2: Stories per Category (bar chart)."""
    category_counts = df['category'].value_counts().sort_index()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    
    plt.figure(figsize=(10, 6))
    plt.bar(category_counts.index, category_counts.values, color=colors[:len(category_counts)])
    plt.xlabel('Category')
    plt.ylabel('Number of Stories')
    plt.title('Stories per Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(outputs_folder / 'chart2_categories.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("✓ Saved chart2_categories.png")


def chart3_scatter(df, outputs_folder):
    """Chart 3: Score vs Comments scatter plot."""
    popular = df[df['is_popular'] == True]
    unpopular = df[df['is_popular'] == False]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(unpopular['score'], unpopular['num_comments'], alpha=0.5, color='blue', label='Not Popular')
    plt.scatter(popular['score'], popular['num_comments'], alpha=0.5, color='red', label='Popular')
    plt.xlabel('Score')
    plt.ylabel('Number of Comments')
    plt.title('Score vs Comments')
    plt.legend()
    plt.tight_layout()
    plt.savefig(outputs_folder / 'chart3_scatter.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("✓ Saved chart3_scatter.png")


def bonus_dashboard(df, outputs_folder):
    """Bonus: Combine all charts into one dashboard."""
    top_10 = df.nlargest(10, 'score')[['title', 'score']].reset_index(drop=True)
    top_10['title_short'] = top_10['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
    
    category_counts = df['category'].value_counts().sort_index()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    
    popular = df[df['is_popular'] == True]
    unpopular = df[df['is_popular'] == False]
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('TrendPulse Dashboard', fontsize=16, fontweight='bold')
    
    # Chart 1: Top 10 stories
    axes[0].barh(range(len(top_10)), top_10['score'].values, color='steelblue')
    axes[0].set_yticks(range(len(top_10)))
    axes[0].set_yticklabels(top_10['title_short'].values, fontsize=8)
    axes[0].set_xlabel('Score')
    axes[0].set_title('Top 10 Stories by Score')
    
    # Chart 2: Categories
    axes[1].bar(category_counts.index, category_counts.values, color=colors[:len(category_counts)])
    axes[1].set_xlabel('Category')
    axes[1].set_ylabel('Number of Stories')
    axes[1].set_title('Stories per Category')
    axes[1].tick_params(axis='x', rotation=45)
    
    # Chart 3: Scatter plot
    axes[2].scatter(unpopular['score'], unpopular['num_comments'], alpha=0.5, color='blue', label='Not Popular')
    axes[2].scatter(popular['score'], popular['num_comments'], alpha=0.5, color='red', label='Popular')
    axes[2].set_xlabel('Score')
    axes[2].set_ylabel('Number of Comments')
    axes[2].set_title('Score vs Comments')
    axes[2].legend()
    
    plt.tight_layout()
    plt.savefig(outputs_folder / 'dashboard.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("✓ Saved dashboard.png (bonus)")


def main():
    """Execute the visualization pipeline."""
    try:
        df, outputs_folder = setup()
        chart1_top_stories(df, outputs_folder)
        chart2_categories(df, outputs_folder)
        chart3_scatter(df, outputs_folder)
        bonus_dashboard(df, outputs_folder)
        print("\n✓ All visualizations completed successfully!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
