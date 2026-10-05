from string import Template
from urllib.parse import parse_qsl, urlencode

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

    @staticmethod
    def getDefinition(heatmapColor, stravaEmail, stravaPassword):
        """Legacy login-and-generate API, retained for existing CLI callers."""
        from stravacookies import StravaCookieFetcher

        fetcher = StravaCookieFetcher()
        fetcher.fetchCookies(stravaEmail, stravaPassword)
        cookies = dict(parse_qsl(fetcher.getCookieString(), keep_blank_values=True))
        return OnlineMap.getDefinitionFromCookies(heatmapColor, cookies)

    @staticmethod
    def getDefinitionFromCookies(heatmapColor, cookies, *, maxZoom=22):
        """Generate a Cartograph definition without login, browser or network.

        cookies maps Key-Pair-Id, Policy and Signature to nonempty strings.
        The caller owns authorization validity/renewal. The legacy maximum zoom
        remains 22; pass maxZoom=15 to limit to the verified native TMS level.
        """
        if heatmapColor not in OnlineMap.COLORS:
            raise ValueError("Unsupported heatmap color")
        names = ("Key-Pair-Id", "Policy", "Signature")
        if not all(isinstance(cookies.get(k), str) and cookies[k] for k in names):
            raise ValueError("Three nonempty signed heatmap parameters are required")
        if type(maxZoom) is not int or not 2 <= maxZoom <= 22:
            raise ValueError("maxZoom must be an integer between 2 and 22")
        cookieString = urlencode({k: cookies[k] for k in names})

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
                "maxZoom": maxZoom,
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
