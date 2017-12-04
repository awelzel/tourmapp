"""
# Set a few default options that are needed.
"""
# Used in templates so we do not have to hard-code this...
APP_NAME = "tourmapp"

# How to access Strava
STRAVA_OAUTH_AUTHORIZE_URL = "https://www.strava.com/oauth/authorize"
STRAVA_OAUTH_TOKEN_URL = "https://www.strava.com/oauth/token"

HASHIDS_SALT = "DEVELOPMENT"
HASHIDS_MIN_LENGTH = 8

# New default for Flask-SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False

# For environment checks???
HEROKU = False

MAPBOX_ACCESS_TOKEN = None
