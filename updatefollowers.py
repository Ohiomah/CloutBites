import pandas as pd

# Load the JSON data
df = pd.read_json('outputs/nyc_foodies_filtered.json')

instagram_urls = [f"https://www.instagram.com/{username}" for username in df['username']]
df['instagram_url'] = instagram_urls

# export only the instagram_url as CSV
df.to_csv('outputs/nyc_foodies_filtered.csv', columns=['instagram_url'], index=False)

print("CSV file saved successfully!")