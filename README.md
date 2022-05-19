# stravaheatmap

A collection of utilities for providing the high resolution
[Strava Heatmaps](https://www.strava.com/heatmap)
to cartographic applications. Currently,
[JOSM](https://josm.openstreetmap.de) and
[Cartograph Maps](https://www.cartograph.eu)
are supported.

Permission to use the hi-res Strava Heatmap in JOSM has been granted by Strava,
see https://wiki.openstreetmap.org/wiki/Strava
and https://wiki.openstreetmap.org/wiki/Permissions/Strava


## Requirements
`stravaheatmap` relies on Python 3, which comes pre-installed on
most *x systems.  For macOS, a convenient way to install Python 3 is
homebrew; see, e.g.,
https://docs.python-guide.org/starting/install3/osx/. For Windows, see
https://www.python.org/downloads/windows/.

A Strava account is required. Facebook/Google/Apple login to Strava is not
supported. You can setup a Strava account heading to https://www.strava.com/register.

## JOSM

### Additional requirements
The utility for JOSM runs on macOS, linux, and Windows operating systems.

### Usage
To install the Strava Heatmap in JOSM, perform the following steps:

1. In JOSM preferences, activate the Strava imagery entries that you need.
You can choose among *all activities* (`all`),
*ride* (`ride`), *run* (`run`), and *winter activities* (`winter`).
2. Change each default imagery URL string from e.g.:
```
tms[3,11]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles/run/hot/{zoom}/{x}/{y}.png
```
to:
```
tms[3,15]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles-auth/run/hot/{zoom}/{x}/{y}.png
```
3. Close JOSM.
4. From the command line, run `python3 -m stravaheatmap.josm`.
5. Provide the email/password of your Strava account.
6. Open JOSM. The imagery URL now should be something like:
```
tms[3,15]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles-auth/run/hot/{zoom}/{x}/{y}.png?Key-Pair-Id=<YOUR_KEY_PAIR_ID_COOKIE_VALUE>&Policy=<YOUR_POLICY_COOKIE_VALUE>&Signature=<YOUR_SIGNATURE_COOKIE_VALUE>
```
When JOSM can no longer display the hi-res heatmap, it means authentication
cookies have expired. You need to repeat the procedure from step 3.

## Cartograph Maps

### Usage
You can add online maps to Cartograph Maps through an
[online map definition file](https://www.cartograph.eu/help_onlinemapimport).
An online map definition file is a JSON file that can be imported directly
in Cartograph Maps.

The `stravaheatmap.cartograph` utility generates an online map
definition (omapdef) file containing the
[TMS](https://en.wikipedia.org/wiki/Tile_Map_Service) URLs
of the Strava Heatmap of the four available activities
(`all`, `ride`, `run`, and `winter`).

1. From the command line, run `python3 -m stravaheatmap.cartograph`
2. Provide the email/password of your Strava account
3. Choose whether you want to save the omapdef file saved in the current
directory or in iCloud (only relevant for macOS users--if you choose iCloud
the file will be saved in
`<HOME>/Library/Mobile Documents/com~apple~CloudDocs/Cartograph Pro`,
for an easy import into Cartograph Maps from mobile devices).
4. Import the map definition file into Cartograph Maps. The following maps
will be available in the *Manage Maps* menu:
   - Strava Heatmap (all)
   - Strava Heatmap (ride)
   - Strava Heatmap (run)
   - Strava Heatmap (winter)

When Cartograph Maps can no longer display the hi-res heatmap, it means
Strava authentication cookies have expired. From the *Manage Maps* menu, remove
any previous Strava Heatmap previously installed in Cartograph Maps, and
repeat the process from step 1.

## Licence
`stravaheatmap` is distributed under the GPL v3.0 licence.
