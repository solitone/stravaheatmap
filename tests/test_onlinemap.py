import builtins
import sys
from types import SimpleNamespace
from urllib.parse import parse_qs, urlsplit

import pytest
from stravaheatmap.cartograph.onlinemap import OnlineMap

COOKIES = {'Key-Pair-Id':'key','Policy':'policy','Signature':'signature'}

@pytest.mark.parametrize('color', OnlineMap.COLORS)
def test_cached_generation_has_no_authentication_or_network(color, monkeypatch):
    original = builtins.__import__
    def guarded(name, *args, **kwargs):
        if name.startswith(('stravacookies', 'playwright')):
            pytest.fail('Pure generator imported browser/authentication code')
        return original(name, *args, **kwargs)
    monkeypatch.setattr(builtins, '__import__', guarded)
    doc = OnlineMap.getDefinitionFromCookies(color, COOKIES, maxZoom=15)
    assert doc['version'] == 2
    assert len(doc['maps']) == 4
    for m, activity in zip(doc['maps'], OnlineMap.ACTIVITIES):
        assert m['name'] == OnlineMap.MAPNAMES[activity]
        assert '/'+activity+'/'+OnlineMap.COLORS[color]+'/' in m['url']
        assert '{z}/{x}/{y}.png?' in m['url']
        assert m['maxZoom'] == 15
        assert parse_qs(urlsplit(m['url']).query) == {k:[v] for k,v in COOKIES.items()}

@pytest.mark.parametrize('values', [{}, {**COOKIES,'Signature':''}, {**COOKIES,'Policy':None}])
def test_missing_cookie_rejected(values):
    with pytest.raises(ValueError):OnlineMap.getDefinitionFromCookies('hot', values)

@pytest.mark.parametrize('zoom', [True, 1, 23, '15'])
def test_bad_zoom_rejected(zoom):
    with pytest.raises(ValueError):OnlineMap.getDefinitionFromCookies('hot', COOKIES, maxZoom=zoom)

def test_bad_color_rejected():
    with pytest.raises(ValueError):OnlineMap.getDefinitionFromCookies('invalid', COOKIES)

def test_values_are_escaped_and_unrelated_session_cookies_omitted():
    params={**COOKIES, 'Signature':'a&b=+/?', '_strava4_session':'private'}
    m=OnlineMap.getDefinitionFromCookies('hot', params)['maps'][0]
    query=parse_qs(urlsplit(m['url']).query)
    assert query['Signature']==['a&b=+/?']
    assert '_strava4_session' not in query

def test_legacy_api_still_logs_in_once_and_preserves_output(monkeypatch):
    calls=[]
    class Fetcher:
        def fetchCookies(self,email,password):calls.append((email,password))
        def getCookieString(self):return 'Key-Pair-Id=key&Policy=policy&Signature=signature'
    monkeypatch.setitem(sys.modules,'stravacookies',SimpleNamespace(StravaCookieFetcher=Fetcher))
    old=OnlineMap.getDefinition('hot','test@example.invalid','dummy')
    assert calls==[('test@example.invalid','dummy')]
    assert old==OnlineMap.getDefinitionFromCookies('hot',COOKIES)
    assert all(m['maxZoom']==22 for m in old['maps'])
