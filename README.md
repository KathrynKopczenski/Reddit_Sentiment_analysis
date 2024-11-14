# Reddit Sentiment Analysis on Movies 🎬

### Overview
This project analyzes sentiment from Reddit comments related to movies. Using the Reddit API, it gathers comments on a specific movie or keyword, cleans the text data, performs sentiment analysis, and visualizes the sentiment distribution. The app is built with Streamlit for an interactive user experience.

### Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)

### Features
- **Data Collection**: Gathers Reddit comments related to a movie or keyword from the "movies" subreddit.
- **Text Cleaning**: Cleans and processes comments, removing URLs, special characters, and excess whitespace.
- **Sentiment Analysis**: Uses TextBlob to evaluate the polarity of comments, indicating whether sentiment is positive, negative, or neutral.
- **Visualization**: Displays the sentiment distribution in a histogram and provides sample comments for context.

### Technologies Used
- **Python**: Main programming language.
- **PRAW**: Reddit API wrapper for fetching Reddit comments.
- **TextBlob**: For sentiment analysis.
- **Streamlit**: For building an interactive web application.
- **Matplotlib**: For visualizing sentiment distributions.

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/reddit_sentiment_analysis.git
   cd reddit_sentiment_analysis
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Reddit API Credentials**
   - Go to [Reddit's Developer Portal](https://www.reddit.com/prefs/apps) and create an application to obtain your Reddit API credentials.
   - Create a `.streamlit/secrets.toml` file to securely store API credentials:
     ```toml
     client_id = "your_client_id"
     client_secret = "your_client_secret"
     user_agent = "your_user_agent"
     ```

### Usage

1. **Run the Streamlit App**
   ```bash
   streamlit run app.py
   ```

2. **Interacting with the App**
   - Open a browser and go to the local URL provided by Streamlit (typically `http://localhost:8501`).
   - Enter a movie title or keyword in the input field and click "Analyze" to fetch comments and view the sentiment analysis.

3. **App Features**
   - **Sentiment Results**: Displays the average sentiment score for the selected movie or keyword.
   - **Sentiment Distribution**: Shows a histogram of sentiment scores across comments.
   - **Sample Comments**: Provides a few sample comments related to the movie or keyword.

### Project Structure
```
reddit_sentiment_analysis/
│
├── app.py                    # Main Streamlit app file
├── requirements.txt          # Python dependencies
└── .streamlit/
    └── secrets.toml          # Reddit API credentials (not included in GitHub for security)
```

### Future Improvements
- **Topic Modeling**: Use NLP techniques to identify key themes or topics in comments.
- **More Advanced Sentiment Analysis**: Replace TextBlob with more sophisticated models like VADER or transformers (e.g., BERT) for improved sentiment accuracy.
- **Enhanced Visualizations**: Add interactive charts to allow users to explore sentiment over time or by specific themes.

