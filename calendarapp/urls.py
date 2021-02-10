from django.conf.urls import url, include
from django.urls import path, re_path
from . import views
app_name = 'calendarapp'
urlpatterns = [
    re_path(r'^account/updatep/$', views.phoneValidationView.as_view(), name='phoneupdate'),
    re_path(r'^login/', views.LoginView.as_view(), name='loginbooking'),
    # re_path(r'^createbook/$', views.createAppointment.as_view(), name='creatingBooking'),
    # re_path(r'^confirmbook/$', views.confbook.as_view(), name='confbook'),
    re_path(r'^confirmationbookingmessage/$', views.confirmationMessageRender.as_view(), name='confirmationbooking'),
    re_path(r'^guestbookingformload/$', views.guestNewFormRender.as_view(), name='guestbookingformload'),
    re_path(r'^bookingtime/$', views.bookingTimes.as_view(), name='bookingtimeretrieval'),
    re_path(r'^renderguestformsub/$', views.guestFormRender.as_view(), name='guestformrender'),
    re_path(r'^renderloginpage/$', views.renderLoginPage.as_view(), name='renderloginpage'),
    re_path(r'^loadsignupform/$', views.loadSignUpForm.as_view(), name='loadsignupform'),
    re_path(r'^loadloginformreq/$', views.loadLoginFormRequest.as_view(), name='loadloginformreq'),
    re_path(r'^facebookLoginBooked/$', views.facebookLogin.as_view(), name='facebookLogin'),
    re_path(r'^requestclient/$', views.requestSpot.as_view(), name='requestSpotAsClient'),
    re_path(r'^checkIfClient/$', views.checkIfClientView.as_view(), name='checkIfClient'),
    re_path(r'^createAcct/$', views.createAccountView.as_view(), name='createAccount'),
    re_path(r'loginareturningcustomer/', views.loginReturningCustomer.as_view(), name='loginbookmereturning'),
    re_path(r'^renderstaffservice/', views.staffofferingservice.as_view(), name='staffofferingservice'),
    re_path(r'^renderbookingtimes/$', views.bookingTimesView.as_view(), name='getbookingtime'),
    re_path(r'^bookingbutton/$', views.bookingCalendarRender.as_view(), name='getbookingbuttons'),
    path('social-auth/',include('social_django.urls',namespace='social'), name='fb'),
    # re_path(r'^service(?P<pk>\d+)/$', views.bookingServiceView, name='bookingserviceurls'),
    # path('<slug:slug>/',views.bookingStaffUrl,name='getstaffurl'),
    re_path(r'^$', views.bookingurlupdated, name='bookingurls'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)