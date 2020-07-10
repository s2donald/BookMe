from django.urls import path
from . import views
app_name = 'business'
urlpatterns = [
    path('business/', views.ManageServiceListView.as_view(),name='manage_service_list'),
    path('business/create/', views.ServiceCreateView.as_view(),name='service_create'),
    path('business/edit/', views.ServiceUpdateView.as_view(),name='service_edit'),
    path('business/delete/', views.ServiceDeleteView.as_view(),name='service_delete'),
    path('<int:id>/<slug:slug>/',views.company_detail,name='company_detail'),
    path('<slug:category_slug>/',views.company_list, name='company_list_by_category'),
    path('list/', views.company_list, name='company_list'),
    path('', views.homepage, name='homepage'),
    
]