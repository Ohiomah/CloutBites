import requests
import time
import csv

# -----------------------------------------------------------------------------------
# 1) INSERTED YOUR YELP API KEY (PUBLICLY SHARED)
# -----------------------------------------------------------------------------------
API_KEY = "B7Kvqaeax-frXKYdFUAoSemQRBuI5hzmtnqD6bf0fDir3mYZ8OizgLM5s8LDyAdFa86dbprS7NwRICNIyXK6MU80VwG5FZZ47ie2-7rZ0Pin1vCYIij-0P0YaGXDZ3Yx"

# -----------------------------------------------------------------------------------
# 2) CONFIGURATION
# -----------------------------------------------------------------------------------
SEARCH_URL = "https://api.yelp.com/v3/businesses/search"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Five NYC boroughs
boroughs = ["Manhattan, NY", "Brooklyn, NY", "Queens, NY", "Bronx, NY", "Staten Island, NY"]

# Some cuisine categories
cuisines = [
    "italian", "mexican", "chinese", "japanese", "thai",
    "korean", "indpak", "seafood", "steakhouses", "greek",
    "mediterranean"
]

# Yelp's max offset+limit is 240
LIMIT_PER_PAGE = 50
MAX_OFFSET_PLUS_LIMIT = 240
REQUEST_DELAY = 1   # seconds to sleep between calls to avoid rate-limit issues
OUTPUT_CSV = "nyc_borough_cuisines.csv"

# -----------------------------------------------------------------------------------
# 3) MAIN SCRIPT
# -----------------------------------------------------------------------------------
def main():
    # Dictionary to store businesses by Yelp ID (to avoid duplicates)
    all_businesses = {}

    for borough in boroughs:
        for cuisine in cuisines:
            print(f"\n--- Fetching {cuisine.upper()} restaurants in {borough} ---")
            offset = 0

            while True:
                # 1) If offset is already at or beyond the 240 cap, stop for this combo
                if offset >= MAX_OFFSET_PLUS_LIMIT:
                    print(f"Reached {MAX_OFFSET_PLUS_LIMIT}-result cap for {cuisine} in {borough}.")
                    break

                # 2) If the next page would exceed 240, reduce the limit for this page
                current_limit = LIMIT_PER_PAGE
                if offset + current_limit > MAX_OFFSET_PLUS_LIMIT:
                    current_limit = MAX_OFFSET_PLUS_LIMIT - offset
                    if current_limit <= 0:
                        break

                params = {
                    "location": borough,
                    "term": "restaurants",
                    "categories": cuisine,
                    "limit": current_limit,
                    "offset": offset
                }

                response = requests.get(SEARCH_URL, headers=HEADERS, params=params)
                if response.status_code != 200:
                    print("Error:", response.status_code, response.text)
                    break

                data = response.json()
                businesses = data.get("businesses", [])
                if not businesses:
                    print("No more results for this (borough, cuisine) combination.")
                    break

                # Store businesses in dict, keyed by business ID
                for biz in businesses:
                    all_businesses[biz["id"]] = biz

                offset += current_limit
                # Small pause to avoid hitting rate limits
                time.sleep(REQUEST_DELAY)

    # --------------------------------------------------------------------------------
    # 4) WRITE RESULTS TO CSV
    # --------------------------------------------------------------------------------
    unique_count = len(all_businesses)
    print(f"\nTotal unique businesses collected: {unique_count}")

    fieldnames = [
        "id", "name", "rating", "review_count",
        "address", "phone", "latitude", "longitude", "categories_list"
    ]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for biz_id, biz_data in all_businesses.items():
            categories_list = "; ".join([cat["title"] for cat in biz_data.get("categories", [])])
            row = {
                "id": biz_id,
                "name": biz_data.get("name", ""),
                "rating": biz_data.get("rating", ""),
                "review_count": biz_data.get("review_count", ""),
                "address": ", ".join(biz_data["location"].get("display_address", [])),
                "phone": biz_data.get("display_phone", ""),
                "latitude": biz_data["coordinates"].get("latitude", ""),
                "longitude": biz_data["coordinates"].get("longitude", ""),
                "categories_list": categories_list
            }
            writer.writerow(row)

    print(f"Data successfully written to {OUTPUT_CSV}.")

# -----------------------------------------------------------------------------------
# ENTRY POINT
# -----------------------------------------------------------------------------------
if __name__ == "__main__":
    main()