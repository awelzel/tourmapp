import logging
import dateutil.parser

from tourmap import database
from tourmap.utils import strava

logger = logging.getLogger(__name__)

def sync_activities(user_id):
    user = database.User.query.filter_by(id=user_id).one()
    token = user.token.access_token

    client = strava.StravaClient.from_env()
    page = 1
    while True:
        logger.info("Fetching page %d...", page)
        activities = list(client.activities(token=token, page=page, per_page=16))
        if not activities:
            break

        for src in activities:
            # get_or_create approach based on strava id
            activity = database.Activity.query.filter_by(strava_id=src["id"]).one_or_none()
            if activity is None:
                activity = database.Activity(
                    user=user,
                    strava_id=src["id"]
                )
            else:
                if activity.user_id != user.id:
                    raise Exception("not good...")

            # Should check if we need to update!
            activity.update_from_strava(src)
            database.db.session.add(activity)

        logger.info("DIRTY OBJECTS: %s", repr(database.db.session.dirty))
        database.db.session.commit()

        page += 1

    logger.info("Done!")
