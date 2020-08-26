from django.conf.urls import url, include

from . import views
app_name = 'businessadmin'
urlpatterns = [
    url(r'^$', views.businessadmin, name='bizadminmain'),
]