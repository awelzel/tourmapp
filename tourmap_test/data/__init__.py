# Copied from the DB...
import json
import dateutil.parser

# as returned by strava...
activity1_dict = {'achievement_count': 31,
 'athlete': {'id': 11176987, 'resource_state': 1},
 'athlete_count': 1,
 'average_heartrate': 101.9,
 'average_speed': 5.639,
 'average_temp': 27.0,
 'average_watts': 151.2,
 'comment_count': 0,
 'commute': False,
 'device_watts': False,
 'distance': 131143.0,
 'elapsed_time': 28234,
 'elev_high': 1376.2,
 'elev_low': 304.0,
 'end_latlng': [18.778952, 98.984456],
 'external_id': 'garmin_push_2337663742',
 'flagged': False,
 'from_accepted_tag': False,
 'gear_id': 'b3785475',
 'has_heartrate': True,
 'has_kudoed': False,
 'id': 1280026117,
 'kilojoules': 3516.0,
 'kudos_count': 8,
 'location_city': None,
 'location_country': 'Germany',
 'location_state': None,
 'manual': False,
 'map': {'id': 'a1280026117',
  'resource_state': 2,
  'summary_polyline': r'c{cuBy`zwQf@lI~d@o~@lSL~CqRhc@|NrtCob@tbAi`Ap`AgHbBuQb}@yM[}l@zr@svAfnAk|@yAuqAsSiRcEe]vIsWmJqLvAie@_OuVhIgK}Nea@xQc}@_KyP`GqN{Kg\\hGeMkGq^vf@w_@aA}i@gZuu@o`@iFoJk[bYwZuYwLFsWlRim@`^sOdJob@vm@gVcBaYhh@iHpVvNrG}\\oSmL}QtIpQsg@nf@oFSoMpYyXrLbGjDwVf`@~AiMiD`CyLdYeEzBgi@tQoOp_@iKa[|Vpp@wMdHf@yP|Er@`JjbBaE}Bed@~{@go@nJ_a@|dAsPl|BpLt}@gNbxAee@`YaWgIeAlZcEg@mVjU}DtAtOpf@{WgBmX~Vke@cAyc@rLcb@uWma@i\\jK`Ekc@cMuQnDkPpHnD{OkQ}Agh@nPgb@eL_X~No\\_HoQ~I{b@nl@{b@~r@goB|B_u@|a@mb@gVq]_Ngv@vL_PkBkXzcAeoAbNsiAfNcTw]_o@|GiaAh_@_h@rJye@eIeh@ftAseDfLew@pwD_r@buChMtgCwJpfG~FfzDvb@jx@ua@thD{~@xbAsi@rmCse@voGudBn_AmHxHuOfDjMxNa@lBan@~vAxDp@p\\vQpEpB~VsHkE'},
 'max_heartrate': 162.0,
 'max_speed': 19.9,
 'moving_time': 23256,
 'name': 'Pai to Chiang Mai - 762 twists and turns, or so they say',
 'photo_count': 0,
 'pr_count': 31,
 'private': False,
 'resource_state': 2,
 'start_date': '2017-11-18T02:16:00Z',
 'start_date_local': '2017-11-18T09:16:00Z',
 'start_latitude': 19.358107,
 'start_latlng': [19.358107, 98.442535],
 'start_longitude': 98.442535,
 'timezone': '(GMT+07:00) Asia/Bangkok',
 'total_elevation_gain': 1715.0,
 'total_photo_count': 1,
 'trainer': False,
 'type': 'Ride',
 'upload_id': 1386710672,
 'utc_offset': 25200.0,
 'workout_type': 10
}

# Sizes are 306/306, for whatever reason (Instagram!)
photos2_dict = json.loads(r'{"unique_id": null, "activity_id": 490862480, "activity_name": "Morning Ride", "default_photo": false, "source": 2, "id": 120366754, "created_at": "2016-02-11T11:05:39Z", "sizes": {"256": [306, 306]}, "urls": {"256": "https://www.instagram.com/p/BBpAhGxjDeUjflJbQ5nwiDgkVjpfBdAp0uJIPo0/media?size=m"}, "created_at_local": "2016-02-11T12:05:39Z", "uploaded_at": "2016-02-11T09:21:01Z", "resource_state": 2, "post_id": null, "type": "InstagramPhoto", "ref": "https://www.instagram.com/p/BBpAhGxjDeUjflJbQ5nwiDgkVjpfBdAp0uJIPo0/", "caption": null, "uid": "1182478652177921940_2515825780", "athlete_id": 3966901}')

