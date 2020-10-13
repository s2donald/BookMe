from django.conf import settings
from django_hosts import patterns, host

settings.PARENT_HOST = 'gibele.com:8000'
host_patterns = patterns('',
    # host(r'www', 'gibele.urls',name='ww'),
    host(r'', settings.ROOT_URLCONF, name=' '),
    host(r'business','businessadmin.urls', name='bizadmin'),
    host(r'(?P<slug>[-\w]+)', 'calendarapp.urls', callback='calendarapp.views.get_companyslug',name='bookingurl'),

    # host(r'', settings.ROOT_URLCONF, name='www'),
)
