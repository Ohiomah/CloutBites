# update instagram scraper

import json

# making a function to improve the returned data from scraping
def extract_likely_restaurants(data):
    """
    Extracts likely restaurant names from Instagram data and filters 
    out entries with less than 10,000 followers.

    Args:
        data (dict): A dictionary containing Instagram profile data.

    Returns:
        list: A list of likely restaurant names from posts by accounts 
              with 10,000 or more followers. Returns an empty list 
              if no such accounts are found.
    """

    if data["followersCount"] < 10000:
        return []  # Skip if followers are less than 10,000

    likely_restaurants = set()
    for post in data["latestPosts"]:
        # 1. Prioritize locationName if available:
        if post.get("locationName"):
            likely_restaurants.add(post["locationName"])

        # 2. Extract from caption using mentions and context keywords
        caption = post.get("caption", "").lower()
        mentions = post.get("mentions", [])

        for mention in mentions:
            # Heuristic: Check if mention is followed by common restaurant-related terms
            potential_restaurant_phrases = [
                f"@{mention}", # Mention alone might be restaurant
                f"@{mention} restaurant",
                f"@{mention} cafe",
                f"@{mention} bar",
                f"@{mention} grill",
                f"@{mention} eatery",
                f"@{mention} bistro",
                f"@{mention} kitchen",
                f"@{mention} popup", # For pop-up restaurants
                f"at @{mention}",
                f"from @{mention}",
            ]
            for phrase in potential_restaurant_phrases:
                if phrase in caption:
                    # Extract the mention (likely restaurant) and clean it up
                    restaurant_name = mention.replace("_", " ") # remove underscores
                    likely_restaurants.add(restaurant_name)


        # 3. Use tagged users as a fallback (less reliable but still potentially useful):
        tagged_users = post.get("taggedUsers", [])
        for user in tagged_users:
            likely_restaurants.add(user["full_name"])



    return list(likely_restaurants)


# Example Usage (assuming you load your JSON data into 'insta_data')
with open("./outputs/nyc_foodies.json", "r", encoding="utf-8") as f:
    insta_data = json.load(f)

print(insta_data["followersCount"])
restaurants = extract_likely_restaurants(insta_data)

if restaurants:
    print("Likely Restaurant Names:")
    for restaurant in restaurants:
        print(f"- {restaurant}")
else:
    print("No accounts found with 10,000 or more followers.")