# This script performs a regex search to find likely restaurant names in the 'caption' field of each entry in IG_posts.json,
# which was scraped previously via the Apify Instagram scraper for keywords 'NYC restaurants' and 'NYC foodies'. After identifying
# a potential name using the @ symbol, it attempts to visit the corresponding Instagram profile using BeautifulSoup to extract
# the official name. The script then checks if the extracted name exists in merged_restaurants_final.csv and updates the JSON
# file with the results.
import json
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup


def extract_restaurant_name(caption):
    # Extract the first @mention in the caption
    match = re.search(r'@([\w.]+)', caption)
    if match:
        username = match.group(1)
        try:
            # Fetch Instagram profile page
            # I signed into my personal instagram so the webpage brings me to each individual restaurant page
            url = f'https://instagram.com/{username}'
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse the page to extract the official name
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                # Extract the name from the title (e.g., 'Name (@username) • Instagram photos and videos')
                title = title_tag.text.strip()
                name = title.split('(')[0].strip()
                return name
        except Exception as e:
            print(f'Error fetching Instagram profile for @{username}: {e}')
    return ''


def check_restaurant_in_csv(restaurant_name, csv_path):
    try:
        df = pd.read_csv(csv_path)
        return restaurant_name in df['Name'].values
    except Exception as e:
        print(f'Error reading CSV: {e}')
        return False


def process_ig_posts(json_path, csv_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            posts = json.load(f)

        for post in posts:
            caption = post.get('caption', '')
            restaurant_name = extract_restaurant_name(caption)
            if restaurant_name:
                post['restaurantName'] = restaurant_name
                post['foundInCSV'] = check_restaurant_in_csv(restaurant_name, csv_path)
            else:
                post['restaurantName'] = ''
                post['foundInCSV'] = False

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f'Error processing IG posts: {e}')


# Files are listed as follows -> please note that merged_restaurants_final was previously prepared in the clean_data.ipynb Python notebook

IG_POSTS_JSON = 'outputs/IG_posts.json'
MERGED_RESTAURANTS_CSV = 'outputs/merged_restaurants_final.csv'

process_ig_posts(IG_POSTS_JSON, MERGED_RESTAURANTS_CSV)
