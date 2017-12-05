import datetime
import unittest.mock
import uuid

import tourmap_test
import tourmap_test.data

from tourmap.models import Activity, User, Tour, PollState, Token
from tourmap.resources import db
from tourmap.utils import dt2ts
from tourmap.utils.json import dumps
from tourmap.utils.objpool import ObjectPool
from tourmap.utils.strava import StravaClient, StravaBadRequest

from tourmap.tasks.strava_poller import StravaPoller


class StravaPollerTest(tourmap_test.TestCase):

    def setUp(self):
        super().setUp()
        self.session = db.session

        self.strava_client_mock = unittest.mock.Mock(spec=StravaClient)
        self.user = User(strava_id=123, email="auser@strava.com")
        self.buser = User(strava_id=124, email="buser@strava.com")
        self.cuser = User(strava_id=125, email="cuser@strava.com")
        self.tour = Tour(user=self.user, name="Simple Test Tour")
        self.token = Token(user=self.user, access_token=uuid.uuid4().hex)
        self.poll_state = PollState(user=self.user)
        self.session.add_all([self.user, self.buser, self.cuser, self.token, self.tour, self.poll_state])
        self.session.commit()

        self.strava_client_pool = ObjectPool(lambda: self.strava_client_mock)
        self.strava_poller = StravaPoller(self.session, self.strava_client_pool)

    def test_get_states__no_states_in_db(self):
        self.session.delete(self.poll_state)
        self.session.commit()

        states = list(self.strava_poller._get_poll_states())
        self.assertEqual(0, len(states))

    def test_get_poll_states__single_state(self):
        states = list(self.strava_poller._get_poll_states())
        self.assertEqual(1, len(states))

    def test_get_poll_states__full_fetch_completed_states(self):
        poll_state1 = PollState(user=self.buser, full_fetch_completed=True)
        poll_state2 = PollState(
            user=self.cuser,
            full_fetch_completed=True,
            last_fetch_completed_at=datetime.datetime.utcnow(), # This should not show up
        )
        self.session.add_all([poll_state1, poll_state2])
        self.session.commit()
        states = list(self.strava_poller._get_poll_states())
        self.assertEqual(2, len(states))


    def test_fetch_activities__full_fetch_mode(self):
        self.strava_client_mock.activities.return_value = []
        result = self.strava_poller.fetch_activities(self.user, self.token, self.poll_state)
        self.strava_client_mock.activities.assert_called_once_with(
            page=1,
            per_page=4,
            token=self.token.access_token
        )

        self.assertTrue(result["state_update"]["full_fetch_completed"])
        self.assertEqual(2, result["state_update"]["full_fetch_next_page"])
        self.assertEqual(4, result["state_update"]["full_fetch_per_page"])
        self.assertIsInstance(
            result["state_update"]["last_fetch_completed_at"],
            datetime.datetime
        )

    def test_fetch_activities__latest_fetch_mode(self):
        last_fetch_completed_at = datetime.datetime(2017, 7, 1)
        self.poll_state.last_fetch_completed_at = last_fetch_completed_at
        self.poll_state.full_fetch_completed = True
        self.session.add(self.poll_state)
        self.session.commit()

        expected_after_ts = dt2ts(last_fetch_completed_at - datetime.timedelta(days=14))
        self.strava_client_mock.activities.return_value = []
        result = self.strava_poller.fetch_activities(self.user, self.token, self.poll_state)
        self.strava_client_mock.activities.assert_called_once_with(
            after=expected_after_ts,
            token=self.token.access_token,
            per_page=50
        )

        self.assertTrue(result["state_update"]["total_fetches"])
        self.assertIsInstance(
            result["state_update"]["last_fetch_completed_at"],
            datetime.datetime
        )

    def test_json_dumps(self):
        serialize_this = {
            "now": datetime.datetime.utcnow(),
            "today": datetime.date.today(),
            "array": [
                1, "Stuff", {}
            ]
        }
        result = dumps(serialize_this)

    def test_process_results_crash1(self):
        from tourmap_test.data import poller_crash_results1
        self.strava_poller._process_result(
            poll_state_id=self.poll_state.id,
            result=poller_crash_results1,
            submit_kwargs=None
        )
        self.assertEqual(4, Activity.query.count())

        # This one did not have start/end latlng values, check it!
        strava_id = 981285468
        a = Activity.query.filter_by(strava_id=strava_id).one()
        self.assertEqual("Morning Ride", a.name)
        self.assertIsNone(a.summary_polyline)
        self.assertEqual(0, len(a.latlngs))
        self.assertIsNone(a.start_lat)
        self.assertIsNone(a.start_lng)
        self.assertIsNone(a.end_lat)
        self.assertIsNone(a.end_lng)

        # This one had some start/end latlngs...
        strava_id = 981446234
        a = Activity.query.filter_by(strava_id=strava_id).one()
        self.assertEqual(5516, a.moving_time)
        self.assertEqual(7634, a.elapsed_time)
        self.assertTrue(a.summary_polyline)
        self.assertEqual(96, len(a.latlngs))
        self.assertAlmostEqual(37.72, a.start_lat)
        self.assertAlmostEqual(-122.4, a.start_lng)
        self.assertAlmostEqual(37.57, a.end_lat)
        self.assertAlmostEqual(-122.32, a.end_lng)
