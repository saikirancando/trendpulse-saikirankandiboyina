# Use the requests library to fetch the top story IDs, then fetch each story's details
# If a request fails, print a message and move on — don't crash the script
# Wait 2 seconds between each category (time.sleep(2)) — one sleep per category loop, not per individual story fetch


import json
import time
from datetime import datetime

import requests

BASE_URL = "https://hacker-news.firebaseio.com/v0"

# agent
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# technology	AI, software, tech, code, computer, data, cloud, API, GPU, LLM
# worldnews	war, government, country, president, election, climate, attack, global
# sports	NFL, NBA, FIFA, sport, game, team, player, league, championship
# science	research, study, space, physics, biology, discovery, NASA, genome
# entertainment	movie, film, music, Netflix, game, book, show, award, streaming

CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"],
}

MAX_PER_CATEGORY = 25

# function for assigning category based on title keywords
def assign_category(title):
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None

# function for fetching top stories
def fetch_top_stories():
    url = f"{BASE_URL}/topstories.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Error fetching top stories: {error}")
        return []


# function for fetching story details
def fetch_story_details(story_id):
    url = f"{BASE_URL}/item/{story_id}.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        story_details = response.json()
        print(story_details)
        return story_details
    except requests.RequestException as error:
        print(f"Error fetching story {story_id}: {error}")
        return None

# main function to orchestrate the data collection
def main():
    top_story_ids = fetch_top_stories()
    collected_stories = []
    category_counts = {category: 0 for category in CATEGORIES}

    for story_id in top_story_ids:
        if all(count >= MAX_PER_CATEGORY for count in category_counts.values()):
            break

        story_details = fetch_story_details(story_id)
        if not story_details or "title" not in story_details:
            time.sleep(2)
            continue

        category = assign_category(story_details["title"])
        if category is None:
            time.sleep(2)
            continue

        if category_counts[category] >= MAX_PER_CATEGORY:
            time.sleep(2)
            continue

        collected_stories.append(
            {
                "post_id": story_details.get("id"),
                "title": story_details.get("title"),
                "category": category,
                "score": story_details.get("score", 0),
                "num_comments": story_details.get("descendants", 0),
                "author": story_details.get("by"),
                "collected_at": datetime.now().isoformat(),
            }
        )
        category_counts[category] += 1
        print(f"Collected {category}: {category_counts[category]}/{MAX_PER_CATEGORY}")
        time.sleep(2)

    with open("raw_data.json", "w", encoding="utf-8") as fh:
        json.dump(collected_stories, fh, indent=2)

    print(f"Saved {len(collected_stories)} stories to raw_data.json")
    print(f"Category counts: {category_counts}")


if __name__ == "__main__":
    main()
