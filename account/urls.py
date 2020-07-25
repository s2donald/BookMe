from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    path('name/', views.NameChangeView, name='name'),
    path('<slug:slug>/<int:id>/', views.BusinessAccountsView , name='company_detailed'),
    path('list/', views.BusinessListViews, name='biz_list'),
    path('signup/', views.ConsumerRegistrationView, name ='signup'),
    path('done/', views.RegisteredAccountView, name='registered'),
    path('', views.AccountSummaryView, name='account')
]
