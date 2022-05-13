from string import Template
from stravacookies import StravaCookieFetcher

class OnlineMap(object):
# Constants:
## Heatmap colors
    COLORS = {  "hot": "hot",
                "blue": "blue",
                "purple": "purple",
                "gray": "gray",
                "red": "bluered"}

## Heatmap activities
    ACTIVITIES = {  "all": "all",
                    "ride": "ride",
                    "run": "run",
                    "winter": "winter"}

## Names that will be given to heatmaps based on their activity
    MAPNAMES = {"all": "Strava Heatmap (all)",
                "ride": "Strava Heatmap (ride)",
                "run": "Strava Heatmap (run)",
                "winter": "Strava Heatmap (winter)"}

## Heatmap URLs will be generated from the following template,
## replacing placeholders 'activity', 'color', and 'cookieString' with actual values
    URL_TEMPLATE = Template("https://heatmap-external-a.strava.com/tiles-auth/$activity/$color/{z}/{x}/{y}.png?$cookieString")

    def getDefinition(heatmapColor, stravaEmail, stravaPassword):
# Returns a python dictionary representing an online map definition;
# dumping that dictionary to a json file results in an
# online map definition file that can be imported into Cartograph Maps
        stravaCookieFetcher = StravaCookieFetcher()
        stravaCookieFetcher.fetchCookies(stravaEmail, stravaPassword)
        cookieString = stravaCookieFetcher.getCookieString()

        maps = []

        for key in OnlineMap.ACTIVITIES:
            url = OnlineMap.URL_TEMPLATE.substitute(activity = OnlineMap.ACTIVITIES[key], color = OnlineMap.COLORS[heatmapColor], cookieString = cookieString)

            map = {
                "name": OnlineMap.MAPNAMES[key],
                "type": "ONLINE", # Possible values: "ONLINE" or "WMS"
                "url": url,
                "attribution": "© Strava",
                "description": "",
                "defaultLatitude": 45.0781,
                "defaultLongitude": 7.6761,
                "defaultZoom": 11,
                "minZoom": 2,
                "maxZoom": 22,
                "projection": "EPSG_4326", # Possible values: "EPSG_4326" (default) or "EPSG_900913"
                "headers": [
                    {
                    "key": "User-Agent",
                    "value": "Cartograph"
                    }
                ]
            }
            maps.append(map)

        onlineMapDef = {
            "version": 2,
            "maps": maps
        }

        return onlineMapDef
