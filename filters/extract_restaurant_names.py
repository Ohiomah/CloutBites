# This script performs a call to Gemini Flash 2.0 model to find likely restaurant names in the 'caption' field of each entry in IG_posts.json,
# which was scraped previously via the Apify Instagram scraper for keywords 'NYC restaurants' and 'NYC foodies'. After identifying
# provides the caption as context and asks it to identify the likely restaurant name, or none
# after that, I manually went through and took care of some spelling errors to match the candidate names with the merged_restaurants_final.csv

import json
import google.generativeai as genai
from tqdm import tqdm # for a progress bar

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY) # API Key is exposed because this is a private repo

# # call listmodels
# list_models = genai.list_models()
# for model in list_models:
#     print(model)

model = genai.GenerativeModel('gemini-2.0-flash')

def extract_restaurant_name_gemini(caption):
    # Prompt deployment to gemini
    try:
        prompt = f"""
        Extract the restaurant name from this Instagram caption. 
        Return ONLY the name or blank if none found:
        {caption}
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error: {e}")
        return ""

def process_posts(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    for post in tqdm(posts, desc="Processing posts"):
        if 'restaurantName' not in post:  # Only process if field doesn't exist
            caption = post.get('caption', '')
            post['restaurantName'] = extract_restaurant_name_gemini(caption) if caption else ""
    
    with open(input_json, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    process_posts('../outputs/IG_posts.json')
