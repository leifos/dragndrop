from django.contrib import admin
from dragndrop.models import Folder, Bookmark, Profile
from django.contrib.auth.models import User

admin.site.register(Folder)
admin.site.register(Bookmark)
admin.site.register(Profile)
