from django.conf.urls import url, include
from django.urls import path
from . import views
app_name = 'calendarapp'
urlpatterns = [
    url(r'^account/updatep/$', views.phoneValidationView.as_view(), name='phoneupdate'),
    url(r'^login/', views.LoginView.as_view(), name='loginbooking'),
    url(r'^createbook/$', views.createAppointment.as_view(), name='creatingBooking'),
    url(r'^confirmbook/$', views.confbook.as_view(), name='confbook'),
    url(r'^bookingtime/$', views.bookingTimes.as_view(), name='bookingtimeretrieval'),
    url(r'^facebookLoginBooked/$', views.facebookLogin.as_view(), name='facebookLogin'),
    url(r'^requestclient/$', views.requestSpot.as_view(), name='requestSpotAsClient'),
    url(r'^checkIfClient/$', views.checkIfClientView.as_view(), name='checkIfClient'),
    url(r'^createAcct/$', views.createAccountView.as_view(), name='createAccount'),
    path('social-auth/',include('social_django.urls',namespace='social'), name='fb'),
    url(r'^service(?P<pk>\d+)/$', views.bookingServiceView, name='bookingserviceurls'),
    url(r'^$', views.bookingurl, name='bookingurls'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)