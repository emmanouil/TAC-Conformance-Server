"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import requests

class Simulation(object):
    """
    Handles /simulation/{url}.
    """

    def on_get(self, req, resp):
        """
        GET /simulation/{url}
        """
        response = requests.get('https://{}'.format(
            req.path.replace('/simulation/', '')))
        resp.content_type = response.headers['Content-Type']
        resp.set_header('DASH-IF-IETF-Token', 'eyJhbGciOiJIUzI1NiIsInR5c'
                        'CI6IkpXVCJ9.eyJpc3MiOiJEQVNILUlGIENvbmZvcm1hbmNl'
                        'IiwiY2RuaXN0dCI6Mn0.QjVVZGUXOsFPiHCTax_I14su5rpp'
                        'K-yWPQXrkcI1gQI')
        resp.body = response.content
