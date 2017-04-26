#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 19:31:40 2017

@author: Jackie Ali Cordoba

Important notes:
- This script collects tweets based on users, not topics. Future updates
or a separate script may handle topic based pulls.
- Make sure to name the column containg Twitter handles "twitter" in your csv.
- If you have user labels for supervised learning, name that column "label"
- CSV needs to be in the same folder as the python script
- Don't forget to create a config.py file with your Twitter API secret keys and
access tokens!

I know I should add optional arguments to the script to specify things like
tweet count, whether to collect English tweets only, etc. instead of hard-coding
the values and asking the user to update them. Alas, time was limited.

This code is licensed under the MIT license.
"""
import config
import os
import pandas as pd # https://github.com/pandas-dev/pandas
import sys
import tweepy # https://github.com/tweepy/tweepy
from pymongo import MongoClient # https://github.com/mongodb/mongo-python-driver

# Keys and Secrets for the Twitter API
# NOTE: for other users: Make sure to create a config.py file containing these!
# Add them to your .gitignore so you don't push your Twitter API credentials.
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_secret = config.access_secret

def get_mongo_collection(db_name='tweetdb', col_name='tweets'):
    """
    Sets up a connection to a MongoDB collection.

    db_name  -- The name for the database
    col_name -- The name for the collection

    """

    # MongoDB setup
    client = MongoClient()
    db = client[db_name]
    collection = db[col_name]

    return collection


def get_user_tweets(user, count=200):
    """
    Fetches tweets for the given user. Works in batches due to Twitter's
    limits on the number of tweets you can get per API request.

    NOTE: Even with this method, Twitter only allows you to collect 3,200 tweets
    from a single user's timeline.

    user  -- The desired user's Twitter handle
    count -- The total number of tweets to fetch

    """

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    # Waiting on the rate limit means the script will continue after the cooldown period
    # if you hit the limit of API calls you can make in a given period.
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Fetch the first batch of tweets!
    user_tweets = []
    new_batch = api.user_timeline(screen_name=user, count=200)
    user_tweets += new_batch

    # Used later so API request fetches tweets with IDs <= bookmark.
    # NOTE: Smaller IDs are older!
    bookmark = user_tweets[-1].id - 1

    remaining_tweets = count - 200
    batch_size = 200

    # Loop until the user's tweets run out or we collected the desired number of tweets
    while len(new_batch) > 0 and remaining_tweets > 0:
        if remaining_tweets - batch_size < 0:
            batch_size = remaining_tweets

        # Pick up where we left off using the bookmark
        new_batch = api.user_timeline(screen_name=user,
                                      count=batch_size,
                                      max_id=bookmark)

        user_tweets += new_batch

        # Update the bookmark
        bookmark = user_tweets[-1].id - 1

        # Update remaining tweets:
        remaining_tweets -= batch_size

    return user_tweets


def main():
    try:
        csv_filename = sys.argv[1]
        df = pd.read_csv(csv_filename)
    except IndexError:
        print "Missing input argument. Specify path to CSV containing Twitter handles."
        sys.exit(1)
    except IOError as e:
        print str(e)
        sys.exit(1)

    # If you have a preferred database or collection name, pass them in below.
    # Defaults: db_name='tweetdb' and col_name='tweets'
    collection = get_mongo_collection()

    for index, row in df.iterrows():
        # Check if user is already in the db in case the script was interrupted
        if collection.find({'username': row['twitter']}).count() == 0:
            print "Collecting tweets for %s" % (row['twitter'])

            user = {
                'username': row['twitter']
            }

            # Collects 3200 tweets by default
            # Update count parameter if you want a different amount.
            tweet_objects = get_user_tweets(user['username'], count=3200)

            tweets = []
            for tweet in tweet_objects:
                # Remove this if statement if you want to collect tweets in any
                # language.
                if tweet.lang == 'en':
                    tweets.append(tweet.text.encode('utf-8'))

            user['tweets'] = tweets

            # Add a label to the user for supervised learning if provided
            if 'label' in df.columns:
                user['label'] = row['label']

            if len(tweets) > 0:
                collection.insert_one(user)
        else:
            print "Already collected tweets for %s" % (row['twitter'])

if __name__ == '__main__':
    main()
