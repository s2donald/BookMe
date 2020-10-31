from django.urls import path
from . import views
app_name = 'business'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('privacy/', views.privacyViews, name='privacy'),
    path('terms/', views.tosViews, name='terms'),
    path('ajax/cancelAppt/', views.cancelAppointmentAjax.as_view(), name='cancelAppointment'),
    path('services/<int:id>/<slug:slug>/', views.ManageServiceListView,name='manage_service_list'),
    path('create/<int:pk>/<slug:slug>/', views.CreateServiceView, name='create_service'),
    path('delete/<int:pk>/<int:pks>/<slug:slug>/', views.DeleteServiceView, name='delete_service'),
    path('update/<int:pk>/<int:pks>/<slug:slug>/', views.UpdateServiceView, name='update_service'),
    path('userlike', views.company_like.as_view(), name='company_like'),
    path('list/', views.company_list, name='company_list'),
    path('search', views.allsearch,name='bizsearch'),
    path('<slug:slug>/<int:id>/',views.company_detail,name='company_detail'),
    path('<slug:category_slug>/',views.company_list, name='company_list_by_category'),
    
    
]