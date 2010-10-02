from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^twilioapp/', include('twilioproj.twilioapp.urls')),

    (r'^admin/', include(admin.site.urls)),

    #Remove this for prod
    (r'^static_media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_DOC_ROOT,
        }),
)
