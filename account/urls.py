from django.urls import path
from . import views
from consumer import views as consviews
from django.contrib.auth import views as auth_views
app_name = 'account'
urlpatterns = [
    path('addbiz/',views.addBusinessView, name='add_biz'),
    path('homeaddress/',views.homeAddressChangeView, name='home_updated'),
    path('schedule/<slug:slug>/<int:id>/', consviews.bookingScheduleView, name='booking_business'),
    path('services/<slug:slug>/<int:id>/', views.BusinessAccountsView , name='company_detailed'),
    path('list/', views.BusinessListViews, name='biz_list'),
    path('signup/', views.ConsumerRegistrationView, name ='signup'),
    path('done/', views.RegisteredAccountView, name='registered'),
    path('bookings/',consviews.FutPastBooking, name='booking_consumer'),
    path('updatep/', views.personalValidationView.as_view(),name='update_personal'),
    path('', views.AccountSummaryView, name='account'),
]
