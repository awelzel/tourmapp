import logging
logger = logging.getLogger(__name__)

from flask import current_app


MAPBOX_ATTRIBUTION = (
    'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, '
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, '
    'Imagery &copy <a href="http://mapbox.com">Mapbox</a>'
)
MAPBOX_URL = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={access_token}'

class TourController(object):


    def _pdict(self, p):
        return {
            "url": p["url"],
            "height": p["height"],
            "width": p["width"],
        }

    def _prepare_photos(self, activity):
        """
        Create a list with entries:

        [
            {
                "url": ...
                "width": ...
                "height": ...
                "caption": ...
                "large": {
                    "url": ...
                    "width": ...
                    "height": ...
                }
            }
        ]
        """
        result = []

        if not activity.photos:
            return result

        photos = activity.photos.get_photos()
        keys = list(photos.keys())
        if not keys:
            return result

        if len(keys) != 2:
            logger.warning("Got weird sizes %s for %s", repr(keys), activity)

        large = max(keys)
        small = min(keys)
        large_dict = {p["unique_id"]: self._pdict(p) for p in photos[large]}
        result = []
        for p in photos[small]:
            pdict = self._pdict(p)
            pdict["large"] = large_dict[p["unique_id"]]
            pdict["caption"] = p.get("caption")
            result.append(pdict)
        return result

    def prepare_activities_for_map(self, tour):
        """
        Prepare activity data to be displayed on a map.

        # Naive sampling:
        # "latlngs": [latlngs[0]] + latlngs[8:-7:8] + [latlngs[-1]],
        """
        activities = []
        for a in tour.activities:
            latlngs = list(a.latlngs)
            if not latlngs:
                continue

            photos = self._prepare_photos(a)
            activities.append({
                "name": a.name,
                "date": a.start_date_local.date().isoformat(),
                "latlngs": latlngs,
                "photos": photos,
            })
        return activities

    def _find_bounds(self, prepared_activities):
        """Helper to find corner1 and corner2 values"""
        lat_min, lat_max = (90, -90)
        lng_min, lng_max = (180, -180)
        for a in prepared_activities:
            if not a["latlngs"]:
                continue

            latlngs = a["latlngs"]
            lat_min = min(lat_min, min([ll[0] for ll in latlngs]))
            lat_max = max(lat_max, max([ll[0] for ll in latlngs]))
            lng_min = min(lng_min, min([ll[1] for ll in latlngs]))
            lng_max = max(lng_max, max([ll[1] for ll in latlngs]))

        return [(lat_min, lng_min), (lat_max, lng_max)]


    def get_map_settings(self, tour, prepared_activities):
        result = {}

        tile_layer_id = "mapbox.streets"
        polyline_color = "red"
        polyline_weight = 5

        result["tile_layer"] = {
            "provider": "mapbox",
            "url_template": MAPBOX_URL,
            "options": {
                "access_token": current_app.config["MAPBOX_ACCESS_TOKEN"],
                "max_zoom": 18,
                "attribution": MAPBOX_ATTRIBUTION,
                "id": tile_layer_id,
            }
        }


        corner1, corner2 = self._find_bounds(prepared_activities)

        result["bounds"] = {
            "corner1": corner1,
            "corner2": corner2,
        }

        # Compute max mounds as percentage of the difference and some
        # more freaking heuristics...
        max_wiggle = 0.15
        lat_wiggle = max(abs(corner1[0] - corner2[0]) * max_wiggle, 5.0)
        lng_wiggle = max(abs(corner1[1] - corner2[1]) * max_wiggle, 5.0)
        print(corner1, corner2)
        print(lat_wiggle, lng_wiggle)
        result["max_bounds"] = {
            "corner1": (corner1[0] - lat_wiggle, corner1[1] - lng_wiggle),
            "corner2": (corner2[0] + lat_wiggle, corner2[1] + lng_wiggle),
        }

        result["polyline"] = {
            "options": {
                "color": polyline_color,
                "weight": polyline_weight,
            }
        }

        return result
