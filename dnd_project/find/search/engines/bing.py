import json
import string
import requests
from find.search.engine import Engine
from find.search.response import Response
from find.search.exceptions import EngineAPIKeyException, QueryParamException, EngineConnectionException

API_ENDPOINT = 'https://api.datamarket.azure.com/Bing/Search/v1/Composite'
WEB_ONLY_API_ENDPOINT = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/'
RESULT_TYPES = ('web', 'image', 'video')
DEFAULT_RESULT_TYPE = 'web'

# bing's limits
MAX_PAGE_SIZE = 50
MAX_RESULTS = 1000


class Bing(Engine):
    """
    Bing search engine.

    """

    def __init__(self, api_key='', **kwargs):
        """
        Bing engine constructor.

        Kwargs:
            api_key (str): string representation of api key needed to access bing search api
            See Engine.

        Raises:
            EngineException

        Usage:
            engine = EngineFactory('bing', api_key='etc123456etc123456etc123456')

        """
        Engine.__init__(self, **kwargs)
        self.api_key = api_key

        if not self.api_key:
            raise EngineAPIKeyException(self.name, "'api_key=' keyword argument not specified")

            # TODO pull api key from keys.py

    def _search(self, query):
        """
        Concrete method of Engine's interface method 'search'.
        Performs a search and retrieves the results as an ifind Response.

        Args:
            query (ifind Query): Object encapsulating details of a search query.

        Query Kwargs:
            top (int): specifies the mamximum amount of results to return up to MAX_PAGE_SIZE.
            skip (int): specifies the offset/starting point of results returned.
            result_type (str): specifies the type of results to return (see top of class for available types).

        Returns:
            ifind Response: object encapulsating a search request's results.

        Raises:
            EngineException

        Usage:
            Private method.

        """
        if not query.top:
            raise QueryParamException(self.name, "Total result amount (query.top) not specified")

        if query.top > MAX_RESULTS:
            raise QueryParamException(self.name, 'Requested result amount (query.top) '
                                                 'exceeds max of {0}'.format(MAX_PAGE_SIZE))

        if query.top <= MAX_PAGE_SIZE:
            return self._request(query)

        if query.top > MAX_PAGE_SIZE:
            return self._auto_request(query)

    def _request(self, query):
        """
        Issues a single request to the API_ENDPOINT and returns the result as
        an ifind Response.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            ifind Response: object encapsulating a search request's results.

        Raises:
            EngineException

        Usage:
            Private method.

        """
        query_string = self._create_query_string(query)

        try:
            response = requests.get(query_string, auth=('', self.api_key))
        except requests.exceptions.ConnectionError:
            raise EngineConnectionException(self.name, "Unable to send request, check connectivity")

        if response.status_code != 200:
            raise EngineConnectionException(self.name, "", code=response.status_code)

        return Bing._parse_json_response(query, response)

    def _auto_request(self, query):
        """
        Issues a multiple requests to the API_ENDPOINT to meet query.top
        requirements and returns the result as an ifind Response.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            ifind Response: object encapsulating a search request's results.

        Usage:
            Private method.

        """
        target = query.top
        query.top = MAX_PAGE_SIZE
        query.skip = 0
        response = self._request(query)

        while response.result_total < target:

            remaining = target - response.result_total

            if remaining > MAX_PAGE_SIZE:
                query.skip += MAX_PAGE_SIZE
                query.top = MAX_PAGE_SIZE
                response += self._request(query)

            if remaining <= MAX_PAGE_SIZE:
                query.skip += query.top
                query.top = remaining
                response += self._request(query)

        return response

    def _create_query_string(self, query):
        """
        Creates and returns Bing API query string with encoded query parameters.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            str: query string for Bing API request

        Raises:
            EngineException

        Usage:
            Private method.

        """
        result_type = query.result_type

        if not result_type:
            result_type = DEFAULT_RESULT_TYPE

        if result_type not in RESULT_TYPES:
            raise QueryParamException(self.name, "Engine doesn't support query result type '{0}'"
                                                 .format(query.result_type))
        params = {'$format': 'JSON',
                  '$top': query.top,
                  '$skip': query.skip}

        result_string = '?Sources="{}"'.format(result_type)

        query_string = 'Query="{}"'.format(str(query.terms))

        for key, value in params.iteritems():
            query_string += '&' + key + '=' + str(value)

        return API_ENDPOINT + Bing._encode_symbols(result_string + '&' + query_string)

    @staticmethod
    def _encode_symbols(query_string):
        """
        Encodes certain symbols of a query string to match Bing's API specification.

    spell    Args:
            query_string (str): query string for Bing API request.

        Returns:
            str: encoded query string for Bing API request.

        Usage:
            Private method.

        """
        encoded_string = string.replace(query_string, "'", '%27')
        encoded_string = string.replace(encoded_string, '"', '%27')
        encoded_string = string.replace(encoded_string, '+', '%2b')
        encoded_string = string.replace(encoded_string, ' ', '%20')
        encoded_string = string.replace(encoded_string, ':', '%3a')

        return encoded_string

    @staticmethod
    def _parse_json_response(query, results):
        """
        Parses Bing's JSON response and returns as an ifind Response.

        Args:
            query (ifind Query): object encapsulating details of a search query.
            results : requests library response object containing search results.

        Returns:
            ifind Response: object encapsulating a search request's results.

        Usage:
            Private method.

        """
        response = Response(query.terms)

        content = json.loads(results.text)

        if query.result_type == 'web' or not query.result_type:
            for result in content[u'd'][u'results'][0][u'Web']:
                response.add_result(title=result[u'Title'], url=result[u'Url'], summary=result[u'Description'])

        if query.result_type == 'image':
            for result in content[u'd'][u'results'][0][u'Image']:
                file_size = str(int(result[u'FileSize']) / 1024)  # in kilobytes
                width = result[u'Width']
                height = result[u'Height']
                media_url = result[u'MediaUrl']
                thumb_url = result[u'Thumbnail'][u'MediaUrl']
                response.add_result(file_size=file_size, width=width, height=height,
                                    media_url=media_url, thumb_url=thumb_url)

        if query.result_type == 'video':
            for result in content[u'd'][u'results'][0][u'Video']:
                run_time = Bing._get_video_length(int(result[u'RunTime']))
                title = result[u'Title']
                media_url = result[u'MediaUrl']
                thumb_url = result.get(u'Thumbnail', {}).get(u'MediaUrl', None)
                if thumb_url is None:
                    continue
                response.add_result(title=title, media_url=media_url, run_time=run_time, thumb_url=thumb_url)

        return response

    @staticmethod
    def _get_video_length(run_time):
        """
        Converts video length (in milliseconds) to human readable string.

        Args:
            run_time (int): length of video in milliseconds

        Returns:
            str: human readable representation of video's length

        Usage:
            Private method.

        """
        if not run_time:
            return ''

        # get minutes
        minutes = run_time / 1000 / 60
        min_string = '{} mins'.format(minutes)

        # get seconds
        seconds = run_time / 1000 % 60
        sec_string = '{} seconds'.format(seconds)

        if minutes and seconds:
            return min_string + ' ' + sec_string

        if minutes and not seconds:
            return min_string

        if seconds and not minutes:
            return sec_string