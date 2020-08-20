from django.conf.urls import url, include

from . import views
app_name = 'calendarapp'
urlpatterns = [
    url(r'^page/$', views.bizadmin, name='businessadm'),
    url(r'^$', views.bookingurl, name='bookingurls'),
]