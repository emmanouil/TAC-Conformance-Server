"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import json

import requests

from xml.dom import minidom

from mpegdash.parser import MPEGDASHParser
from mpegdash.nodes import BaseURL
from mpegdash.utils import write_child_node

MPDS = {
    'mpds': {
        '1': {
            'name': 'SegmentBase, ondemand profile',
            'url': 'https://dash.akamaized.net/dash264/TestCases/1a/sony/SNE_DASH_SD_CASE1A_REVISED.mpd',
            'base_url': '/dash.akamaized.net/dash264/TestCases/1a/sony/'
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
        mpd_response = requests.get(MPDS['mpds'][mpd_id]['url'])
        resp.content_type = 'application/dash+xml'
        mpd = MPEGDASHParser.parse(mpd_response.text)
        mpd.base_urls = []
        base_url = BaseURL()
        base_url.base_url_value = "/proxy{}".format(
            MPDS['mpds'][mpd_id]['base_url'])
        mpd.base_urls.append(base_url)
        xml_doc = minidom.Document()
        write_child_node(xml_doc, 'MPD', mpd)
        resp.body = xml_doc.toprettyxml(indent='    ', newl='\n')
