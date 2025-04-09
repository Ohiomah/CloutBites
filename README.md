# CloutBites: NYC Restaurant Social Media Analysis

# CPSC 572 Winter 2025 - Final Project

## Project Background

Hey, we are Ohiomah and Derek! We are both avid foodies and high ranked users of the app Beli, check out this [intriguing article about the app](https://www.oxfordstudent.com/2024/02/27/in-conversation-with-madeline-bryant/) to learn more. Our project was born out of a curiosity to explore the intersection of social media influence and restaurant reviews. 

Specifically, we wanted to investigate:
- Do the same influencers review similar restaurants? (e.g. foodies that consistently review halal restaurants, or eat/review the same places everytime)
- How does social media sentiment compare to traditional review ratings on platforms like Yelp and Google Maps?

## Project Overview

CloutBites (just a name we created) analyzes restaurant reviews and sentiment across Instagram and Yelp in the New York City area. Why did we choose New York? Beli was started there, and the social media scraping proved to provide over 2000 restaurants with rich social media reviews. By leveraging social media data and traditional restaurant ratings, we can make a start at trying to provide insights into the complex world of food influencer marketing and restaurant reputation. Also, the concept of "social proof" admittedly often influences our purchasing decisions and we wanted to see how it played out in the restaurant industry.

## Dataset

- **Source**: Instagram posts and Yelp restaurant data
- **Scope**: Restaurants in the New York City metropolitan area
- **Focus**: Analyzing restaurant reviews through social media influencers

## See Our Dataset (Flask app)
We prepared a shortlist of restaurants and their reviews by borough, including the Yelp rating and the # of Instagram reviews, on which we conducted sentiment analysis.

To access,
```bash
cd app
python app.py # which will start the app on http://localhost:5000 by default
```

## Key Data Files (please look)

- `IG_posts.json`: Raw Instagram post data
- `merged_restaurants_final.csv`: Comprehensive Yelp restaurant dataset
- `nyc_borough_cuisines.csv`: NYC restaurant inspection data (used in intermediate presentation, but not the final analysis)

## What is our Methodology?

### 🧹 Data Collection and Cleaning (`clean_data.ipynb`)

#### Restaurant Name Extraction
- Used **Gemini Flash 2.0 AI model** to predict restaurant names from Instagram captions
- Cross-checked against `merged_restaurants_final.csv`
- Employed `difflib` for string matching to reconcile name variations
- Manually set `ratingAvailable`: true for matched restaurants (lots of Ctrl + F but this was the best way as some names were close, though not identical matches to the Yelp names)

#### Additional Data Sources
- Google Places reviews (fallback method)
- Attempted Instagram follower scraping with Instaloader (rate-limited, sadly, but would be a future extension)

### 💬 Sentiment Analysis (`sentiment_analysis_IG_posts.ipynb`)

Used LangChain and a special wrapper class of the Gemini API (engineering a prompt that worked as a human might) for Instagram post sentiment scoring:
- **Taste** (40% weight)
- **Presentation** (30% weight)
- **Creativity** (30% weight)

Calculated weighted average for overall score

### 🌐 Network Analysis

Created two one-mode projections of a bipartite network:

1. **Influencer Network**: 
   - **Nodes**: Instagram food influencers
   - **Edges**: Connected if they reviewed the same restaurant

2. **Restaurant Network**:
   - **Nodes**: Restaurants
   - **Edges**: Connected if reviewed by the same influencer

## Project Structure

### Folders
- `filters/`: Data processing and analysis Jupyter notebooks
- `outputs/`: Processed data and results
- `gephi/`: Network graph data files
- `scripts/`: Utility Python scripts
- `degree/`: Using networkx as we learned in class, a representation of our degree distribution

## Setup and Installation

### Prerequisites
- Python 3.8+
- Google API Key (required for Gemini API)

### Installation Steps
1. Clone the repository
2. Create a virtual environment (linux instructions):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

### Configuration

Set your Google API Key as an environment variable

```bash
export GOOGLE_API_KEY='your_api_key'
```

### Checkout and Reproduce the Project

- Open Jupyter notebooks from the `filters/` folder
- Execute notebooks in sequence
1. `clean_data.ipynb`
2. `sentiment_analysis_IG_posts.ipynb`
3. `gephi_creation.ipynb`

The final notebook will generate the various nodes and edges files in the `gephi/` folder that can be imported as spreadsheet into Gephi.

### General Approach to Gephi

1. Force Atlas 2 Method
2. For restaurants (over 2000 nodes): Fruchterman Reingold
3. Sized by degree
4. Coloured by modularity class
5. Edge colour by weight

## Future Extensions
- Improve Instagram follower data collection
- Expand sentiment analysis techniques



