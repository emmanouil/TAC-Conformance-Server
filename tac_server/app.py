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
from tac_server.resources.simulation import Simulation

CORS_OPTS = CORS(allow_all_origins=True,
                 allow_all_headers=True,
                 allow_methods_list=['GET', 'OPTIONS'])

API = falcon.API(middleware=[CORS_OPTS.middleware])

MPD = Mpd()
MPDS = Mpds()

API.add_route('/mpd/', MPDS)
API.add_route('/mpd/{mpd_id:int}', MPD)
API.add_sink(Proxy().on_get, prefix='/proxy')
API.add_sink(Validation().on_get, prefix='/validation')
API.add_sink(Simulation().on_get, prefix='/simulation')
