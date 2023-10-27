"""This module is used for educational purposes
Analyzes text from not twitter in order to predict
the likelihood that a certain user wrote the text
uses LogisticRegression from the scikit-learn module
"""

# Imports
from sklearn.linear_model import LogisticRegression
import numpy as np
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_username, user1_username, hypo_tweet_text):
    """Generates model based on 2 Not Twitter users: user0 and user1
    using their NotTweets lists, they for a logistic regression predictive
        model in order to make predictions about a hypothetical not tweet
        in particular the specific user who is likely to have written it

    Parameters
    ----------
    user0_username : str
        Not Twitter handle associated with the first user
    user1_username : str
        Not Twitter handle associated with the second user
    hypo_tweet_text : str
        Text we are wanting to make a prediction on

    Returns
    -------
    prediction : int
        Predicts the user who wrote the hypothetical Not Tweet
    """
    # Grab the users from the DB
    user0 = User.query.filter(User.username==user0_username).one()
    user1 = User.query.filter(User.username==user1_username).one()

    # Get the word embeddings from each user
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Vertically stack the 2D array and create X_train and y_train
    X_train = np.vstack([user0_vects, user1_vects])
    zeros = np.zeros(user0_vects.shape[0])
    ones = np.ones(user1_vects.shape[0])
    y_train = np.concatenate([zeros, ones])

    # Instantiate and fit the LogisticRegression Model
    lr = LogisticRegression().fit(X_train, y_train)

    # Vectorize the hypothetical Not Tweet
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text).reshape(1,-1)

    # Makes prediction on Hypothetical tweet
    return lr.predict(hypo_tweet_vect)[0]
