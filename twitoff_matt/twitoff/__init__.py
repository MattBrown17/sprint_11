"""This module is used for educational purposes
Runs the startup of web application for a fake Twitter
Processor/Analyzer
"""

from .app import create_app

APP = create_app()
"""APP varible calls the creation of the web application"""
