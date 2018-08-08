"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import json

import requests

import jwt

import falcon

from tac_server.logger import init_logging
from tac_server.tac import TAC_QUERY_STRING

LOGGER = init_logging()

class Validation(object):
    """
    Handles /validation/{url}.
    """

    def on_get(self, req, resp):
        """
        GET /validation/{url}
        """
        # Step 1 - Verify the presence of the query string dash-if-ietf-token
        tac_query_found = False
        encoded_token = ""
        decoded_token = ""
        for query_string in req.query_string.split('&'):
            key, value = query_string.split('=')
            if key == TAC_QUERY_STRING:
                if tac_query_found:
                    LOGGER.warning('A second TAC query string found:'
                                   ' key={}, value={}'.format(key, value))
                    LOGGER.warning('This seconf TAC query string will '
                                   'be discarded in the validation process.')
                else:
                    LOGGER.info('OK|A TAC query string found:'
                                ' key={}, value={}'.format(key, value))
                    encoded_token = value
                    tac_query_found = True

        if not tac_query_found:
            LOGGER.error('KO|No TAC query string was found.')
            resp.body = json.dumps({
                'success': False,
                'message': 'No TAC query string ({}) '
                           'found in request.'.format(TAC_QUERY_STRING)
            })
            resp.status = falcon.HTTP_400
            return

        # Step 2 - Verify the format of the token
        try:
            decoded_token = jwt.decode(encoded_token, verify=False)
        except jwt.exceptions.InvalidTokenError as error:
            LOGGER.error(error)
            LOGGER.error('KO|String in TAC query string is not a JWT.')
            resp.body = json.dumps({
                'success': False,
                'message': 'String in TAC query string is not a JWT.'
            })
            resp.status = falcon.HTTP_400
            return


        LOGGER.info('Access Token decoded: {}'.format(decoded_token))

        # Step 3 - Verify that the Access Token contains the cdnistt claim
        # and that the value is "2"
        if 'cdnistt' in decoded_token:
            if decoded_token['cdnistt'] == 2:
                LOGGER.info('OK|The cdnistt claim value is 2')
            else:
                LOGGER.error('KO|The cdnistt claim value is not 2 '
                             'but {}.'.format(decoded_token['cdnistt']))
                resp.body = json.dumps({
                    'success': False,
                    'message': 'Access Token does not have a CDNI Signed '
                               'Token Transport (cdnistt) claim'
                })
                resp.status = falcon.HTTP_400
                return
        else:
            LOGGER.error('KO|Access Token does not have a CDNI Signed '
                         'Token Transport (cdnistt) claim.')
            resp.body = json.dumps({
                'success': False,
                'message': 'Access Token does not have a CDNI Signed '
                           'Token Transport (cdnistt) claim'
            })
            resp.status = falcon.HTTP_400
            return


        response = requests.get('https://{}'.format(
            req.path.replace('/validation/', '')))
        resp.content_type = response.headers['Content-Type']
        resp.body = response.content
