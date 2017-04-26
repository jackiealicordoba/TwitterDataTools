# TwitterDataTools
This repository contains scripts adapted from my Twitter data analysis projects that can be used for future work by myself or others. They were generalized to work in less specific contexts.

## tweet_collector.py
This is a script you can use to collect tweets from various users and store
them in MongoDB.

Just create a CSV with Twitter handles in a column called "twitter" in the
same folder as the script.

If you have labels for supervised machine learning that you need to assign
to each user, simply put them in a column called "label" so the script can
find them.

Use this command to run the script:
```sh
$ python tweet_collector.py your_csv.csv
```

It collects 3200 tweets per user by default and stores them in a database
called 'tweetdb' in the 'tweets' collection. If you want to change the number
of tweets collected or the database and collection names, make the changes I
specify in comments of the script. By default, it only collects English tweets,
but you can change that as well by removing an if statement.

## tweet_cleaner.py
Coming soon! This script is used to preprocess, clean, and tokenize tweets.
I need to modify the original script to be general-purpose.

# Libraries Used
The following tools were used at least once in the scripts above:
* [PyMongo](https://github.com/mongodb/mongo-python-driver) - A python driver for MongoDB
* [tweepy](https://github.com/tweepy/tweepy) - A python wrapper for the Twitter API
* [pandas](https://github.com/pandas-dev/pandas) - A data analysis library for Python

# License
MIT
