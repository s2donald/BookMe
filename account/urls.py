from django.urls import path
from . import views
from consumer import views as consviews
from django.contrib.auth import views as auth_views
app_name = 'account'
urlpatterns = [
    path('name/', views.NameChangeView, name='name'),
    path('email/', views.emailChangeView, name='email_update'),
    path('addbiz/',views.addBusinessView, name='add_biz'),
    path('phone/', views.phoneChangeView, name='phone_update'),
    path('homeaddress/',views.homeAddressChangeView, name='home_updated'),
    path('schedule/<slug:slug>/<int:id>/', consviews.bookingScheduleView, name='booking_sched'),
    path('services/<slug:slug>/<int:id>/', views.BusinessAccountsView , name='company_detailed'),
    path('list/', views.BusinessListViews, name='biz_list'),
    path('signup/', views.ConsumerRegistrationView, name ='signup'),
    path('done/', views.RegisteredAccountView, name='registered'),
    path('', views.AccountSummaryView, name='account')
]
