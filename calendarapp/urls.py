from django.conf.urls import url, include
from django.urls import path, re_path
from . import views
app_name = 'calendarapp'
urlpatterns = [
    re_path(r'^account/updatep/$', views.phoneValidationView.as_view(), name='phoneupdate'),
    re_path(r'^login/', views.LoginView.as_view(), name='loginbooking'),
    re_path(r'^createbook/$', views.createAppointment.as_view(), name='creatingBooking'),
    re_path(r'^confirmbook/$', views.confbook.as_view(), name='confbook'),
    re_path(r'^bookingtime/$', views.bookingTimes.as_view(), name='bookingtimeretrieval'),
    re_path(r'^facebookLoginBooked/$', views.facebookLogin.as_view(), name='facebookLogin'),
    re_path(r'^requestclient/$', views.requestSpot.as_view(), name='requestSpotAsClient'),
    re_path(r'^checkIfClient/$', views.checkIfClientView.as_view(), name='checkIfClient'),
    re_path(r'^createAcct/$', views.createAccountView.as_view(), name='createAccount'),
    # path('<slug:slug>/',views.bookingStaffUrl,name='company_detail'),
    path('social-auth/',include('social_django.urls',namespace='social'), name='fb'),
    re_path(r'^service(?P<pk>\d+)/$', views.bookingServiceView, name='bookingserviceurls'),
    re_path(r'^$', views.bookingurl, name='bookingurls'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)