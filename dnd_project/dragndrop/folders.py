__author__ = 'leif'

from models import Folder, Bookmark
from django.contrib.auth.models import User

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


def suggest_folder(user, query):
    pass

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


def get_folder_results(folder_id):
    """ returns a list of Bookmarks
    """
    f = get_folder(folder_id)
    if f:
        b = Bookmark.objects.filter(folder=f)
    else:
        return None


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
        b = Bookmark.objects.get_or_create(folder=f,title=result.title, url=result.url, summary=result.summary)
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







