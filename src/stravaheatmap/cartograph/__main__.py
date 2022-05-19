# -*- coding: utf-8 -*-

import json
import platform
import sys

from pathlib import Path

from colorama import Fore, Style
from getpass import getpass

from .onlinemap import OnlineMap
from stravacookies import StravaCFetchCookieError

# Set location where output file will be written
outdir = "./"
print("If you are on MacOS, you can save the map file directly in the Cartograph folder")
print("in iCloud, otherwise it will be saved in the current working directory.")
while True:
    print("Do you want to save the map file in iCloud (y/N)?")
    answer = input()
    if (answer == "y" or answer == "Y"):
        outdir = str(Path.home()) + "/Library/Mobile Documents/com~apple~CloudDocs/Cartograph Pro/"
        break
    elif (answer == "n" or answer == "N" or answer == ""):
        # leave outdir unchanged
        break


print("What map color do you want?")
for color in OnlineMap.COLORS:
    print ("  " + color)
while True:
    print("?")
    answer = input()
    if answer in OnlineMap.COLORS:
        break
color = answer

stravaEmail = input(f"{Fore.CYAN}**** Enter your Strava account email:{Style.RESET_ALL} ")
stravaPassword = getpass(f"{Fore.CYAN}**** Enter your Strava account password:{Style.RESET_ALL} ")

try:
    print("Creating online map definition file... ", end="", flush=True)

    onlineMapDef = OnlineMap.getDefinition(color, stravaEmail, stravaPassword)

    print(json.dumps(onlineMapDef), file=open(outdir + "carto_strava.onlinemap", "w"))
    print("done.")

except StravaCFetchCookieError as e:
    print("Strava cookies unavailable.", file=sys.stderr)
    print(e.message, file=sys.stderr)
except Exception as e:
    print("An error has occurred: " + e.message, file=sys.stderr)
