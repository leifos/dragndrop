__author__ = 'leif'
from ifind.search.engine import Engine
from ifind.search.response import Response


class Dummy(Engine):
    """
    This search engine makes no internet requests
    It serves up pre-programmed responses for testing
    For all queries, it returns the same response which is:
        a list of results with title: x, url: www.x.com, description: x x x
        where x is in ['one','two','three',...,'ten']
    """

    def __init__(self, **kwargs):
        Engine.__init__(self, **kwargs)


    def _create_response(self, query):
        response = Response(query.terms)

        matches = ['one','two','three','four','five','six','seven','eight','nine','ten']
        result_list = ['rand','rand','rand','rand','rand','rand','rand','rand','rand','rand']
        matched = False

        if query.terms in matches:
            matched = True

        if matched:
            result_list = matches

        rank = 1
        for x in result_list:
            response.add_result(title=x, url='www.'+x+'.com', summary= x +' '+' ' + x, rank=234)
            rank = rank + 1
            print rank

        return response

    def search(self, query):
        """Dummy search, returns the same set of results, regardless of query

        Parameters:

        * query (ifind.search.query.Query)

        Returns:

            * ifind.search.response.Response

        Raises:

            * urllib2.URLError
            * API key error

        """
        response = self._create_response(query)

        return response
