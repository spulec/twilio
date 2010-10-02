from django.conf.urls.defaults import *

urlpatterns = patterns('twilioproj.twilioapp.views',

        # Phone numbers
        (r'^$', 'index_number'),
        (r'^create/$', 'create_number'),
        #(r'^(?P<phone_number>\d+)/view/$', 'view_number'),
        (r'^(?P<phone_number>\d+)/edit/$', 'edit_number'),

        (r'^response/$', 'index_response'),
        (r'^response/create/$', 'create_response'),
        (r'^response/(?P<response_name>\w+)/view/$', 'view_response'),
        (r'^response/(?P<response_name>\w+)/edit/$', 'edit_response'),

)

