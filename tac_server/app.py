"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import falcon
from falcon_cors import CORS

from tac_server.resources.mpd import Mpds
from tac_server.resources.mpd import Mpd
from tac_server.resources.proxy import Proxy
from tac_server.resources.validation import Validation

CORS_OPTS = CORS(allow_all_origins=True,
                 allow_all_headers=True,
                 allow_methods_list=['GET', 'OPTIONS'])

api = application = falcon.API(middleware=[CORS_OPTS.middleware])

MPD = Mpd()
MPDS = Mpds()

api.add_route('/mpds/', MPDS)
api.add_route('/mpds/{mpd_id}', MPD)
api.add_sink(Proxy().on_get, prefix='/proxy')
api.add_sink(Validation().on_get, prefix='/validation')
