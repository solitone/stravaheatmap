import os
import datetime
from shutil import copy
import xml.etree.ElementTree as ET

from stravacookies.fetcher import StravaCookieFetcher

class ImgUpdater(object):
    def __init__(self):
        self.josmPreferences = "./fakepath.xml" # has to be set in OS-specific constructor
        self.cookieFetcher=StravaCookieFetcher() # may be overridden in OS-specific constructor

    def bakPrefs(self):
        bakfile = self.josmPreferences + '.' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.bak'
        copy(self.josmPreferences, bakfile)

    def updPrefs(self, stravaEmail, stravaPassword):
        stravaCookieFetcher = self.cookieFetcher
        stravaCookieFetcher.fetchCookies(stravaEmail, stravaPassword)
        cookieString = stravaCookieFetcher.getCookieString()
        ET.register_namespace('', "http://josm.openstreetmap.de/preferences-1.0")
        doc = ET.parse(self.josmPreferences)
        root = doc.getroot()
        for maptag in doc.findall("./{http://josm.openstreetmap.de/preferences-1.0}maps/{http://josm.openstreetmap.de/preferences-1.0}map/{http://josm.openstreetmap.de/preferences-1.0}tag[@key='url']"):
            if "strava.com" in maptag.attrib["value"]:
                print("Updating Strava Imagery URL...")
                fullUrl = maptag.attrib["value"]
                splittedUrl = fullUrl.split('?')
                baseUrl = splittedUrl[0]
                print("--> [" + baseUrl + "]")
                fullUrl = baseUrl + "?" + cookieString
                maptag.attrib["value"] = fullUrl
        print("Writing out preferences.xml...")
        doc.write(self.josmPreferences, encoding="UTF-8")


class MacOsImgUpdater(ImgUpdater):
    def __init__( self ):
        super().__init__()
        self.josmPreferences = os.path.expanduser('~/Library/Preferences/JOSM/preferences.xml')


class LinuxImgUpdater(ImgUpdater):
    def __init__( self ):
        super().__init__()
        # On Linux, three possible locations for JOSM preference file
        # according to https://josm.openstreetmap.de/wiki/Help/Preferences
        # (plus, users may specify a custom directory within JOSM;
        # this script doesn't support that)
        pref = os.path.expanduser('~/.josm/preferences.xml')
        if not os.path.isfile( pref ):
            try:
                pref = os.path.join(
                    os.environ['XDG_CONFIG_HOME'],
                    'JOSM', 'preferences.xml')
            except KeyError:
                pref = os.path.expanduser('~/.config/JOSM/preferences.xml')
        if not os.path.isfile( pref ):
            message = "Supported locations of preferences.xml:\n"
            message+= "~/.josm/, $XDG_CONFIG_HOME/JOSM, or ~/.config/JOSM\n"
            message+= "(custom preference locations are not supported)"
            raise StravaCFetchJosmprefsError(message)
        self.josmPreferences = pref


class WindowsImgUpdater(ImgUpdater):
    def __init__( self ):
        super().__init__()
        self.josmPreferences = os.path.join(
            os.path.expandvars('%APPDATA%\JOSM'),
            'preferences.xml')
        # location of JOSM preference file for Windows
        # according to https://josm.openstreetmap.de/wiki/Help/Preferences
        if not os.path.isfile( self.josmPreferences ):
            message = "Expect preferences.xml to sit in %APPDATA%\JOSM"
            raise StravaCFetchJosmprefsError(message)
