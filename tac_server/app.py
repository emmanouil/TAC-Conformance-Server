"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import falcon
from falcon_cors import CORS

from .resources.mpd import Mpds
from .resources.mpd import Mpd

cors = CORS(allow_all_origins=True)
api = application = falcon.API(middleware=[cors.middleware])

MPD = Mpd()
MPDS = Mpds()

api.add_route('/mpds/', MPDS)
api.add_route('/mpds/{mpd_id}', MPD)