poller_crash_results1 = json.loads(r'{"activity_infos": [{"activity": {"id": 986628180, "resource_state": 2, "external_id": "2017-05-14-171219-ELEMNT 5F59-14-0.fit", "upload_id": 1089528309, "athlete": {"id": 12120243, "resource_state": 1}, "name": "Big Basin", "distance": 52306.0, "moving_time": 9144, "elapsed_time": 12338, "total_elevation_gain": 1228.0, "type": "Ride", "start_date": "2017-05-14T17:12:19Z", "start_date_local": "2017-05-14T10:12:19Z", "timezone": "(GMT-08:00) America/Los_Angeles", "utc_offset": -25200.0, "start_latlng": [37.21, -122.16], "end_latlng": [37.21, -122.16], "location_city": null, "location_state": null, "location_country": "United States", "start_latitude": 37.21, "start_longitude": -122.16, "achievement_count": 2, "kudos_count": 10, "comment_count": 0, "athlete_count": 2, "photo_count": 0, "map": {"id": "a986628180", "summary_polyline": "mdcbFjsqhVcNwFcHePu_@tH}P_HlAw]sIx@_GbIaHeH_MrEkLyDyIiNi\\zYyKtXuGbAeLoPiT|NjAsMvVeo@a@qLq[}\\a_@cPyCmIa@se@kQk]tBcCyBxGvQvYAjc@nEhKlObLfLz@bUbQzFrLXdKaYrv@XdHfT{QrJhRbJk@rJ{Xn\\oYpH~LtMjFjLaFpIxH`IoIrFDyCpXjPdK``@cHlJfNb\\|LlP}Cr]fK|FiEwB|NpFdRzJ`InUiFzDpZlH~HvA~_@uJtKGfMoLnP}Zf{@g@fO|GhEiAjJdBzAzQ_TnDpBuA|IjBqKlPmAXsJtf@eTtH{QpC_Zfb@cXrIiV`JwEvH}NdGcUtPgQ~ZoAy_@jp@fCgRaB{@oRlq@zCzLlGjF[xQdFzQvM`FxLzPf@~W`K`[wG`IgFgAuEcKuDxF`Mf^cPns@eArz@_GpFqJMgEkC?uIyKvCeCmFjCkJyGkGcx@iWkOnKcGuF_[oCiQuOy@_e@jEcF{DoJ~Ecf@yCeCoDlJcPhInAuIcImCq@gMrZir@PkI`K}M~@gNtLkOcDuQrB_OcIkG{D_`@qStGcNwHuD_PnCcQ}OdEyLiBiFsGkQzDcMcE", "resource_state": 2}, "trainer": false, "commute": false, "manual": false, "private": false, "flagged": false, "gear_id": "b2955320", "from_accepted_tag": false, "average_speed": 5.72, "max_speed": 19.5, "average_temp": 9.0, "average_watts": 160.3, "kilojoules": 1465.6, "device_watts": false, "has_heartrate": false, "elev_high": 821.0, "elev_low": 271.0, "pr_count": 1, "total_photo_count": 0, "has_kudoed": false, "workout_type": 10}, "photos": {}}, {"activity": {"id": 984963118, "resource_state": 2, "external_id": "2017-05-13-183844-ELEMNT 5F59-13-0.fit", "upload_id": 1087566775, "athlete": {"id": 12120243, "resource_state": 1}, "name": "Lunch Ride", "distance": 42636.3, "moving_time": 7581, "elapsed_time": 16897, "total_elevation_gain": 590.0, "type": "Ride", "start_date": "2017-05-13T18:38:44Z", "start_date_local": "2017-05-13T11:38:44Z", "timezone": "(GMT-08:00) America/Los_Angeles", "utc_offset": -25200.0, "start_latlng": [37.75, -122.39], "end_latlng": [37.75, -122.39], "location_city": null, "location_state": null, "location_country": "United States", "start_latitude": 37.75, "start_longitude": -122.39, "achievement_count": 18, "kudos_count": 6, "comment_count": 0, "athlete_count": 2, "photo_count": 0, "map": {"id": "a984963118", "summary_polyline": "{jleFzy_jVjIHhAfcAbFjZ`B|wA~P@tk@dPzQ|VnHlWoHpm@uE~Hb@bIaBVmEaGyLh@cIdSeGzCsBxPwMfKS`BrHxNpLfJ~C`HpHxr@r[lb@rEj{ClZp[zVhK}DlK_E`D}a@jEuLsA[mF{AxCm@gDwC@uaB|Ew@zEuTp@aBmm@mq@jB}BcA]_KaEcRNuJqHc]cDe^oN{j@UiIxDkTwJeVuwAtDpAzXmDf@}B_Eo\\sNyFqG_EtAuGkRXkC`FmEl@yCyH~MnGpQ[dBgECkH_HwB~FqCJsAsAPsDkAkBeQ_A{E~BvCyf@qCgMjBs@wBn@pClM{Cnf@jFcBnPb@wD_JwEeEr@qNdE{ExHfAbJ{UeFaFh@eEiGoSjDmEtDeLiD{GxD}AaH_dAfDoAQwHhDYrBxRzkDmc@d\\sA_Bwv@bIcB{J_eDtFe@c@yU`Aa@~c@_Cr@rJlM_@d@lD|@L", "resource_state": 2}, "trainer": false, "commute": false, "manual": false, "private": false, "flagged": false, "gear_id": "b2955320", "from_accepted_tag": false, "average_speed": 5.624, "max_speed": 15.4, "average_temp": 18.0, "average_watts": 148.7, "kilojoules": 1127.2, "device_watts": false, "has_heartrate": false, "elev_high": 188.0, "elev_low": 4.0, "pr_count": 6, "total_photo_count": 0, "has_kudoed": false, "workout_type": null}, "photos": {}}, {"activity": {"id": 981446234, "resource_state": 2, "external_id": "2017-05-11-133312-ELEMNT 5F59-10-0.fit", "upload_id": 1083382032, "athlete": {"id": 12120243, "resource_state": 1}, "name": "Morning Ride", "distance": 35270.6, "moving_time": 5516, "elapsed_time": 7634, "total_elevation_gain": 308.0, "type": "Ride", "start_date": "2017-05-11T13:33:12Z", "start_date_local": "2017-05-11T06:33:12Z", "timezone": "(GMT-08:00) America/Los_Angeles", "utc_offset": -25200.0, "start_latlng": [37.72, -122.4], "end_latlng": [37.57, -122.32], "location_city": null, "location_state": null, "location_country": "United States", "start_latitude": 37.72, "start_longitude": -122.4, "achievement_count": 11, "kudos_count": 8, "comment_count": 0, "athlete_count": 2, "photo_count": 0, "map": {"id": "a981446234", "summary_polyline": "}gfeF|kajVz_@eFlDbMhIz@~BbEbN~Inq@~UtIg@|k@kTiArI}UrMsE`KMvUiHvc@dBnG~LjJzAvHu@~DcL|Qg@lFlBpFhKjF~@~F{E|QoJ~QcQ~q@jCrH|OlCfRzN`GfQpKpD~JrYbQ_DdJkFpPuQnkA{kCvMyUxCiM`n@tM~\\ufCn@cAdTjFxGiEu@yHxCcKr@e[t\\oGhEtAfAgBlHdHxAdLrq@{Z`EzMlJxF`Wy@z}@aVvAmCdA{Rl\\_Jvg@a}@]}PmCyHjCwGlAt@w@qB~Ms_@vRsVxe@{SnEoMoBcJMem@`M_TpAwc@m@yEkGoLMq[vTeCuBcQNkHhG{ArAqIi@gEgFsHkEuYrHsEdBcDRyEvLcGtReUjaAj_BpGoG]yCtHyHm@eBv@oBjCb@", "resource_state": 2}, "trainer": false, "commute": false, "manual": false, "private": false, "flagged": false, "gear_id": "b2955320", "from_accepted_tag": false, "average_speed": 6.394, "max_speed": 14.8, "average_temp": 9.0, "average_watts": 140.4, "kilojoules": 774.7, "device_watts": false, "has_heartrate": false, "elev_high": 224.0, "elev_low": 4.0, "pr_count": 3, "total_photo_count": 0, "has_kudoed": false, "workout_type": null}, "photos": {}}, {"activity": {"id": 981285468, "resource_state": 2, "external_id": "2017-05-11-131821-ELEMNT 5F59-9-12.fit", "upload_id": 1083191703, "athlete": {"id": 12120243, "resource_state": 1}, "name": "Morning Ride", "distance": 0.0, "moving_time": 860, "elapsed_time": 860, "total_elevation_gain": 0.0, "type": "Ride", "start_date": "2017-05-11T13:18:21Z", "start_date_local": "2017-05-11T06:18:21Z", "timezone": "(GMT-08:00) America/Los_Angeles", "utc_offset": -25200.0, "start_latlng": null, "end_latlng": null, "location_city": null, "location_state": null, "location_country": "United States", "start_latitude": null, "start_longitude": null, "achievement_count": 0, "kudos_count": 3, "comment_count": 0, "athlete_count": 1, "photo_count": 0, "map": {"id": "a981285468", "summary_polyline": null, "resource_state": 2}, "trainer": true, "commute": false, "manual": false, "private": false, "flagged": false, "gear_id": "b2955320", "from_accepted_tag": false, "average_speed": 0.0, "max_speed": 0.0, "average_temp": 7.0, "average_watts": 0.0, "device_watts": false, "has_heartrate": false, "pr_count": 0, "total_photo_count": 0, "has_kudoed": false, "workout_type": null}, "photos": {}}], "state_update": {"full_fetch_next_page": 31, "full_fetch_per_page": 4, "full_fetch_completed": false, "total_fetches": 30, "last_fetch_completed_at": "2017-12-05T18:04:41.398959"}}')
poller_crash_results1["state_update"]["last_fetch_completed_at"] = dateutil.parser.parse(poller_crash_results1["state_update"]["last_fetch_completed_at"])
db_photos1_dict = {"256": [{"caption": "", "height": 192, "source": 1, "unique_id": "9B0AA5E9-8849-4C33-8C25-C3B4F0527A8C", "url": "https://dgtzuqphqg23d.cloudfront.net/k4hEhUdJC9qW3idBYxwL-xMZwsDvWT5oIjLQE6g_z24-256x192.jpg", "width": 256}, {"caption": "", "height": 192, "source": 1, "unique_id": "1F488127-1676-408E-AA26-5AF9F8D9CDCE", "url": "https://dgtzuqphqg23d.cloudfront.net/4qQuqA6YJFF4LNvwH5t-3sjZmZIMaVOFgRI83CLXXAY-256x192.jpg", "width": 256}, {"caption": "", "height": 192, "source": 1, "unique_id": "755A22CB-907C-47DF-B7D1-068B8755DE97", "url": "https://dgtzuqphqg23d.cloudfront.net/w5bUb3iE4VqzUBd3ApEoE7lL1d8w8mX1Zw81D1dKjHA-256x192.jpg", "width": 256}, {"caption": "", "height": 192, "source": 1, "unique_id": "48013B93-43DF-43FB-AFBD-8A1B1061E61D", "url": "https://dgtzuqphqg23d.cloudfront.net/cJhwZByVzhwG6Aoh9WNR0qsmiXH_o5qI9fFRRsNkwaI-256x192.jpg", "width": 256}], "1024": [{"caption": "", "height": 768, "source": 1, "unique_id": "9B0AA5E9-8849-4C33-8C25-C3B4F0527A8C", "url": "https://dgtzuqphqg23d.cloudfront.net/k4hEhUdJC9qW3idBYxwL-xMZwsDvWT5oIjLQE6g_z24-1024x768.jpg", "width": 1024}, {"caption": "", "height": 768, "source": 1, "unique_id": "1F488127-1676-408E-AA26-5AF9F8D9CDCE", "url": "https://dgtzuqphqg23d.cloudfront.net/4qQuqA6YJFF4LNvwH5t-3sjZmZIMaVOFgRI83CLXXAY-1024x768.jpg", "width": 1024}, {"caption": "", "height": 768, "source": 1, "unique_id": "755A22CB-907C-47DF-B7D1-068B8755DE97", "url": "https://dgtzuqphqg23d.cloudfront.net/w5bUb3iE4VqzUBd3ApEoE7lL1d8w8mX1Zw81D1dKjHA-1024x768.jpg", "width": 1024}, {"caption": "", "height": 768, "source": 1, "unique_id": "48013B93-43DF-43FB-AFBD-8A1B1061E61D", "url": "https://dgtzuqphqg23d.cloudfront.net/cJhwZByVzhwG6Aoh9WNR0qsmiXH_o5qI9fFRRsNkwaI-1024x768.jpg", "width": 1024}]}
