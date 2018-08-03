"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import falcon

from .resources.mpd import Mpds
from .resources.mpd import Mpd


api = application = falcon.API()

MPD = Mpd()
MPDS = Mpds()

api.add_route('/mpds/', MPDS)
api.add_route('/mpds/{mpd_id}', MPD)
