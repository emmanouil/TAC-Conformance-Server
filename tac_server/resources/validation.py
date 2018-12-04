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

def is_access_token_valid(encoded_token):
    """
    Validate that an Access Token is well-formatted.
    """
    try:
        decoded_token = jwt.decode(encoded_token, verify=False) # Rule TAC1
    except jwt.exceptions.InvalidTokenError as error:
        LOGGER.error(error)
        LOGGER.error('KO|The string is not a JWT.')
        response = json.dumps({
            'success': False,
            'message': 'String is not a JWT.'
        })
        return (False, response)

    LOGGER.info('Access Token decoded: {}'.format(decoded_token))

    # Step 3 - Verify that the Access Token contains the cdnistt claim
    # and that the value is "2"
    if 'cdnistt' in decoded_token:
        if decoded_token['cdnistt'] == 2: # Rule TAC2
            LOGGER.info('OK|The cdnistt claim value is 2')
        else:
            LOGGER.error('KO|The cdnistt claim value found is not 2 '
                         'but {}.'.format(decoded_token['cdnistt']))
            response = json.dumps({
                'success': False,
                'message': 'Access Token does have a CDNI Signed '
                           'Token Transport (cdnistt) claim but with a '
                           'wrong value.'
            })
            return (False, response)
    else:
        LOGGER.error('KO|Access Token does not have a CDNI Signed '
                     'Token Transport (cdnistt) claim.')
        response = json.dumps({
            'success': False,
            'message': 'Access Token does not have a CDNI Signed '
                       'Token Transport (cdnistt) claim'
        })
        return (False, response)

    return (True, '')

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
            if query_string != "":
                key, value = query_string.split('=')
                if key == TAC_QUERY_STRING:
                    if tac_query_found:
                        LOGGER.warning('A second TAC query string found:'
                                       ' key={}, value={}'.format(key, value))
                        LOGGER.warning('This seconf TAC query string will '
                                       'be discarded in the validation '
                                       'process.')
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

        # Step 2 - Verify the format of the token - Rule TAC5
        token_valid, message = is_access_token_valid(encoded_token)
        if not token_valid:
            resp.body = message
            resp.status = falcon.HTTP_400
            return

        response = requests.get('https://{}'.format(
            req.path.replace('/validation/', '')))
        if 'DASH-IF-IETF-Token' in response.headers:
            LOGGER.debug('The TAC HTTP header has been found in the '
                         'response from the server')
            token_valid, message = is_access_token_valid(encoded_token) # Rule TAC4
            if not token_valid:
                resp.body = message
                resp.status = falcon.HTTP_400
                return
        else:
            LOGGER.debug('The TAC HTTP header has not been found in the '
                         'response from the server')

        resp.content_type = response.headers['Content-Type']
        resp.body = response.content
