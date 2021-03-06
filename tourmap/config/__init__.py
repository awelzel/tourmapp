import logging
import os
import sys

logger = logging.getLogger(__name__)


def _is_heroku_env(environ=None):
    environ = os.environ if not environ else environ
    return "DYNO" in environ and "heroku" in os.environ.get("PATH", "")


def configure_logging(app):
    """
    Configure the root logger and remove the crazy handlers from
    app.logger and set the propagate flag of that logger.

    This creates a bog standard stderr logger as that works best when
    some other process (supervisord, systemd, etc.) captures the output
    and writes it to file/syslog/ELK. We don't want to bother with
    opening files, rotating them, etc etc.
    """
    loglevel = getattr(logging, app.config.get("LOG_LEVEL", "INFO").upper())
    root_logger = logging.getLogger()

    if root_logger.handlers:
        for h in root_logger.handlers[:]:
            root_logger.removeHandler(h)

    fmt = "%(levelname)-7s - %(threadName)-13s - %(name)s: %(message)s"
    formatter = logging.Formatter(fmt)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(loglevel)
    root_logger.level = logging.NOTSET
    root_logger.addHandler(stream_handler)

    # Reset the app.logger setup
    for h in app.logger.handlers[:]:
        app.logger.removeHandler(h)
    app.logger.propagate = True


def configure_app(app, config=None):
    """
    Load the appropriate config and update app.config.

    Developing locally should be easy by using CONFIG_PYFILE and loading
    a local file. At the same time, we want to easily support heroku by
    just fetching everything from the environment. And for unit tests,
    the config options should be explictly passed in through.

    :param config: Update app.config from this dictionary and do not
        try any other methods of configuration.
    """
    app.config.from_object("tourmap.config.defaults")

    if config:
        app.config.update(config)
    elif _is_heroku_env():
        logger.info("Detected heroku environment...")
        app.config.from_object("tourmap.config.heroku")
    else:
        config_pyfile = os.environ.get("CONFIG_PYFILE", "../config.py")
        logger.info("Reading local config %s...", config_pyfile)
        app.config.from_pyfile(config_pyfile)

    # Setup proper logging...
    configure_logging(app)

    # SQLAlchemy configuration...
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
    from tourmap.resources import db
    db.init_app(app)

    # StravaClient configuration
    from tourmap.resources import strava
    strava.init_app(app)

    # Check for some required settings and else crash
    REQUIRED_SETTINGS = [
        "MAPBOX_ACCESS_TOKEN",
        "SECRET_KEY",
        "HASHIDS_SALT",
    ]
    for setting in REQUIRED_SETTINGS:
        if setting not in app.config or not app.config[setting]:
            raise RuntimeError("It appears {} was not set".format(setting))

    return app
