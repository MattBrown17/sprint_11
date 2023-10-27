"""This module is used for educational purposes
designed to create and manage database for web application: Twitoff
"""

from flask_sqlalchemy import SQLAlchemy


# Create a DB object from the SQLAlchemy class
DB = SQLAlchemy()

class User(DB.Model):
    """Identifies the User of Not Twitter

    Attributes
    ----------
    id : Big Int
        stores the database id
    username : str
        Non null instance storing the username of not Twitter
    newest_tweet_id : BigInt
        stores the most recent tweet id in our DB
    """
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    username = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        """Prints out object as f'user: {username}'"""
        return f"User: {self.username}"


class Tweet(DB.Model):
    """Stores the tweet related to a particular user

    Attributes
    ----------
    id : BigInt
        stores the unique id for the tweet
    text : Unicode
        Contains the main body of the tweet
    vect : PickleType (np Array)
        Vectorization of text
    user_id : BigInt
        foreign key associated with user id
    user : list : str
        references User class. stores list of tweets.
        lazy execution, only operates when called
    """
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable= False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        """Prints out object as f'tweet: {text}'"""
        return f"Tweet: {self.text}"
