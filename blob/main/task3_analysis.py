# Create a folder called data/ if it doesn't exist
# Save all stories to a file like data/trends_20240115.json
# Print how many stories were collected in total

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# A file at data/trends_YYYYMMDD.json DONE
# At least 100 stories inside it 
# A console message like: Collected 122 stories. Saved to data/trends_20240115.json

def save_to_json():
    """Load processed data and save to JSON file in data/ folder."""
    # Create data/ folder if it doesn't exist
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)
    
    # Load processed data
    df = pd.read_csv("processed_data.csv")
    
    # Convert DataFrame to list of dictionaries
    stories = df.to_dict(orient="records")
    
    # Create filename with current date (YYYYMMDD format)
    today = datetime.now().strftime("%Y%m%d")
    filename = data_folder / f"trends_{today}.json"
    
    # Save to JSON file
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(stories, fh, indent=2)
    
    # Print summary
    total_stories = len(stories)
    print(f"Collected {total_stories} stories. Saved to {filename}")


if __name__ == "__main__":
    save_to_json()
