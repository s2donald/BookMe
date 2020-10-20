from django.urls import path
from . import views
from consumer import views as consviews
from django.contrib.auth import views as auth_views
app_name = 'account'
urlpatterns = [
    path('homeaddress/',views.homeAddressChangeView, name='home_updated'),
    path('signup/', views.ConsumerRegistrationView, name ='signup'),
    path('done/', views.RegisteredAccountView, name='registered'),
    path('favourite/', views.favouriteViews, name='favourite'),
    path('reviews/', views.reviewsViews, name='reviews'),
    path('bookings/',consviews.FutPastBooking, name='booking_consumer'),
    path('updatep/', views.personalValidationView.as_view(),name='update_personal'),
    path('', views.AccountSummaryView, name='account'),
]
