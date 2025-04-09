from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import os

app = Flask(__name__, template_folder='templates')


# this is for a demo video to display the contents of our dataset, IG reviews and Yelp rating/review_count
def load_data():
    try:
        # Use absolute path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        restaurants_path = os.path.join(base_dir, 'outputs', 'merged_restaurants_final.csv')
        posts_path = os.path.join(base_dir, 'outputs', 'IG_posts_with_sentiment.json')

        print(f"Restaurants CSV path: {restaurants_path}")
        print(f"Posts JSON path: {posts_path}")

        # Load merged restaurants CSV file into a DataFrame.
        restaurants_df = pd.read_csv(restaurants_path)
        
        # Load Instagram posts JSON.
        with open(posts_path, 'r', encoding='utf-8') as f:
            ig_posts = json.load(f)
        
        # Filter posts with ratingAvailable: true.
        valid_posts = []
        for post in ig_posts:
            if post.get('ratingAvailable') is True:
                valid_posts.append(post)
        
        print(f"Total restaurants in CSV: {len(restaurants_df)}")
        print(f"Valid posts: {len(valid_posts)}")
        
        return restaurants_df, valid_posts
    except Exception as e:
        print(f"Error loading data: {e}")
        raise
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

# Global variables to store data.
try:
    restaurants_df, valid_posts = load_data()
except Exception as e:
    print(f"Could not load data: {e}")
    restaurants_df, valid_posts = None, None

@app.route('/')
def index():
    if restaurants_df is None:
        return "Data could not be loaded", 500
    
    try:
        # Get unique boroughs from the CSV.
        boroughs = sorted(restaurants_df['borough'].unique().tolist())
        print(f"Boroughs: {boroughs}")
        return render_template('index.html', boroughs=boroughs)
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"An error occurred: {e}", 500

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    if restaurants_df is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    try:
        # Filter by borough if provided.
        borough = request.args.get('borough', '').strip().lower()

        # Prepare a dictionary mapping restaurant_name_lower -> list of posts.
        posts_by_restaurant = {}
        for post in valid_posts:
            post_name = post.get("restaurantName", "").strip().lower()
            posts_by_restaurant.setdefault(post_name, []).append(post)
        
        restaurant_data = []
        # Iterate over each row in the CSV DataFrame.
        for _, restaurant in restaurants_df.iterrows():
            csv_name = str(restaurant['name']).strip()
            csv_name_lower = csv_name.lower()
            csv_borough = str(restaurant.get("borough", "")).strip().lower()

            # Apply borough filter if provided.
            if borough and csv_borough != borough:
                continue

            # Only process if there are matching IG posts.
            if csv_name_lower in posts_by_restaurant:
                restaurant_posts = posts_by_restaurant[csv_name_lower]
                overall_scores = [
                    post.get("sentiment_analysis", {}).get("overall_score", 0)
                    for post in restaurant_posts 
                    if post.get("sentiment_analysis", {}).get("overall_score") is not None
                ]
                avg_overall_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0

                restaurant_data.append({
                    'name': csv_name,
                    'borough': restaurant.get('borough'),
                    'yelp_rating': restaurant.get('rating'),
                    'overall_score': round(avg_overall_score, 2),
                    'review_count': len(restaurant_posts),
                    'posts': restaurant_posts
                })
        
        return jsonify(restaurant_data)
    except Exception as e:
        print(f"Error in restaurants route: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)