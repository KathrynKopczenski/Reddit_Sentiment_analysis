#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import praw
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter
import re

# Reddit API credentials 
client_id = 'Itp99XIFIbTeNkKiFQuAuw'
client_secret = 'TaBqOZ9_HzrpkoYLW4rpvUKsJ2S3tQ'
user_agent = 'Personal_App by Emotional-Egg-5809'

# Initialize Reddit API connection
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Define function to fetch Reddit comments from the "movies" subreddit
def fetch_reddit_comments(query, limit=20):
    comments = []
    # Limit search to "movies" subreddit and use exact phrase matching
    for submission in reddit.subreddit("movies").search(f'"{query}"', limit=limit):
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            comments.append(comment.body)
    return comments

# Define function to clean text
def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    # Remove special characters and digits
    text = re.sub(r'[^A-Za-z\s]+', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Define function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Define function to filter comments based on relevant keywords
def filter_broad_comments(comments, min_words=5, sentiment_threshold=0.2):
    filtered_comments = []
    for comment in comments:
        # Check if comment is long enough and has significant sentiment
        word_count = len(comment.split())
        sentiment = analyze_sentiment(comment)
        if word_count >= min_words and abs(sentiment) >= sentiment_threshold:
            filtered_comments.append(comment)
    return filtered_comments

# Streamlit UI setup
st.title("Reddit Sentiment Analysis on Movies")
st.write("Enter a movie title or keyword to analyze sentiment on Reddit.")

# User input for movie title
user_input = st.text_input("Movie Title or Keyword:", "")

if st.button("Analyze"):
    if user_input:
        # Fetch comments
        comments = fetch_reddit_comments(user_input)
        if comments:
            # Filter comments to improve relevance
            filtered_comments = filter_relevant_comments(comments)
            if filtered_comments:
                # Data processing
                clean_comments = [clean_text(comment) for comment in filtered_comments]
                df = pd.DataFrame(clean_comments, columns=['Comment'])
                df['Sentiment'] = df['Comment'].apply(analyze_sentiment)

                # Calculate average sentiment
                average_sentiment = df['Sentiment'].mean()

                # Display results
                st.subheader("Sentiment Analysis Results")
                st.write(f"Average Sentiment for '{user_input}': {average_sentiment:.2f}")
                
                # Plot sentiment distribution
                st.subheader("Sentiment Distribution")
                plt.hist(df['Sentiment'], bins=20, color='skyblue', edgecolor='black')
                plt.title(f"Sentiment Distribution for '{user_input}'")
                plt.xlabel("Sentiment Score")
                plt.ylabel("Number of Comments")
                st.pyplot(plt.gcf())

                # Display sample comments
                st.subheader("Sample Comments")
                for comment in df['Comment'].sample(5):
                    st.write(f"- {comment}")
            else:
                st.write("No relevant comments found. Try a different keyword or movie title.")
        else:
            st.write("No comments found. Try a different keyword or movie title.")
    else:
        st.write("Please enter a movie title or keyword.")
