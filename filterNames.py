import json
import re

with open("./outputs/IG_posts.json", "r", encoding="utf-8") as f:
    insta_data = json.load(f)
    

restaurant_names = set()

for entry in insta_data:
    caption = entry.get("caption", "").lower()
    
    # Extract restaurant names from caption
    possible_names = re.findall(r'@([a-zA-Z0-9_]+)', caption)
    restaurant_names.update(possible_names)

restaurant_names = list(restaurant_names)

# put into file

with open("restaurant_names.json", "w") as file:
    
    json.dump(restaurant_names, file, indent=4)
    
    print("Data has been written to file")
    
