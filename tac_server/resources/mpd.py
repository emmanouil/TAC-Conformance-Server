"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import json

class MPD(object):
    """
    DASH MPD resource.
    """

    def on_get(self, req, resp):
        mpds = {
            'mpds': {
                '1': {
                    'url': 'https://dash.akamaized.net/dash264/TestCases/1a/sony/SNE_DASH_SD_CASE1A_REVISED.mpd'
                }
            }
        }

        resp.body = json.dumps(mpds, ensure_ascii=False)
