from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    path('registerb/', views.BusinessRegistrationView, name='registration'),
    path('registerc/', views.ConsumerRegistrationView, name='consumer_registration'),
    path('done/', views.RegisteredAccountView, name='registered'),
    path('', views.AccountSummaryView, name='account')
]
