from registration.backends.simple.views import RegistrationView as BaseRegistrationView
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

class RegistrationView(BaseRegistrationView):
    """
    Class inheriting from the django-registration simple RegistrationView.
    This is required to redirect users to the correct URL after signing up...unfortunately.
    """
    def get_success_url(self, request, user):
        return "/"  # When successfully registered, redirect the new user to root.

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', RegistrationView.as_view()),
    url(r'^accounts/$', include('registration.backends.simple.urls')),  # One-step django-registration backend.
    url(r'^', include('dragndrop.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns( 'django.views.static', (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}), )
