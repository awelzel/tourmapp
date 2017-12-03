import json

import dateutil.parser
import hashids
import polyline
from sqlalchemy.schema import Index, UniqueConstraint

from tourmap.database import db
from tourmap.utils import seconds_to_readable_interval


class HashidMixin(object):

    @classmethod
    def __get_Hashids(cls):
        # XXX" This is ugly
        from tourmap.app import app
        salt = app.config["HASHIDS_SALT"]
        salt = "{}{}".format(cls.__name__, salt)
        min_length = app.config["HASHIDS_MIN_LENGTH"]
        return hashids.Hashids(salt, min_length=min_length)

    @classmethod
    def get_by_hashid(cls, hashid):
        id = cls.__get_Hashids().decode(hashid)
        if len(id) != 1:
            return None
        return cls.query.get(id[0])

    @property
    def hashid(self):
        return self.__get_Hashids().encode(self.id)


class User(db.Model, HashidMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    strava_id = db.Column(db.BigInteger, unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255), nullable=True)
    lastname = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)

    @property
    def name_str(self):
        return " ".join(filter(None, [self.firstname, self.lastname]))

    @property
    def strava_link(self):
        """
        Hackish...
        """
        return "https://www.strava.com/athletes/{}".format(self.strava_id)


class Tour(db.Model, HashidMixin):
    __tablename__ = "tours"
    __table_args__ = (
        UniqueConstraint("user_id", "name",
                         name="uq_%(column_0_label)s %(column_1_name)s"),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(User)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    tilelayer_provider = db.Column(db.String(16), nullable=True)
    polyline_color = db.Column(db.String(16), nullable=True)

    @property
    def activities(self):
        query = Activity.query.filter_by(user=self.user)
        if self.start_date:
            query = query.filter(Activity.start_date >= self.start_date)
        if self.end_date:
            query = query.filter(Activity.start_date <= self.end_date)
        return query

    @property
    def start_date_str(self):
        return self.start_date.date().isoformat() if self.start_date is not None else ""

    @property
    def end_date_str(self):
        return self.end_date.date().isoformat() if self.end_date is not None else ""


User.tours = db.relationship(Tour, order_by=Tour.id)


class Activity(db.Model):
    """
    Most importantly, datetime, name and distance.
    """
    __tablename__ = "activities"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    strava_id = db.Column(db.BigInteger, unique=True, nullable=False)
    external_id = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(32), nullable=False)

    name = db.Column(db.String(255), nullable=False)

    distance = db.Column(db.Float)
    moving_time = db.Column(db.Integer, nullable=False)
    elapsed_time = db.Column(db.Integer, nullable=False)
    total_elevation_gain = db.Column(db.Float)
    average_temp = db.Column(db.Float)

    start_date = db.Column(db.DateTime, nullable=False)
    start_date_local = db.Column(db.DateTime, nullable=False)
    utc_offset = db.Column(db.Integer, nullable=False)
    timezone = db.Column(db.String(64))

    start_lat = db.Column(db.Float)
    start_lng = db.Column(db.Float)
    end_lat = db.Column(db.Float)
    end_lng = db.Column(db.Float)
    summary_polyline = db.Column(db.Text)

    total_photo_count = db.Column(db.Integer)

    user = db.relationship(User)

    @property
    def latlngs(self):
        if self.summary_polyline:
            return polyline.decode(self.summary_polyline)
        return []

    @property
    def moving_time_str(self):
        return seconds_to_readable_interval(seconds=self.moving_time)

    @property
    def elapsed_time_str(self):
        return seconds_to_readable_interval(seconds=self.elapsed_time)

    @property
    def distance_str(self):
        """
        Cycling is all about kilometers! Suck it!
        """
        if self.distance is None:
            return ""

        suffix = "m"
        divisor = 1.0
        if self.distance > 1000.0:
            suffix = "km"
            divisor = 1000.0

        return "{:.1f} {}".format(self.distance / divisor, suffix)

    @property
    def elevation_gain_str(self):
        if self.total_elevation_gain is None:
            return "0 m"
        return "{:.1f} m".format(self.total_elevation_gain)

    @property
    def average_temp_str(self):
        if self.average_temp is None:
            return ""
        return "{:.0f} °C".format(self.average_temp)

    @property
    def strava_link(self):
        """
        Hackish...
        """
        return "https://www.strava.com/activities/{}".format(self.strava_id)

    def update_from_strava(self, src):
        """
        Update from a dict as provided by the Strava API with condition checks
        """
        if src.get("external_id") and self.external_id != src.get("external_id"):
            self.external_id = src["external_id"]

        if self.type != src["type"]:
            self.type = src["type"]

        if not self.name or self.name != src["name"]:
            self.name = src.get("name", "")

        start_date = dateutil.parser.parse(src["start_date"])
        if start_date.tzinfo is not None and start_date.utcoffset().seconds != 0:
            raise Exception("Non UTC date parsed! {!r}".format(src["start_date"]))
        start_date = start_date.replace(tzinfo=None)
        if self.start_date is None or self.start_date != start_date:
            self.start_date = start_date

        start_date_local = dateutil.parser.parse(src["start_date_local"])
        if start_date_local.tzinfo is not None:
            if start_date_local.utcoffset().seconds != 0:
                msg = "Non UTC date parsed! {!r}".format(start_date_local)
                raise Exception(msg)

        start_date_local = start_date_local.replace(tzinfo=None)
        if self.start_date_local is None or self.start_date_local != start_date_local:
            self.start_date_local = start_date_local

        if self.utc_offset is None or self.utc_offset != int(src["utc_offset"]):
            self.utc_offset = int(src["utc_offset"])

        if src.get("timezone") and self.timezone != src["timezone"]:
            self.timezone = src["timezone"]

        summary_polyline = src.get("map", {}).get("summary_polyline")
        if summary_polyline and self.summary_polyline != summary_polyline:
            self.summary_polyline = summpary_polyline

        # XXX: No check for changes here...
        start_latlng = src.get("start_latlng", [None, None])
        end_latlng = src.get("end_latlng", [None, None])
        self.start_lat, self.start_lng = start_latlng[0], start_latlng[1]
        self.end_lat, self.end_lng = end_latlng[0], end_latlng[1]
        self.distance = src.get("distance")
        self.moving_time = src.get("moving_time")
        self.elapsed_time = src.get("elapsed_time")
        self.total_elevation_gain = src.get("total_elevation_gain")
        self.average_temp = src.get("average_temp")
        self.total_photo_count = src.get("total_photo_count", 0)


