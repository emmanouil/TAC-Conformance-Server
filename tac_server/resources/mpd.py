"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import json

import requests

MPDS = {
    'mpds': {
        '1': {
            'name': 'SegmentBase, ondemand profile',
            'url': 'https://dash.akamaized.net/dash264/TestCases/1a/sony/SNE_DASH_SD_CASE1A_REVISED.mpd'
        }
    }
}

class Mpds(object):
    """
    Hanldes /mpds.
    """

    def on_get(self, req, resp):
        resp.body = json.dumps(MPDS, ensure_ascii=False)

class Mpd(object):
    """
    Handles /mpds/{mpd_id}
    """

    def on_get(self, req, resp, mpd_id):
        r = requests.get(MPDS['mpds'][mpd_id]['url'])
        resp.content_type = 'application/dash+xml'
        resp.body = r.text
