"""
HAVE NOT TESTED FOR SPEED (but second one seems better)

Decent link here about ip spoofing -
http://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html

I think it has already been incorporated and my code works on his committed change.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from json import loads
from urllib2 import urlopen
from flask import request
from flask.ext.login import current_user
from config_vars import GEO_URL, VALID_IP


# ========================
# HELPER FUNCTIONS
# ========================
def _key_modifier(data):
    """Change geo labels"""
    for k in data.keys(): data[k.replace('geoplugin_', '')] = data.pop(k)
    data['zip_code'] = data.pop('areaCode')
    return data


def _gen_shortdata(data):
    """Truncate the data provided"""
    if data:
        short_data = {k: data[k] for k in ['city', 'zip_code',
                                           'latitude', 'longitude']}
    else:
        short_data = {'city': 'CITY', 'zip_code': 'ZIP',
                      'latitude': '13', 'longitude': '14'}
    return short_data


def get_clientdata():
    # DO NOT UNDERSTAND DISTINCTIONS
    # ip = request.access_route[0] or request.remote_addr
    # ip = request.headers.getlist('X-Forwarded-For', request.remote_addr)
    # ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    client_data = {}
    ip = request.environ.get('REMOTE_ADDR', request.remote_addr)
    if not VALID_IP.match(ip):
        raise ValueError('Invalid IPv4 format')
    client_data['ip_address'] = ip
    client_data['browser'] = request.headers.get("User-Agent")
    if current_user.is_active:
         client_data['member_id'] = current_user.get_id()
    return client_data


def get_geodata(switched_on=False, keymod_fn=None, geo_url=GEO_URL):
    """
    Search for geolocation information;
    Generally switched off (for speed).
    NOTE: because of proxies etc. this isn't ultimately used;
    We use locn_script as client-driven source of the data.
    More accurate.
    """
    data = get_clientdata()
    if switched_on:
        url = geo_url.format(data['ip_address'])
        try:
            response = urlopen(url).read()
            geog = loads(response)
            if keymod_fn:
                geog = keymod_fn(geog)

            data.update(_gen_shortdata(geog))
        except Exception:
            pass
    return data


if __name__ == '__main__':
    #get_geodata('91.85.158.49')
    #ip = request.environ.get('REMOTE_ADDR', request.remote_addr)
    cc = get_geodata(True, _key_modifier)

