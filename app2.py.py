#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import praw
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter

# Reddit API credentials 
client_id = 'Itp99XIFIbTeNkKiFQuAuw'
client_secret = 'TaBqOZ9_HzrpkoYLW4rpvUKsJ2S3tQ'
user_agent = 'Personal_App by Emotional-Egg-5809'

# Initialize Reddit API connection
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Define function to fetch Reddit comments
def fetch_reddit_comments(query, limit=100):
    comments = []
    for submission in reddit.subreddit("all").search(query, limit=limit):
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            comments.append(comment.body)
    return comments

# Define function to clean text
def clean_text(text):
    return ' '.join(word for word in text.split() if word.isalnum())

# Define function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

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
            # Data processing
            df = pd.DataFrame(comments, columns=['Comment'])
            df['Cleaned_Comment'] = df['Comment'].apply(clean_text)
            df['Sentiment'] = df['Cleaned_Comment'].apply(analyze_sentiment)

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
            for comment in df['Cleaned_Comment'].sample(5):
                st.write(f"- {comment}")
        else:
            st.write("No comments found. Try a different keyword or movie title.")
    else:
        st.write("Please enter a movie title or keyword.")

