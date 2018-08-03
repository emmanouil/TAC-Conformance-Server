"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import falcon
from falcon_cors import CORS

from .resources.mpd import Mpds
from .resources.mpd import Mpd
from .resources.proxy import Proxy

CORS_OPTS = CORS(allow_all_origins=True,
                 allow_all_headers=True,
                 allow_methods_list=['GET', 'OPTIONS'])

api = application = falcon.API(middleware=[CORS_OPTS.middleware])

MPD = Mpd()
MPDS = Mpds()

api.add_route('/mpds/', MPDS)
api.add_route('/mpds/{mpd_id}', MPD)
api.add_sink(Proxy().on_get, prefix='/proxy')
