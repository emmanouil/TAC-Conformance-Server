"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import json

import falcon
import requests
from xml.dom import minidom
from mpegdash.parser import MPEGDASHParser
from mpegdash.nodes import BaseURL
from mpegdash.nodes import Descriptor
from mpegdash.nodes import XMLNode
from mpegdash.utils import write_child_node
from mpegdash.utils import parse_child_nodes
from mpegdash.utils import parse_attr_value
from mpegdash.utils import write_attr_value

from tac_server.logger import init_logging

LOGGER = init_logging()

MPDS = {
    'mpds': {
        '1': {
            'name': 'SegmentBase, ondemand profile',
            'url': 'https://dash.akamaized.net/dash264/TestCases/1a/sony/SNE_DASH_SD_CASE1A_REVISED.mpd',
            'base_url': '/dash.akamaized.net/dash264/TestCases/1a/sony/'
        }
    }
}

class DescriptorWithExtUrlQuery(Descriptor):
    """
    Descriptor with child nodes
    """
    def __init__(self):
        self.ext_url_query_info = None #
        self.xmlns = 'urn:mpeg:dash:schema:urlparam:2016'
        self.prefix = 'up'
        self.scheme_id_uri = 'urn:mpeg:dash:urlparam:2016:querystring'
        self.id = None # pylint: disable=invalid-name
        self.value = None

    def parse(self, xmlnode):
        """Parsing"""
        self.xmlns = parse_attr_value(xmlnode,
                                      'xmlns:{}'.format(self.prefix),
                                      str)
        self.ext_url_query_info = parse_child_nodes(
            xmlnode,
            '{}:ExtUrlQueryInfo'.format(self.prefix),
            ExtUrlQueryInfo)

    def write(self, xmlnode): # pylint: disable=super-on-old-class
        """Writing"""
        super(DescriptorWithExtUrlQuery, self).write(xmlnode)
        write_attr_value(xmlnode, 'xmlns:{}'.format(self.prefix), self.xmlns)
        write_child_node(xmlnode,
                         '{}:ExtUrlQueryInfo'.format(self.prefix),
                         self.ext_url_query_info)

class ExtUrlQueryInfo(XMLNode):
    """
    ExtUrlQueryInfo
    """
    def __init__(self):
        self.include_in_requests = None #
        self.query_string = None        #
        self.query_template = None      #
    def parse(self, xmlnode):
        """Parsing"""
        self.include_in_requests = parse_attr_value(xmlnode,
                                                    'includeInRequests',
                                                    str)
        self.query_string = parse_attr_value(xmlnode, 'queryString', str)
        self.query_template = parse_attr_value(xmlnode, 'queryTemplate', str)

    def write(self, xmlnode):
        """Writing"""
        write_attr_value(xmlnode, 'includeInRequests', self.include_in_requests)
        write_attr_value(xmlnode, 'queryString', self.query_string)
        write_attr_value(xmlnode, 'queryTemplate', self.query_template)

class Mpds(object):
    """
    Hanldes /mpds.
    """

    def on_get(self, req, resp):
        """
        GET /mpds
        """
        resp.body = json.dumps(MPDS, ensure_ascii=False)

class Mpd(object):
    """
    Handles /mpds/{mpd_id}
    """

    def on_get(self, req, resp, mpd_id):
        """
        GET /mpds/{mpd_id}
        """
        mode = ''
        for key, value in req.params.items():
            if key == 'mode':
                mode = value

        base_url = BaseURL()
        if mode == 'proxy':
            base_url.base_url_value = "/proxy{}".format(
                MPDS['mpds'][str(mpd_id)]['base_url'])
        elif mode == 'simulation':
            base_url.base_url_value = "/simulation{}".format(
                MPDS['mpds'][str(mpd_id)]['base_url'])
        elif mode == 'validation':
            base_url.base_url_value = "/validation{}".format(
                MPDS['mpds'][str(mpd_id)]['base_url'])
        else:
            LOGGER.error('No mode provided as query string.')
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({
                'message': 'Please provide a mode in the request '
                           'as query string: mode=proxy|simulation|validation.'
            })
            return

        mpd_response = requests.get(MPDS['mpds'][str(mpd_id)]['url'])
        resp.content_type = 'application/dash+xml'
        mpd = MPEGDASHParser.parse(mpd_response.text)
        mpd.base_urls = []

        # Add the custome base urls
        mpd.base_urls.append(base_url)

        # Add TAC signalling
        if mode != 'proxy':
            tac = DescriptorWithExtUrlQuery()
            tac.scheme_id_uri = 'urn:mpeg:dash:urlparam:2016:querystring'
            url_query_info = ExtUrlQueryInfo()
            url_query_info.include_in_requests = 'mpd segment'
            url_query_info.query_string = 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJEQVNILUlGIENvbmZvcm1hbmNlIiwiY2RuaXN0dCI6Mn0.QjVVZGUXOsFPiHCTax_I14su5rppK-yWPQXrkcI1gQI'
            url_query_info.query_template = 'dash-if-ietf-token=$query:token$'
            tac.ext_url_query_info = url_query_info
            for period in mpd.periods:
                for adaptation_set in period.adaptation_sets:
                    if not adaptation_set.essential_properties:
                        adaptation_set.essential_properties = []
                    adaptation_set.essential_properties.append(tac)

        # Serialize MPD to XML
        xml_doc = minidom.Document()
        write_child_node(xml_doc, 'MPD', mpd)
        resp.body = xml_doc.toprettyxml(indent='    ', newl='\n')
