"""This module is used for educational purposes
Simulates an instance of Twitter API that
can be queried and stored into the database 
and web application Twitoff

Handles connection to Not Twitter API from Not Tweepy
"""

from os import getenv
from .models import DB, Tweet, User
import not_tweepy as tweepy
import spacy


# Get out API keys from the .env file
key = getenv('TWITTER_API_KEY')
secret = getenv('Twitter_API_KEY_SECRET')

# Connect to the Not Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):
    """Take a username and pull user's data/tweets from API
    If user exists in DB: checks to see if user has new tweets to add

    Parameters
    ----------
    username : str
        contains the screen_name of Twitter user (i.e. handle)
    """
    try:
        # gets the username
        twitter_user = TWITTER.get_user(screen_name=username)

        # Check to see if user is in DB or Adds user
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, username=username)
        DB.session.add(db_user)

        # Gets user's tweets (list)
        tweets = twitter_user.timeline(count=200,
                                    exclude_replies=True,
                                    include_rts=False,
                                    tweet_mode='extended',
                                    since_id=db_user.newest_tweet_id)

        # Update newest tweet id
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # Adds tweets to DB
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id,
                            text=tweet.full_text[:300],
                            vect=tweet_vector,
                            user_id=db_user.id)

            DB.session.add(db_tweet)

        # Commits changes to DB
        DB.session.commit()

    except Exception as e:
        print(f"Error processing {username}: {e}")

    else:
        # Save Changes to DB
        DB.session.commit()

# load my_model for text vectorization
nlp = spacy.load('my_model/')


def vectorize_tweet(tweet_text):
    """Takes string object and returns a np Array object
    that represents the tweet numerically

    Parameters
    ----------
    tweet_text : Unicode
        Unicode data no longer tha 300 stored in Tweet object
    
    Returns
    -------
    vect : PickleType
        96 dimensional np Array
    """
    return nlp(tweet_text).vector


def get_all_usernames():
    """Returns all the current usernames in database

    Returns
    -------
    list : str
        contains usernames in database
    """
    usernames = []
    users = User.query.all()
    for user in users:
        usernames.append(user.username)

    return usernames
