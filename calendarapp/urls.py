from django.conf.urls import url, include

from . import views
app_name = 'calendarapp'
urlpatterns = [
    url(r'^confirmbook/$', views.confbook.as_view(), name='confbook'),
    url(r'^bookingtime/$', views.bookingTimes.as_view(), name='bookingtimeretrieval'),
    url(r'^page/$', views.bizadmin, name='businessadm'),
    url(r'^(?P<pk>\d+)$', views.bookingServiceView, name='bookingserviceurls'),
    url(r'^$', views.bookingurl, name='bookingurls'),
]