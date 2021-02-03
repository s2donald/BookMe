from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, viewsapi
from consumer import views as consviews
from django.contrib.auth import views as auth_views
app_name = 'account'
urlpatterns = [
    #Company API
    path('api/companylist/', viewsapi.CompanyList.as_view()),
    path('api/companydetail/<int:pk>/', viewsapi.CompanyDetail.as_view()),

    #Account API
    url(r'^api/user/create/$', viewsapi.UsersCreateView.as_view(), name="user_create"),
    url(r'^api/users/list/$', viewsapi.UsersListView.as_view(), name="users_list"),
    url(r'^api/users/(?P<pk>\d+)/detail/$', viewsapi.UserDetailView.as_view(), name="user_detail"),
    url(r'^api/users/(?P<pk>\d+)/update/$', viewsapi.UserUpdateView.as_view(), name="user_update"),
    url(r'^api/users/(?P<pk>\d+)/delete/$', viewsapi.UserDeleteView, name="user_delete"),

    #Booking API
    url(r'^api/booking/create/$', viewsapi.BookingCreateView.as_view(), name="booking_create"),
    url(r'^api/booking/list/$', viewsapi.BookingListView.as_view(), name="booking_list"),
    url(r'^api/booking/(?P<pk>\d+)/detail/$', viewsapi.BookingDetailView.as_view(), name="booking_detail"),

    path('homeaddress/',views.homeAddressChangeView, name='home_updated'),
    path('signup/', views.ConsumerRegistrationView, name ='signup'),
    path('done/', views.RegisteredAccountView, name='registered'),
    path('favourite/', views.favouriteViews, name='favourite'),
    path('reviews/', views.reviewsViews, name='reviews'),
    path('bookings/',consviews.FutPastBooking, name='booking_consumer'),
    path('updatep/', views.personalValidationView.as_view(),name='update_personal'),
    path('', views.AccountSummaryView, name='account'),
]

urlpatterns = format_suffix_patterns(urlpatterns)