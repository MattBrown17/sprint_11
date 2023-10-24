"""This module is used for educational purposes
Basic application development through Flask
"""

from re import DEBUG
from flask import Flask, render_template
from .models import DB, User, Tweet

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


    @app.route('/bananas')
    def bananas():
        """Contains /banana page

        Returns
        -------
        template described in base.html
        """
        return render_template('base.html', title='Bananas')


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
        return '''The database has been reset. 
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>'''


    @app.route('/populate')
    def populate():
        """Adds fake users and to database

        Returns
        -------
        str : "Database has been populated"
        """
        # Creates Fake Users
        matt = User(id=1, username='Matt')
        DB.session.add(matt)
        ryan = User(id=2, username='Ryan')
        DB.session.add(ryan)

        # Create Fake Tweets
        tweet1 = Tweet(id=1, text="matt's tweet text", user=matt)
        DB.session.add(tweet1)
        tweet2 = Tweet(id=2, text="ryan's tweet text", user=ryan)
        DB.session.add(tweet2)

        # Commit Changes to the DB
        DB.session.commit()

        return '''Created some users. 
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>'''

    return app
