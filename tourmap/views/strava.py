"""
Strava OAUTH flow hacked together.
"""
from urllib.parse import urlunparse, urlencode, parse_qsl

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
import flask_login

import tourmap.utils
import tourmap.utils.strava
from tourmap import database
from tourmap import resources
from tourmap.models import User, PollState, Token, Tour


class LoginController(object):
    """
    Handle the result of a strava.exchange_token() call.
    """
    def __init__(self, session=None):
        self.__session = session or resources.db.session

    def strava_login(self, data):
        """
        Given data from a Strava token exchange, either update
        an existing user, or create a new one.

        :param data: as returned by a token exchange from Strava.
        :returns: tuple representing (new_user, user)
        """
        for f in ["athlete", "access_token", "refresh_token", "expires_at"]:
            if f not in data:
                raise KeyError(f)

        athlete = data["athlete"]
        new_user = False
        tour = None
        user = User.query.filter_by(strava_id=athlete["id"]).one_or_none()

        if user is None:
            new_user = True
            user = User(strava_id=athlete["id"])
            tour = Tour.default_tour_for(user)

        user.email = athlete.get("email")
        user.firstname = athlete.get("firstname")
        user.lastname = athlete.get("lastname")
        user.country = athlete.get("country")

        self.__session.add_all(filter(None, [user, tour]))
        self.__session.commit()

        # Create or update the token if needed...
        token = Token.query.filter_by(user=user).one_or_none()
        if token is None:
            token = Token()
            token.update_from_strava(data)
            token.user = user
        else:
            token.update_from_strava(data)

        poll_state = PollState.query.filter_by(user=user).one_or_none()
        if poll_state is None:
            poll_state = PollState(
                user=user,
                full_fetch_next_page=0,
                full_fetch_completed=False,
            )

        # Clear the error on a new login, assuming it was related to a
        # token issue which should be solved by a re-login!
        poll_state.clear_error()
        poll_state.start()

        # Ok, go figure it out for us...
        self.__session.add_all([token, poll_state])

        try:
            self.__session.commit()
        except database.IntegrityError as e:
            # Now, this can happen if someone tries to sign-up the
            # same account at the same time. But than he can just
            # retry...
            current_app.logger.exception("User %s: %s", user, e)
            self.__session.rollback()
            abort(500)

        return new_user, user


def create_blueprint(app):
    bp = Blueprint("strava", __name__)

    @bp.route("/login")
    def login():
        """
        Just the Connect with Strava template.
        """
        return render_template("strava/login.html")

    @bp.route("/logout")
    def logout():
        """
        Do a logout.
        """
        flask_login.logout_user()
        return redirect(url_for("index.index"))

    @bp.route("/callback")
    def callback():
        """
        Handle a callback representing a user coming back
        from the Strava page to here.
        """
        if "error" in request.args:
            msg = "Strava error in callback: {!r}".format(request.args["error"])
            current_app.logger.warning(msg)
            flash(msg, category="error")
            return redirect(url_for("strava.login"))

        state = request.args.get("state")
        state_dict = dict(parse_qsl(state))
        if state_dict.get("state") != "CONNECT":
            msg = "Strava callback with unexpected state: {!r}".format(state)
            current_app.logger.error(msg)
            flash(msg, category="error")
            return redirect(url_for("strava.login"))

        try:
            data = resources.strava.client.exchange_token(request.args["code"])
        except tourmap.utils.strava.StravaBadRequest as e:
            msg = "Token exchange with Strava failed: {!r}".format(e.errors)
            current_app.logger.error(msg)
            flash(msg, category="error")
            return redirect(url_for("strava.login"))

        new_user, user = LoginController().strava_login(data)

        # At this point we can be somewhat sure the user has a Strava
        # account and that is good enough for us to log him in.
        current_app.logger.info("%s just logged in!", user)
        flask_login.login_user(tourmap.utils.UserProxy(user))

        if new_user:
            flash("Successfully connected with Strava. Thanks!", category="success")
            flash("Fetching your activities in the background now, "
                  "just refresh this page until they show up ;-)", category="info")

        # Not sure this is working properly... If we got here through a
        # redirect it should go back to the original page.
        try:
            return tourmap.utils.redirect_back(
                default_endpoint="users.user",
                next_candidate=state_dict.get("next"),
                user_hashid=user.hashid
            )
        except Exception as e:
            current_app.logger.exception("Redirect exception... %s", e)
            raise

    @bp.route("/authorize")
    def authorize():
        """
        Redirect the user to Strava asking to authorize our app.
        """
        app.logger.info("Strava authorize call!")

        # XXX: This may break behind a proxy, or maybe not?
        components = (request.scheme, request.host, url_for("strava.callback"),
                      None, None, None)
        redirect_uri = urlunparse(components)

        state = {
            "state": "CONNECT",
        }
        if request.args.get("next"):
            state["next"] = request.args.get("next")

        return redirect(resources.strava.client.authorize_redirect_url(
            redirect_uri=redirect_uri,
            scope=["read", "activity:read_all"],
            state=urlencode(state),
            approval_prompt="auto"
        ))

    return bp
