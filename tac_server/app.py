"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import falcon

from .resources.mpd import MPD


api = application = falcon.API()

mpds = MPD()
api.add_route('/mpds', mpds)
