#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import praw
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import re
import time

# Access credentials from Streamlit Secrets
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
user_agent = st.secrets["user_agent"]

# Initialize Reddit API connection
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Define function to fetch Reddit comments from the "movies" subreddit
def fetch_reddit_comments(query, limit=20):
    comments = []
    for submission in reddit.subreddit("movies").search(f'"{query}"', limit=limit):
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            comments.append(comment.body)
    return comments

# Define function to clean text
def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  # Remove URLs
    text = re.sub(r'[^A-Za-z\s]+', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    return text

# Define function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Define broader filtering based on word count, sentiment thresholds, and keyword matching
def filter_relevant_comments(comments, movie_title, keywords=[], min_words=5, sentiment_threshold=0.2):
    relevant_comments = []
    for comment in comments:
        # Check if comment is long enough and has significant sentiment
        word_count = len(comment.split())
        sentiment = analyze_sentiment(comment)
        
        # Check if the comment contains the movie title or any additional keywords
        if (word_count >= min_words and abs(sentiment) >= sentiment_threshold and
            (movie_title.lower() in comment.lower() or any(keyword.lower() in comment.lower() for keyword in keywords))):
            relevant_comments.append(comment)
    return relevant_comments

# Streamlit UI setup
st.title("Reddit Sentiment Analysis on Movies")

# Introduction
st.write("""
Welcome to the Reddit Sentiment Analysis Dashboard! This tool allows you to analyze public sentiment around popular movies based on Reddit comments. Enter a movie title or keyword below to see an analysis of sentiment, including an average sentiment score, sentiment distribution, and sample comments.
""")

# Instructions for the User
st.subheader("How to Use This Dashboard")
st.write("""
1. Enter a movie title or keyword in the input box below.
2. Click the "Analyze" button to fetch Reddit comments related to the movie.
3. View the sentiment results, including an average sentiment score and sentiment distribution.
4. Scroll down to see sample comments for more context on how people are discussing this movie.
""")

# User input for movie title
user_input = st.text_input("Movie Title or Keyword:", "")

if st.button("Analyze"):
    if user_input:
        # Generate YouTube search link for the movie trailer
        trailer_link = f"https://www.youtube.com/results?search_query={user_input.replace(' ', '+')}+trailer"
        st.markdown(f"**Watch the trailer for '{user_input}' on [YouTube]({trailer_link})**")
        
        # Show loading spinner and progress bar
        with st.spinner("Fetching comments and analyzing sentiment..."):
            progress_bar = st.progress(0)
            
            # Fetch comments
            comments = fetch_reddit_comments(user_input)
            progress_bar.progress(30)  # Update progress
            
            if comments:
                # Define additional keywords related to the specific movie
                additional_keywords = ["character1", "character2", "director name"]  # Customize for each movie
                
                # Filter comments based on the movie title and additional keywords
                filtered_comments = filter_relevant_comments(comments, user_input, additional_keywords)
                progress_bar.progress(60)  # Update progress
                
                if filtered_comments:
                    # Data processing
                    clean_comments = [clean_text(comment) for comment in filtered_comments]
                    df = pd.DataFrame(clean_comments, columns=['Comment'])
                    df['Sentiment'] = df['Comment'].apply(analyze_sentiment)
                    progress_bar.progress(80)  # Update progress

                    # Calculate average sentiment
                    average_sentiment = df['Sentiment'].mean()
                    progress_bar.progress(100)  # Complete progress

                    # Display results
                    st.subheader("Sentiment Analysis Results")
                    st.write(f"Average Sentiment for '{user_input}': {average_sentiment:.2f}")

                    # Interpretation of the Average Sentiment Score
                    if average_sentiment > 0:
                        st.write("The average sentiment score is positive, indicating that most users have a favorable opinion about this movie.")
                    elif average_sentiment < 0:
                        st.write("The average sentiment score is negative, suggesting that most users have a less favorable view of this movie.")
                    else:
                        st.write("The average sentiment score is neutral, which means opinions are mixed or evenly balanced between positive and negative.")

                    # Plot sentiment distribution
                    st.subheader("Sentiment Distribution")
                    plt.hist(df['Sentiment'], bins=20, color='skyblue', edgecolor='black')
                    plt.title(f"Sentiment Distribution for '{user_input}'")
                    plt.xlabel("Sentiment Score")
                    plt.ylabel("Number of Comments")
                    st.pyplot(plt.gcf())

                    # Additional insights on sentiment distribution
                    st.write("""
                    - A high concentration of comments with positive sentiment indicates that the movie is generally well-received.
                    - If there’s a mix of positive and negative comments, this may indicate a polarizing or controversial film.
                    - A neutral distribution could mean that users are discussing factual information rather than expressing strong opinions.
                    """)

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
