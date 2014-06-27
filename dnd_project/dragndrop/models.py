from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from urlparse import urlparse
import pickle

MAX_HISTORY_LENGTH = 30
MAX_POPULAR_LENGTH = 30
MAX_RECENTLY_ADDED_LENGTH = 30

class Folder(models.Model):
    name = models.CharField(max_length=128, null=False)
    slug = models.SlugField()
    times_used = models.IntegerField(default=0)
    user = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Folder, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name

class Bookmark(models.Model):
    title = models.CharField(max_length=128, null=True, unique=False)
    summary = models.CharField(max_length=1024, null=True, unique=False)
    url = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    folder = models.ForeignKey(Folder)

    def bdomain(self):
        """
        Given a URL (e.g. http://www.bing.com/images), this function returns the domain
        (e.g. bing.com). It's could probably be improved but hopefully works reasonably well.
        """
        domain = urlparse(self.url).netloc
        domain_parts = domain.split('.')
        if domain_parts[0] == "www":
            return '.'.join(domain_parts[1:])
        else:
            return domain

    def __unicode__(self):
        return self.url

class Profile(models.Model):
    histories = models.TextField(null=True)
    popular = models.TextField(null=True)
    recently_added = models.TextField(null=True)
    user = models.ForeignKey(User)

    def get_history(self):
        return pickle.loads(self.histories)

    def get_popular(self):
        return pickle.loads(self.popular)

    def get_recently_added(self):
        return pickle.loads(self.recently_added)

    def __add_to_dictionary(self,field_inst,result,field_length):
        """
        result: is a dictionary containing the title, url, ...

        this function adds as result to history;
        to do this it's gonna save this back to data base
        """

        # 1. get history and unpickle it

        if self.__dict__[field_inst] is None:
            field_val = ""
            hl = []
        else:
            field_val = self.__dict__[field_inst]
            hl = pickle.loads(field_val)

        if len(hl) == field_length:
            hl.pop()

        hl.insert(0,result)
        self.__dict__[field_inst] = pickle.dumps(hl)

    def add_to_recently_added(self, result):
        self.__add_to_dictionary('recently_added', result, MAX_RECENTLY_ADDED_LENGTH)

    def add_to_history(self, result):
        self.__add_to_dictionary('histories', result, MAX_HISTORY_LENGTH)

    def add_to_popular(self, result):
        self.__add_to_dictionary('popular', result, MAX_POPULAR_LENGTH)