User.activities = db.relationship(Activity, order_by=Activity.start_date_local.desc())


class Token(db.Model):
    __tablename__ = "tokens"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                        unique=True, nullable=False)
    access_token = db.Column(db.String(64), nullable=False)
    user = db.relationship(User, backref=db.backref("token", uselist=False))


class PollState(db.Model):
    """
    One row for each user we poll for.
    """
    __tablename__ = "strava_poll_states"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                        unique=True, nullable=False)
    user = db.relationship(User, backref=db.backref("poll_state", uselist=False))

    # If the user deletes activities while a full fetch is in progress,
    # we may miss some... Lets ignore for now and allow to trigger refetching.
    full_fetch_next_page = db.Column(db.SmallInteger)
    full_fetch_per_page = db.Column(db.SmallInteger)
    full_fetch_completed = db.Column(db.Boolean, default=False)
    last_fetch_completed_at = db.Column(db.DateTime)

    total_fetches = db.Column(db.BigInteger, default=0, nullable=False)

    def __repr__(self):
        return "<PollState {}>".format(self.id)

    # We currently do not want to fetch based on last_fetch_timestamp
    __table_args__ = (
        Index("ix_strava_poll_states_full_fetch_completed_at",
              "full_fetch_completed", "last_fetch_completed_at"),
    )


class ActivityPhotos(db.Model):
    __tablename__ = "activity_photos"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"), nullable=False)

    # A JSON map with sizes to lists of photos. Each photo is a map with
    # "width", "height", "url", "caption"
    json_blob = db.Column(db.TEXT)
    user = db.relationship(User)
    activity = db.relationship(Activity)

    def get_photos(self, size=256):
        d = json.loads(self.json_blob)
        return d.get(str(size), [])


Activity.photos = db.relationship(ActivityPhotos, order_by=ActivityPhotos.id,
                                  uselist=False)
