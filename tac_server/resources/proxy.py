"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import requests

class Proxy(object):
    """
    Handles /proxy/{url}.
    """

    def on_get(self, req, resp):
        """
        GET /proxy/{url}
        """
        response = requests.get('https://{}'.format(
            req.path.replace('/proxy/', '')))
        resp.content_type = response.headers['Content-Type']
        resp.body = response.content
