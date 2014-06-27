__author__ = 'leif'

from models import Folder, Bookmark
import operator
from django.contrib.auth.models import User
import re
from django.db.models import Q


def get_user(username):
    try:
        u = User.objects.get(username=username)
    except:
        u = None
    return u

def create_folder(user, folder_name):
    """
    Args:
        user: django.contrib.auth.models.User
    returns:
        models.Folder
    """
    f = Folder(name=folder_name, user=user, times_used=0)
    f.save()
    return f


def remove_folder(folder_id):
    """ Given the folder_id, remove it and return true,
    returns: None

    """
    f = get_folder(folder_id)
    if f:
        f.delete()
"""
methods
    normalize_query(), get_query()

    adapted from:
    http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap

"""

def __normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def __get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = __normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def suggest_folders(user, query):
    """
    this function searches the bookmarks model's title and description for the given
    query_string
    it returns the top three folders in which the bookmarks contain the query_string

    functions used: get_query
    """

    found_entries = None

    entry_query = __get_query(query, ['title', 'summary',])

    found_entries = Bookmark.objects.filter(entry_query).order_by('-clicks')

    context_dict = {}

    for result in found_entries:
        folder_res = result.folder
        if folder_res.user == user:
            if folder_res in context_dict:
                context_dict[folder_res] += 1
            else:
                context_dict[folder_res] = 1
            folder_res.url = folder_res.name.replace(' ', '_')

    sorted_dict = sorted(context_dict.iteritems(), key=operator.itemgetter(1))[::-1]

    top_three = [i[0] for i in sorted_dict][:3]

    return top_three

def get_folder(folder_id):
    """
    args: folder_id (integer)
    returns Folder object or None
    """
    try:
        f = Folder.objects.get(id=folder_id)
    except:
        f = None
    return f


def get_folder_results(folder_id=-1, folder=None):
    """ returns a list of Bookmarks
    """
    if folder:
        f = folder
    else:
        if folder_id > 0:
            f = get_folder(folder_id)
        else:
            f = None
    if f:
        b = Bookmark.objects.filter(folder=f)
        return b
    else:
        return None


def get_bookmarks_given_folder_slug(user, slug):
    """
    returns the models.Folder object
    """
    try:
        f = Folder.objects.get(user=user, slug=slug)
    except:
        f = None

    bookmarks = get_folder_results(folder=f)
    return bookmarks


def add_result_to_folder(folder_id, result):
    """
    args:
        folder_id (integer)
        result: find.search.response.Result
    returns:
        models.Bookmark
    """
    f = get_folder(folder_id)
    if f:
        b = Bookmark.objects.get_or_create(folder=f,title=result.title, url=result.url, summary=result.summary)[0]
    return b

def get_user_folders(user):
    """
    returns the list of user folders
    """
    folders = Folder.objects.filter(user=user)
    return folders

class Bookmarks(object):

    def __init__(self, max_size=20):
        self.results = []
        self.set_max_size(max_size)

    def set_max_size(self, max_size):
        if max_size > 0:
            self.max_size = max_size

    def add_result(self, result):
        """ add a result to the list, if the list is equal to max_size,
         it will remove one result first
        inputs:
            result: find.response.Result
        out:
            None
        """
        if len(self.results) == self.max_size:
            del self.results[0]
        self.results.append(result)

    def sort_results(self):
        """ sort by the value in rank attribute in Result
        operates on self.results
        """
        pass

    def clear_result(self):
        """
        removes all the results from the result list
        """
        self.results = []







