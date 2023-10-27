"""This module is used for educational purposes
Basic application development through Flask
"""

from re import DEBUG
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user, get_all_usernames
from .predict import predict_user

# Factory to manage application startup
def create_app():
    """Factory managing the production and return of Flask Object

    Returns
    -------
    app : Flask object
        Implementing our web address application
    """
    # Creation of Flask object
    app = Flask(__name__)

    # Database configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Register our DB with app
    DB.init_app(app)

    # Listener for app to interact with URLs
    @app.route('/')
    def root():
        """Connects to the website and runs first
        Querys the user table

        Returns
        -------
        template described in base.html
        """
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)


    @app.route('/reset')
    def reset():
        """Drop all database tables 
        recreate tables according to schema in models.py

        Returns
        -------
        str : "Database has been reset"
        """
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset Database')


    @app.route('/update')
    def update():
        """Updates the DB with most recent tweets from populated tables"""
        # gets all users existing in DB
        usernames = get_all_usernames()

        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='Users Updated')


    @app.route('/user', methods=['POST'])
    @app.route('/user/<username>', methods=['GET'])
    def user(username=None, message=''):
        """Grabs users from the Not Twitter API and displays them

        Parameters
        ----------
        username : str
            tells the app which user to add/display based on their Not Twitter handle
        message : str
            Sent to base.html to be displayed on the application site
        """
        username = username or request.values['user_name']

        try:
            if request.method == 'POST':
                add_or_update_user(username)
                message = f'User "{username}" has been successfully added!'

            tweets = User.query.filter(User.username==username).one().tweets

        except Exception as e:
            message = f'Error adding {username}: {e}'
            tweets = []

        return render_template('user.html', title=username, tweets=tweets, message=message)


    @app.route('/compare', methods=['POST'])
    def compare():
        """Displays the functionality of the Not Tweet comparison"""
        user0, user1 = sorted([request.values['user0'], request.values['user1']])
        hypo_tweet_text = request.values['tweet_text']

        if user0 == user1:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user0, user1, hypo_tweet_text)

            # Get into if statement if prediction is 1
            if prediction:
                message = f'"{hypo_tweet_text}" is more likely to be said by {user1} than by {user0}'
            else:
                message = f'"{hypo_tweet_text}" is more likely to be said by {user0} than by {user1}'

        return render_template('prediction.html', title='Prediction', message=message)

    return app
