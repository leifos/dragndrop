import time
import datetime
import importlib

from find.search.query import Query
from find.search.engines import ENGINE_LIST
from find.search.exceptions import EngineLoadException
from find.search.exceptions import InvalidQueryException


class Engine(object):
    """
    Abstract class representing an find search engine.

    """
    def __init__(self, throttle=0, proxies=None):
        """
        Engine constructor.

        Kwargs:
            throttle(int): limits search method to once per 'throttle' arg in seconds (blocking)
            proxies (dict): mapping of proxies to use i.e. {"http":"10.10.1.10:3128", "https":"10.10.1.10:1080"}.

        Attributes:
            last_search (str): datetime of last search

        Raises:

        Usage:
            See EngineFactory.

        """
        # name of engine
        self.name = self.__class__.__name__

        # throttle value
        self.throttle = throttle

        # load proxies
        self.proxies = proxies  # TODO engine proxies

        # datetime of last query
        self.last_search = None
        self.num_requests = 0
        self.num_requests_cached = 0

    def search(self, query):
        """
        Public search method for an Engine instance, returning the results of a query argument.
        Caching handled here, true search implementation deferred to subclass '_search' method.

        Args:
            query (ifind Query): object encapsulating details of search query.

        Returns:
            ifind Response: object encapsulating a search request's results.

        Raises:

        Usage:
            query = Query('hello world')
            engine = EngineFactory('wikipedia')
            response = engine.search(query)

        """
        # raise exception if search argument isn't an ifind Query object
        if not isinstance(query, Query):
            raise InvalidQueryException('Engine', 'Expected type {}'
                                        .format("<class 'find.search.query.Query'>"))

        self.num_requests +=1
        # check query in cache and return if there

        if self.throttle and self.last_search:
            then = datetime.datetime.strptime(self.last_search, '%a %b %d %H:%M:%S %Y')
            now = datetime.datetime.now()
            diff = (now - then).seconds
            if diff < self.throttle:
                #print "waiting {} seconds".format(self.throttle - diff)
                time.sleep(self.throttle - diff)

        # search and store response

        response = self._search(query)

        self.last_search = time.asctime()

        return response

    def _search(self, query):
        """
        Abstract search method for an Engine instance, to be implemented by subclasses.
        Performs a search and retrieves the results as an ifind Response.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            ifind Response: object encapsulating a search request's results.

        Raises:
            See subclasses.

        Usage:
            Private method.

        """
        pass


class EngineFactory(object):
    """
    Public class representing an ifind search engine factory.

    Instantiates and returns an Engine subclass, keyed by
    the 'engine' argument, or None otherwise.

    Args:
        engine (str): Name of Engine subclass to instantiate.

    Kwargs:
        throttle (int): limits searching to once per 'throttle' in seconds (blocking)

    Returns:
        ifind Engine object: Dynamically dispatched instance of Engine subclass.

    Raises:
        EngineLoadException.
        See subclasses.

    Usage:
        engine = EngineFactory('govuk')
        engine_list = EngineFactory().engines()
        engine = EngineFactory('twitter', throttle=50)

        """

    def engines(self):
        """
        Returns list of available engines.

        """
        return ENGINE_LIST

    def __contains__(self, engine):
        """
        Special containment override for 'in' operator.

        Usage:
            print 'bing' in EngineFactory() --> True

        """
        return engine.lower() in ENGINE_LIST

    def __iter__(self):
        """
        Implements iterator for EngineFactory, returning a single engine at a time.

        Usage:
            for engine in EngineFactory():
                print result

        """
        for engine in ENGINE_LIST:
            yield engine

    def __new__(cls, engine="", **kwargs):
        """
        Overrides object construction so as to bypass __init__ so to dynamically
        dispatch 'engine' subclass. See class docstring.

        """
        # if engine in subclass list, return instantiation
        if engine.lower() in ENGINE_LIST:
            module = importlib.import_module('find.search.engines.{}'.format(engine.lower()))
            return getattr(module, engine.lower().title())(**kwargs)

        # if 'engine' defined but not in supported list
        elif engine:
            raise EngineLoadException("EngineFactory", "Engine '{}' not found".format(engine.lower().title()))

        # if 'engine' undefined ("" or None)
        else:
            return super(EngineFactory, cls).__new__(cls)