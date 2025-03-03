import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import re

def search_reddit(restaurant_name, subreddit="restaurants", limit=25):  # Default to r/restaurants, but customizable


    url = f"https://www.reddit.com/r/{subreddit}/search/?q={restaurant_name}&restrict_sr=1&sort=relevance" # restrict_sr=1 to stay within the subreddit
    all_posts = []


    try:
        response = requests.get(url, headers={'User-agent': 'your bot 0.1'}) # Reddit requires User-agent
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")


        posts = soup.find_all("div", class_="Post")  # Scrape up to the specified limit

        for post in posts[:limit]:  # Iterate up to the limit
            try:
                title = post.find("h3", class_="_eYtD2XCVieq6emjKBH3m").text
                post_text = post.find("p", class_="md-container").text if post.find("p", class_="md-container") else None # Some are just links
                comments_link = post.find("a", class_="comments")['href'] if post.find("a", class_="comments") else None # Handle posts with no comments

                upvotes_element = post.select_one("._1rZYMD_4xY3gRcSS3p8ODO") #  Upvote element
                upvotes = int(re.sub(r"[^\d]", "", upvotes_element['aria-label'])) if upvotes_element and 'aria-label' in upvotes_element.attrs and "upvotes" in upvotes_element['aria-label'] else 0


                all_posts.append({
                    "title": title,
                    "text": post_text,
                    "upvotes": upvotes,
                    "comments_link": comments_link
                })
            except AttributeError as e: # Catch and handle missing elements, continue scraping
                print(f"Attribute error: {e}") # print for debugging
                continue # important: skip this post and move to the next





        time.sleep(3)  # Be polite; avoid rate limiting


    except requests.exceptions.RequestException as e:
        print(f"Error searching Reddit for {restaurant_name}: {e}")



    return all_posts



import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import re

# ... (search_reddit function from the previous response remains the same)

def find_restaurant_reddit_posts_from_csv(csv_filepath, subreddit="restaurants", limit=25, output_filepath="reddit_posts.json"):


    all_restaurant_posts = {}


    try:
        with open(csv_filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                restaurant_name = row['name']
                posts = search_reddit(restaurant_name, subreddit, limit)
                if posts:
                    all_restaurant_posts[restaurant_name] = posts
                time.sleep(2)  # Small delay between searches for different restaurants


        with open(output_filepath, 'w', encoding='utf-8') as jsonfile:  # Save to JSON file
            json.dump(all_restaurant_posts, jsonfile, indent=4, ensure_ascii=False)

        print(f"Reddit posts saved to {output_filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")  # Catch and print any errors




# Example usage:
CSV_FILEPATH = "outputs/nyc_borough_cuisines.csv"
SUBREDDIT = "restaurants"  # Change if needed
LIMIT = 25   # Change if needed
OUTPUT_FILEPATH = "restaurant_reddit_posts.json"  # Customize output filename

find_restaurant_reddit_posts_from_csv(CSV_FILEPATH, SUBREDDIT, LIMIT, OUTPUT_FILEPATH)