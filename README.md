This is a script you can use to collect tweets from various users and store
them in MongoDB.

Just create a CSV with Twitter handles in a column called "twitter" in the
same folder as the script.

If you have labels for supervised machine learning that you need to assign
to each user, simply put them in a column called "label" so the script can
find them.

It collects 3200 tweets per user by default and stores them in a database
called 'tweetdb' in the 'tweets' collection. If you want to change the number
of tweets collected or the database and collection names, make the changes I
specify in comments of the script. By default, it only collects English tweets,
but you can change that as well by removing an if statement.

This is adapted from a more specific script I used to collect and store tweets
from members of Congress for a supervised machine learning project.
(Classifying politicians as Democrats or Republicans based on their tweets).

The script was generalized for other applications (future projects, use by
others).
