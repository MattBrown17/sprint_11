"""This model is used for educational purposes
Produce a simple Flask web application to display
information about air quality
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from .openaq import OpenAQ
import openaq

# api = OpenAQ()
api = openaq.OpenAQ()
"""Creates an API object to store"""


def get_results():
    """Designed to connect to AQ API and get results

    Returns
    -------
    list : tuples
        contains the (utc_datetime, value) pair of bod['results'] object
    """
    _, bod = api.measurements(parameter='pm25')

    date_value_list = []
    for dic in bod['results']:
        utc_datetime = dic['date']['utc']
        value = dic['value']
        date_value_list.append((utc_datetime, value))

    return date_value_list


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)


class Record(DB.Model):
    """Creates a record of date value pairs for web application

    Attributes
    ----------
    id : int : primary key
    datetime : str
    value : float : not null
    """
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    datetime = DB.Column(DB.String)
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        """Prints out Record object as: f'('{datetime}', {value})'"""
        return f"Record: {self.id}, {self.datetime}, {self.value}"


@app.route('/')
def root():
    """Creates the base view of web application

    Returns
    -------
    list : tuples
        contains the (utc_datetime, value) pair of bod['results'] object
    """
    records = Record.query.all()
    return str(records)


@app.route('/refresh')
def refresh():
    """Pulls fresh data from the Open AQ API to replace existing"""
    DB.drop_all()
    DB.create_all()

    # Creates list of result tuples
    date_value_list = get_results()
    i = 1

    # loops through list adding records
    for obj in date_value_list:
        record = Record(id=i, datetime=obj[0], value=obj[1])
        DB.session.add(record)
        i = i + 1

    # Commits changes to the DB
    DB.session.commit()

    return root()
